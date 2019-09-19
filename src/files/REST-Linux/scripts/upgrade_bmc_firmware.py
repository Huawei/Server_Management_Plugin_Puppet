# -*- coding:utf-8 -*-
import sys
from os import path

'''
#=========================================================================
#   @Description:  upgrade BMC firmware
#
#   @author:
#   @Date:
#=========================================================================
'''


def upgradebmcfirmware_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  Initialize BMC firmware upgrade subcommands
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('upgradefw',
                                   help='''upgrade firmware''')

    sub_parser.add_argument('-i', dest='imageuri',
                            required=True,
                            help='''Path of the upgrade package on a remote server. \
                it is in the \
                protocol://username:password@ip/directory/filename \
                format. supported protocols include \
                https, scp, sftp, cifs, and nfs''')
    # sub_parser.add_argument('-F', dest='file',
    #                         required=False,
    #                         help='''the local path and file name of upload file,''' + \
    #                              '''file extensions should be ".hpm"''')

    parser_list['upgradefw'] = sub_parser

    return 'upgradefw'


def upgradebmcfirmware(client, parser, args):
    '''
    #=====================================================================
    #   @Method:  BMC firmware upgrade
    #   @Param:   client, RedfishClient object
                  parser, subcommand argparser. Export error messages when parameters are incorrect
                  args, parameter list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    url = "/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate"
    # if args.imageuri is None and args.file is None:
    #     parser.error('usage: urest upgradefw [-h] [-i IMAGEURI] [-F FILE]')
    # if args.imageuri is not None and args.file is not None:
    #     parser.error('Failure: parameter "-i" or "-F" conflict')
    payload = {}
    image_uri = args.imageuri

    # treat it as local file
    if path.isfile(image_uri):
        if str(image_uri).split('.')[-1] != 'hpm':
            print('Failure: update firmware file type should be \'.hpm\'')
            return None
        if str(image_uri).split('/')[-1] == image_uri:
            filename = str(image_uri).split("\\")[-1]
        else:
            filename = str(image_uri).split('/')[-1]
        ret = upload_file(client, args, filename)
        if ret is False:
            return None
        payload['ImageURI'] = ('/tmp/web/' + filename)
    else:
        protocol = None
        protocol_list = ['https', 'scp', 'sftp', 'cifs', 'nfs']
        for item in protocol_list:
            if image_uri.lower().startswith(item + "://"):
                lower_scheme = image_uri[:len(item)].lower()
                image_uri = lower_scheme + image_uri[len(item):]
                protocol = item.upper()
                payload['ImageURI'] = image_uri
                payload['TransferProtocol'] = protocol
                break

        if protocol == '':
            message = ('File Uri %s is not supported, '
                       'file transfer protocols should be one of %s.')
            parser.error(message % (image_uri, ','.join(protocol_list)))

        payload['ImageURI'] = args.imageuri
        payload['TransferProtocol'] = protocol

    resp = client.create_resource(url, payload, timeout=20)
    if resp is None:
        return None

    if resp['status_code'] == 202:
        # resp = client.print_task_prog(resp, maxtime=3600)
        prog_resp = client.print_task_prog(resp, maxtime=3600)
        if prog_resp == 'Exception':
            taskid = resp['resource']['@odata.id']
            task_resp = client.get_resource(taskid)
            if task_resp is None:
                return None
            elif task_resp['status_code'] != 200:
                return task_resp

            message_id = task_resp['resource']['Messages'] \
                ['MessageId'].split(".")[-1]

            if message_id == 'FirmwareUpgradeError' \
                    or message_id == 'FileTransferErrorDesc':
                message_info = task_resp['resource']['Messages']['Message']
                pos = message_info.find('Details: ')
                message_info = message_info[(pos + 9):-1]
                print('Failure: %s' % message_info)
            else:
                print('Failure: ' + message_id)
            sys.exit(144)

    elif resp['status_code'] == 400:
        err_400_proc(resp)
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')

    return resp


def upload_file(client, args, filesname):
    '''
    #====================================================================================
    #   @Method:  upload file
    #   @Param:
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    url_upload = "/redfish/v1/UpdateService/FirmwareInventory"
    if not path.isfile(args.imageuri):
        print ("Failure: the file does not exist")
        return False
    files = {
        'imgfile': (
            filesname, open(args.imageuri, 'rb'),
            "multipart/form-data",
            {'user_name': client.username}
        )
    }

    if files is None:
        print ("Failure: the file open failed, please try again")
        return False

    resp = client.create_resource(url_upload, files=files, timeout=300)
    if resp is None:
        return False
    if resp['status_code'] != 202:
        print('Failure: Upload files failed.')
        print('Parameter -F only supports iBMC version 2.97 or later')
        return False

    return None


def err_400_proc(resp):
    '''
    #=====================================================================
    #   @Method:  When the response code is 400, process error messages
    #   @Param:   resp, redfish response result
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    message_id = resp['message']['error'] \
        ['@Message.ExtendedInfo'][0]['MessageId'].split(".")[-1]

    if message_id == 'ActionParameterValueFormatError':
        print('Failure: the value for -i is of a different format ' + \
              'than the parameter can accept')
    elif message_id == 'FirmwareUpgrading':
        print('Failure: a file transfer task is being performed or ' + \
              'an upgrade operation is in progress')
    elif message_id == 'FileDownloadTaskOccupied':
        print('Failure: other file is transfering, ' + \
              'current upgrade request failed')
    elif message_id == 'TaskLimitExceeded':
        print('Failure: the asynchronous operation failed because the ' + \
              'number of simultaneous tasks has reached the limit')
    else:
        print('Failure: status code 400')

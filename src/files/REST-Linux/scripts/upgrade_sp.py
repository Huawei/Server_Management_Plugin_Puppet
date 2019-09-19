# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  upgrade sp
#    
#   @author: 
#   @Date: 
#=========================================================================
'''
import sys
import time


def upgradesp_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  Initialize SP upgrade subcommands
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    sub_parser = parser.add_parser('upgradesp',
                                   help='''upgrade sp''')
    sub_parser.add_argument('-i', dest='imageuri',
                            required=True,
                            help='''Path of the upgrade package on a remote server. \
                    it is in the \
                    protocol://username:password@ip/directory/filename \
                    format.''')
    sub_parser.add_argument('-si', dest='signatureuri',
                            required=True,
                            help='''Path of the upgrade package digital signature \
                    file on a remote server. it is in the \
                    protocol://username:password@ip/directory/filename \
                    format.''')
    sub_parser.add_argument('-T', dest='imagetype',
                            required=True,
                            choices=['Firmware', 'SP'],
                            help='''type of the upgrade package''')
    sub_parser.add_argument('-PARM', dest='parameter',
                            required=True,
                            help=''''all' indicates the entire upgrade package or a \
                    specific upgrade package''')
    sub_parser.add_argument('-M', dest='mode',
                            required=True,
                            choices=['Auto', 'Full', 'Recover', 'APP', 'Driver'],
                            help='''mode of the upgrade''')
    sub_parser.add_argument('-ACT', dest='activemethod',
                            required=True,
                            help='''how does the upgrade take effect''')

    parser_list['upgradesp'] = sub_parser

    return 'upgradesp'


def upgradesp(client, parser, args):
    '''
    #=====================================================================
    #   @Method:  SP upgrade
    #   @Param:   client, RedfishClient object
                  parser, subcommand argparser. Export error messages when parameters are incorrect
                  args, parameter list
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    if parser is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/SPService/SPFWUpdate/1/" % slotid + \
          "Actions/SPFWUpdate.SimpleUpdate"

    payload = {}
    payload['ImageURI'] = args.imageuri
    payload['SignalURI'] = args.signatureuri
    payload['ImageType'] = args.imagetype
    payload['Parameter'] = args.parameter
    payload['UpgradeMode'] = args.mode
    payload['ActiveMethod'] = args.activemethod

    resp = client.create_resource(url, payload, timeout=20)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        resp = get_upgrade_progress(client, args.imagetype)
    elif resp['status_code'] == 400:
        err_400_proc(resp)
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    else:
        print_status_code(resp)

    return resp


def get_upgrade_progress(client, imagetype):
    '''
    #=====================================================================
    #   @Method:  Obtain the upgrade progress
    #   @Param:   client, RedfishClient client
    #   @Return:
    #   @author:
    #   @Modify: Modify the Return value when the upgrade is successful.
    #=====================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/SPService/SPFWUpdate/1" % slotid

    time.sleep(3)
    resp = client.get_resource(url)
    if resp is None:
        return None

    status_code = resp['status_code']
    if status_code != 200:
        print_status_code(resp)
        return resp
    # sys.stdout.write("Progress: 0%\r")
    # sys.stdout.flush()

    while status_code == 200:
        progress = resp['resource']['TransferProgressPercent']

        count = 0
        while count != -1 and progress is None:
            if count == 20:
                error_info = ''
                if "Messages" in resp['resource'].keys() \
                        and len(resp['resource']['Messages']) > 0:
                    messages = resp['resource']['Messages'][0]
                    if "Message" in messages.keys():
                        error_info = messages["Message"]
                print('Failure: request progress timed out. ' + error_info)
                sys.exit(144)

            time.sleep(1)
            count = count + 1

            resp = client.get_resource(url)
            if resp is None:
                return None

            status_code = resp['status_code']
            if status_code != 200:
                print_status_code(resp)
                return resp

            progress = resp['resource']['TransferProgressPercent']

        count = -1

        # if progress is not None:
        #     sys.stdout.write("Progress: %d%%\r" % int(progress))
        #     sys.stdout.flush()

        if int(progress) == 100:
            if imagetype == 'Firmware':
                print('Success: file downloaded successfully, '
                      'start SP for the file to take effect')
            else:
                print('Success: successfully completed request')
            return resp

        time.sleep(1)

        resp = client.get_resource(url)
        if resp is None:
            return None

        status_code = resp['status_code']
        if status_code != 200:
            print_status_code(resp)
            return resp
    return resp


def print_status_code(resp):
    """
    print status code
    :return:
    """
    error_code = "0"
    if resp['status_code']:
        error_code = str(resp['status_code'])
    print('Failure: status code ' + error_code)


def err_400_proc(resp):
    '''
    #=====================================================================
    #   @Method:  When the response code is 400, process error messages
    #   @Param:   resp, request response results
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    message_info = resp['message']['error'] \
        ['@Message.ExtendedInfo'][0]['Message']

    print('Failure: %s' % message_info)

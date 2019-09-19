# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  upgrade driver
#
#   @author:
#   @Date:
#=========================================================================
'''
import sys
import time
import upgrade_sp


def upgradedriver_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  Initialize BMC firmware upgrade subcommands
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('upgradedriver',
                                   help='''upgrade driver''')
    sub_parser.add_argument('-i', dest='imageuri',
                            required=True,
                            help='''path of the upgrade package which can be \
                    IP/tmp/filename for a package on the BMC or \
                    IP/directory/filename for a package on a remote server.''')
    sub_parser.add_argument('-si', dest='signatureuri',
                            required=True,
                            help='''path of the upgrade package digital signature \
                    file which can be IP/tmp/filename for a signature file on \
                    the BMC or IP/directory/filename for a signature file on \
                    a remote server.''')
    sub_parser.add_argument('-PRO', dest='protocol',
                            required=True,
                            choices=['SFTP'],
                            help='''protocol used to download the upgrade package''')
    sub_parser.add_argument('-U', dest='accessuser',
                            required=True,
                            help='''user name for upgrade package access''')
    sub_parser.add_argument('-P', dest='accesspassword',
                            required=True,
                            help='''password for upgrade package access''')
    sub_parser.add_argument('-PARM', dest='parameter',
                            required=True,
                            help=''''all' indicates the entire upgrade package or a \
                    specific upgrade package (for example package1.rpm)''')
    sub_parser.add_argument('-ACT', dest='activemethod',
                            choices=['OSRestart', 'ServerRestart'],
                            help='''how does the upgrade take effect''')

    parser_list['upgradedriver'] = sub_parser

    return 'upgradedriver'


def upgradedriver(client, parser, args):
    '''
    #=====================================================================
    #   @Method:  In-band driver upgrade
    #   @Param:   client, RedfishClient object
                  parser, subcommand argparser. Export error messages when parameters are incorrect
                  args, parameter list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if parser is None:
        return None

    url = "/redfish/v1/Sms/1/UpdateService/Actions/UpdateService.SimpleUpdate"

    payload = {}
    payload['ImageURI'] = args.imageuri
    payload['SignalURI'] = args.signatureuri
    payload['ImageType'] = 'Driver'
    payload['TransferProtocol'] = args.protocol
    payload['User'] = args.accessuser
    payload['Password'] = args.accesspassword
    payload['Parameter'] = args.parameter
    if args.activemethod is None:
        payload['ActiveMethod'] = ''
    else:
        payload['ActiveMethod'] = args.activemethod

    resp = client.create_resource(url, payload, timeout=20)
    if resp is None:
        return None

    # If the upgrade is successful, query the upgrade progress.
    if resp['status_code'] == 200:
        resp = get_upgrade_progress(client)
    elif resp['status_code'] == 400:
        err_400_proc(resp)
    elif resp['status_code'] == 404:
        print('Failure: failed to obtain iBMA information')

    return resp


def get_upgrade_progress(client):
    '''
    #=====================================================================
    #   @Method:  Obtain the in-band upgrade progress
    #   @Param:   client, RedfishClient object
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    url = "/redfish/v1/Sms/1/UpdateService/Progress"

    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] != 200:
        upgrade_sp.print_status_code(resp)
        return resp

    status = resp['resource']['Status']
    while status == 'done' or status == 'uploading' \
            or status == 'tobeupgraded' or status == 'preprocessing':
        # sys.stdout.write("Progress: 0%\r")
        # sys.stdout.flush()
        time.sleep(1)

        resp = client.get_resource(url)
        if resp is None:
            return None

        if resp['status_code'] != 200:
            upgrade_sp.print_status_code(resp)
            return resp

        status = resp['resource']['Status']

    while status == 'upgrading':
        progress = resp['resource']['Progress']
        # sys.stdout.write("Progress: %d%%\r" % int(float(progress)))
        # sys.stdout.flush()
        time.sleep(1)

        resp = client.get_resource(url)
        if resp is None:
            return None

        if resp['status_code'] != 200:
            upgrade_sp.print_status_code(resp)
            return resp

        status = resp['resource']['Status']

    flag = suc_or_fail_proc(status, resp)
    if not flag:
        sys.exit(144)
    return resp


def suc_or_fail_proc(status, resp):
    '''
    #=====================================================================
    #   @Method:  Display final success or failure messages
    #   @Param:   status, current upgrade status
                   resp, response results
    #   @Return:
    #   @author:
    #   @Modify: DTS2018042500700: Log analysis
    #=====================================================================
    '''
    flag = False
    # DTS2018042500700
    # If the status is activing, the upgrade is successful.
    if status == 'activing':
        print "Success: successfully completed request"
        sys.exit(0)

    if status == 'tobeactived':
        failure_items = []
        for item in resp['resource']['Log'].values():
            if item['Result'] != 'success':
                failure_items.append(item['File'])

        if len(failure_items) == 0:
            flag = True
            print('Success: successfully completed request')
        else:
            print('Failure: failed to executing some upgrade packages')
            for item in failure_items:
                print('         %s' % item)

    if status == 'error':
        message_info = resp['resource']['Message']

        if message_info.startswith('ImageURI or SingleURI') is True:
            message_info = message_info.replace('ImageURI or SingleURI', \
                                                'image uri or signature uri')
        elif message_info[0].isupper() is True:
            message_info = message_info[0].lower() + message_info[1:]

        if message_info[-1] == '.':
            message_info = message_info[0:-1]

        print('Failure: %s' % message_info)
    return flag


def err_400_proc(resp):
    '''
    #=====================================================================
    #   @Method:  When the response code is 400, process error messages
    #   @Param:   resp, request response results
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    message_info = resp['message']['message']

    if message_info.startswith('ImageURI') is True:
        message_info = message_info.replace('ImageURI', \
                                            'image uri specified by -i')
    elif message_info.startswith('SignalURI') is True:
        message_info = message_info.replace('SignalURI', \
                                            'signature uri specified by -si')
    elif message_info.startswith('Server IP address') is True:
        message_info = message_info.replace('Server IP address', \
                                            'server ip address specified by -i or -si')
    elif message_info.startswith('Server port') is True:
        message_info = message_info.replace('Server port', \
                                            'server port specified by -i or -si')
    elif message_info.startswith('Parameter') is True:
        message_info = message_info.replace('Parameter', \
                                            'parameter specified by -PARM')
    elif message_info.startswith('User or Password') is True:
        message_info = message_info.replace('User or Password', \
                                            'user name or password')
    else:
        message_info = 'status code 400'

    print('Failure: %s' % message_info[0:-1])

# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set the SP service enabling function and timeout interval.
# @command: setsp
# @Param: 
# @author: 
# @date: 2017.11.14
#==========================================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '


def setspinfo_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register commands for setting the SP service.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('setspinfo',
                                   help='''set sp service information''')
    sub_parser.add_argument('-S', dest='SPStartEnabled',
                            type=str, required=False, choices=['True', 'False'], \
                            help='''SP Service Start State''')
    sub_parser.add_argument('-T', dest='SysRestartDelaySeconds', type=int, \
                            required=False, help='''System restart delay time''')
    sub_parser.add_argument('-O', dest='SPTimeout', type=int, \
                            required=False, help='''Maximum time allowed for SP deployment.''')
    sub_parser.add_argument('-F', dest='SPFinished', type=str, \
                            choices=['True', 'False'],
                            required=False, help='''Status of the transaction deployed.''')
    parser_list['setspinfo'] = sub_parser

    return 'setspinfo'


def setspinfo(client, parser, args):
    '''
    #===========================================================
    # @Method: Set processing functions of the SP service.
    # @Param:client, parser, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    if (args.SPStartEnabled is None and args.SysRestartDelaySeconds is None 
        and args.SPTimeout is None and args.SPFinished is None):
        parser.error('at least one parameter must be specified')
    slotid = client.get_slotid()
    if slotid is None:
        return None

        # Query whether resources exist.
    url = "/redfish/v1/Managers/" + slotid + "/SPService"
    resp = client.get_resource(url)
    if resp is None:
        return None
    if resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

    # Fill the request body.
    payload = {}
    if args.SPStartEnabled is not None:
        if args.SPStartEnabled == "False":
            payload["SPStartEnabled"] = False
        else:
            payload["SPStartEnabled"] = True
    if args.SysRestartDelaySeconds is not None:
        payload["SysRestartDelaySeconds"] = args.SysRestartDelaySeconds
    
    if args.SPTimeout is not None:
        if args.SPTimeout >86400 or args.SPTimeout < 300:
            parser.error('''argument -SPTimeout: invalid choice: '%s' (''' % \
                         args.SPTimeout + '''choose from '300' to '86400')''')
            return None
        payload["SPTimeout"] = args.SPTimeout

    if args.SPFinished is not None:
        if args.SPFinished == "False":
            payload["SPFinished"] = False
        else:
            payload["SPFinished"] = True

    # Set attributes.
    resp = client.set_resource(url, payload)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        check_err_info(resp['resource'], resp['status_code'])
    if resp['status_code'] == 400:
        check_err_info(resp['message']['error'], resp['status_code'])
    return resp


def check_err_info(resp, code):
    '''
    #====================================================================================
    # @Method: Check error information.
    # @Param:args
    # @Return:
    # @author: 
    #====================================================================================
    '''
    idx = 0
    # Success flag
    flag = 0
    for key in resp:
        if key == '@Message.ExtendedInfo':
            err_message = resp[key]
            flag = 1
    if flag == 0:
        print('Success: successfully completed request')
        return resp

    # Determine whether a permission problem exists.
    if err_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege":
        print('Failure: you do not have the' + \
              ' required permissions to perform this operation')
        return None
    # Determine messages according to the returned codes.
    if code == 200:
        print(FAILURE_MESS)
        # Poll error information.
        while idx < len(err_message):
            check_info = '         %s' % err_message[idx]['Message']
            print(check_info[:len(check_info) - 1].lower())
            idx += 1
        sys.exit(144)
    if code == 400:
        # The first message must be in a single line.
        sys.stdout.write('Failure: ')
        # Poll error information.
        while idx < len(err_message):
            if idx == 0:
                check_info = '%s' % err_message[idx]['Message']
                print(check_info[:len(check_info) - 1].lower())
            else:
                check_info = '         %s' % err_message[idx]['Message']
                print(check_info[:len(check_info) - 1].lower())
            idx += 1
        return None

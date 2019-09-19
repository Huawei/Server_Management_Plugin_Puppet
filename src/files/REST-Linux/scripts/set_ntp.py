# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set NTP information.
# @command: setntp
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '
PRE_ERR = 'argument -PRE: the length of the parameter \
exceeds the value range (0 to 67 characters)'
ALT_ERR = 'argument -ALT: the length of the parameter \
exceeds the value range (0 to 67 characters)'


def setntp_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain NTP setting commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('setntp',
                                   help='''set network time protocol information''')
    sub_parser.add_argument('-M', dest='NtpAddressOrigin',
                            type=str, required=False,
                            choices=['Static', 'IPv4', 'IPv6'], help='''NTP mode''')
    sub_parser.add_argument('-S', dest='ServiceEnabled',
                            type=str, required=False,
                            choices=['True', 'False'], help='''NTP enable status''')
    sub_parser.add_argument('-PRE', dest='PreferredNtpServer',
                            type=str, required=False,
                            help='''preferred NTP server address''')
    sub_parser.add_argument('-ALT', dest='AlternateNtpServer',
                            type=str, required=False,
                            help='''alternative NTP server address''')
    sub_parser.add_argument('-MIN', dest='MinPollingInterval',
                            type=int, required=False,
                            help='''minimum NTP synchronization interval. \
        the value ranges from 3 to 17''')
    sub_parser.add_argument('-MAX', dest='MaxPollingInterval',
                            type=int, required=False,
                            help='''maximum NTP synchronization interval. \
        the value ranges from 3 to 17''')
    sub_parser.add_argument('-AUT', dest='ServerAuthenticationEnabled',
                            type=str, required=False,
                            choices=['False', 'True'], help='''enable auth status''')

    parser_list['setntp'] = sub_parser

    return 'setntp'


def body_mess(payload, args):
    '''
    #====================================================================================
    # @Method: Encapsulate the request body.
    # @Param: args, payload
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if args.NtpAddressOrigin is not None:
        payload['NtpAddressOrigin'] = args.NtpAddressOrigin
    if args.ServiceEnabled is not None:
        if args.ServiceEnabled == 'False':
            payload['ServiceEnabled'] = False
        else:
            payload['ServiceEnabled'] = True
    if args.PreferredNtpServer is not None:
        payload['PreferredNtpServer'] = args.PreferredNtpServer
    if args.ServerAuthenticationEnabled is not None:
        if args.ServerAuthenticationEnabled == 'False':
            payload['ServerAuthenticationEnabled'] = False
        else:
            payload['ServerAuthenticationEnabled'] = True
    if args.MinPollingInterval is not None:
        payload['MinPollingInterval'] = args.MinPollingInterval
    if args.MaxPollingInterval is not None:
        payload['MaxPollingInterval'] = args.MaxPollingInterval
    if args.AlternateNtpServer is not None:
        payload['AlternateNtpServer'] = args.AlternateNtpServer


def ntp_info(parser, args, payload):
    '''
    #====================================================================================
    # @Method: Parameter check
    # @Param:parser, args, payload
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if args.NtpAddressOrigin is None and \
                    args.ServiceEnabled is None and args.PreferredNtpServer is None \
            and args.AlternateNtpServer is None and \
                    args.MinPollingInterval is None and \
                    args.MaxPollingInterval is None and \
                    args.ServerAuthenticationEnabled is None:
        parser.error('at least one parameter is required')
    if args.MinPollingInterval is not None and \
            (args.MinPollingInterval < 3 or args.MinPollingInterval > 17):
        parser.error('argument -MIN: invalid choice: %s (choose from 3 to 17)' %
                     args.MinPollingInterval)
    if args.MaxPollingInterval is not None and \
            (args.MaxPollingInterval < 3 or args.MaxPollingInterval > 17):
        parser.error('argument -MAX: invalid choice: %s (choose from 3 to 17)' %
                     args.MaxPollingInterval)
    if args.PreferredNtpServer is not None and len(args.PreferredNtpServer) > 67:
        parser.error(PRE_ERR)
    if args.AlternateNtpServer is not None and len(args.AlternateNtpServer) > 67:
        parser.error(ALT_ERR)
    body_mess(payload, args)


def all_err(err_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, err_message
    # @Return:
    # @date:2017.08.29 17:28
    #====================================================================================
    '''
    idx = 0
    while idx < len(err_message):
        check_info = err_message[idx]['Message']
        if idx == 0:
            print('%s%s' % (check_info[0].lower(), check_info[1:len(check_info) - 1]))
        else:
            print('         %s%s' % (check_info[0].lower(), check_info[1:len(check_info) - 1]))
        idx += 1


def part_err(err_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, err_message
    # @Return:
    # @date:2017.08.20 14:26
    #====================================================================================
    '''
    idx = 0
    while idx < len(err_message):
        check_info = err_message[idx]['Message']
        print('         %s%s' % \
              (check_info[0].lower(), check_info[1:len(check_info) - 1]))
        idx += 1


def check_err_info(resp, code):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInf
    # @Param:resp
    # @Return:
    # @author: 
    #====================================================================================
    '''
    err_message = ""
    mess = resp.get("@Message.ExtendedInfo", "")
    if len(mess) != 0:
        err_message = resp["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs.
    if err_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege":
        print('Failure: you do not have the' +
              ' required permissions to perform this operation')
        return None
    # Independent display of 400 messages
    if code == 400:
        sys.stdout.write('Failure: ')
        all_err(err_message)
        return None
    if code == 200:
        print(FAILURE_MESS)
        part_err(err_message)
        sys.exit(144)
    return resp


def check_pollinginterval(parser, args, resp):
    '''
    #====================================================================================
    # @Method: Check the interval.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    ntpinfo = resp.get('resource', None)
    if ntpinfo is None:
        return None
    ntp_min = ntpinfo.get("MinPollingInterval", None)
    ntp_max = ntpinfo.get("MaxPollingInterval", None)
    if args.MinPollingInterval is not None:
        if ntp_min is None:
            parser.error('argument -MIN: the server did ' +
                         'not support the functionality required')
        elif args.MinPollingInterval > ntp_max \
                and args.MaxPollingInterval is None:
            parser.error('argument -MIN: minimum NTP ' +
                         'synchronization interval must be less than ' +
                         'or equal to maximum NTP synchronization interval')

    if args.MaxPollingInterval is not None:
        if ntp_max is None:
            parser.error('argument -MAX: the server did not ' +
                         'support the functionality required')
        elif args.MaxPollingInterval < ntp_min \
                and args.MinPollingInterval is None:
            parser.error('argument -MAX: maximum NTP ' +
                         'synchronization interval must be greater ' +
                         'than or equal to minimum NTP synchronization interval')

    if args.MaxPollingInterval is not None and \
                    args.MinPollingInterval is not None:
        if args.MaxPollingInterval < args.MinPollingInterval:
            parser.error('argument -MAX: maximum NTP ' +
                         'synchronization interval must be greater ' +
                         'than or equal to minimum NTP synchronization interval')
    return True


def setntp(client, parser, args):
    '''
    #====================================================================================
    # @Method: Set NTP information processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
     args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    payload = {}
    ntp_info(parser, args, payload)
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Managers/%s/Ntpservice" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp
    # Determine the time synchronization validity.
    ret = check_pollinginterval(parser, args, resp)
    if ret is None:
        return None

    # Set attributes.
    resp = client.set_resource(url, payload)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        # Determine whether all attributes are set successfully. Query @Message.ExtendedInf
        check_err_info(resp['resource'], resp['status_code'])
    if resp['status_code'] == 400:
        check_err_info(resp['message']['error'], resp['status_code'])
    return resp

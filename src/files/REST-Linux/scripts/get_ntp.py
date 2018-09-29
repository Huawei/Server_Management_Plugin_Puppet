# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query NTP information.
# @command: getntp
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
NTP_FORMAT = "%-30s: %s"


def getntp_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain NTP information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getntp',
                                   help='''get network time protocol information''')
    parser_list['getntp'] = sub_parser

    return 'getntp'


def getntp(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain NTP information command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/managers/%s/ntpservice" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] == 200:
        ntpinfo = resp['resource']
        print((NTP_FORMAT) % ("ServiceEnabled",
                              ntpinfo.get("ServiceEnabled", None)))
        print((NTP_FORMAT) % ("PreferredNtpServer",
                              ntpinfo.get("PreferredNtpServer", None)))
        print((NTP_FORMAT) % ("AlternateNtpServer",
                              ntpinfo.get("AlternateNtpServer", None)))
        print((NTP_FORMAT) % ("NtpAddressOrigin",
                              ntpinfo.get("NtpAddressOrigin", None)))
        print((NTP_FORMAT) % ("ServerAuthenticationEnabled",
                              ntpinfo.get("ServerAuthenticationEnabled", None)))
        print((NTP_FORMAT) % ("MinPollingInterval",
                              ntpinfo.get("MinPollingInterval", None)))
        print((NTP_FORMAT) % ("MaxPollingInterval",
                              ntpinfo.get("MaxPollingInterval", None)))
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    return resp

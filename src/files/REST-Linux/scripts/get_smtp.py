# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query SMTP information.
# @command: getsmtp
# @Param: 
# @author: 
# @date: 2018.8.11
#==========================================================================
'''
SMTP_FORMAT = "%-30s: %s"


def getsmtp_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain NTP information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getsmtp',
                                   help='''get SMTP Service infomation''')
    parser_list['getsmtp'] = sub_parser
    return 'getsmtp'


def getsmtp(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain SMTP service information command processing functions.
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

    url = "/redfish/v1/managers/%s/SmtpService" % slotid
    resp = client.get_resource(url)

    if resp is None:
        return None
    elif resp['status_code'] == 200:
        smtpinfo = resp['resource']
        subject_contains = ", ".join(smtpinfo.get("EmailSubjectContains", []))
        print("[SMTP]")
        print("-" * 60)
        print(SMTP_FORMAT % ("ServiceEnabled",
                             smtpinfo.get("ServiceEnabled", None)))
        print(SMTP_FORMAT % ("ServerAddress",
                             smtpinfo.get("ServerAddress", None)))
        print(SMTP_FORMAT % ("TLSEnabled",
                             smtpinfo.get("TLSEnabled", None)))
        print(SMTP_FORMAT % ("AnonymousLoginEnabled",
                             smtpinfo.get("AnonymousLoginEnabled", None)))
        print(SMTP_FORMAT % ("SenderUserName",
                             smtpinfo.get("SenderUserName", None)))
        print(SMTP_FORMAT % ("SenderAddress",
                             smtpinfo.get("SenderAddress", None)))
        # print(SMTP_FORMAT % ("SenderPassword",
        #                      smtpinfo.get("SenderPassword", None)))
        print(SMTP_FORMAT % ("EmailSubject",
                             smtpinfo.get("EmailSubject", None)))
        print(SMTP_FORMAT % ("EmailSubjectContains", subject_contains))
        print(SMTP_FORMAT % ("AlarmSeverity",
                             smtpinfo.get("AlarmSeverity", None)))

        headers = ["MemberId", "EmailAddress", "Description", "Enabled"]
        recipients = smtpinfo.get("RecipientAddresses", [])
        rows = [[r[key] for key in headers] for r in recipients]
        if len(recipients) > 0:
            from tabulate import tabulate
            print("\n[RecipientAddresses]")
            print(tabulate(rows, headers=headers, tablefmt='psql'))

    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    return resp

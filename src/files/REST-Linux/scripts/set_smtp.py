# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set SMTP information.
# @command: setsmtp
# @Param: 
# @author: 
# @date: 2018.8.13
#==========================================================================
'''
import sys

EMAIL_SUBJECT_CONTAINS = ["HostName", "BoardSN", "ProductAssetTag"]

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '


def setsmtp_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain SMTP setting commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''

    sp = parser.add_parser('setsmtp',
                           help='''set smtp alert information''')
    sp.add_argument('-S', dest='ServiceEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''SMTP enable status''')
    sp.add_argument('-SERVER', dest='ServerAddress',
                    type=str, required=False,
                    help='''SMTP server address''')
    sp.add_argument('-TLS', dest='TLSEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''SMTP TLS enable status''')
    sp.add_argument('-ANON', dest='AnonymousLoginEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''Anonymous Login enabled status''')
    sp.add_argument('-SA', dest='SenderAddress',
                    type=str, required=False,
                    help='''Email sender address''')
    sp.add_argument('-SP', dest='SenderPassword',
                    type=str, required=False,
                    help='''Email Sender password''')
    sp.add_argument('-SU', dest='SenderUserName',
                    type=str, required=False,
                    help='''Email sender username''')
    sp.add_argument('-ES', dest='EmailSubject',
                    type=str, required=False,
                    help='''Email subject''')
    sp.add_argument('-ESC', dest='EmailSubjectContains', nargs='*',
                    type=str, required=False,
                    help='''Email subject keywords which should be
                                a list of specified keywords, example:
                                -ESC HostName BoardSN ProductAssetTag''')
    sp.add_argument('-AS', dest='AlarmSeverity',
                    type=str, required=False,
                    help='''Severities of alarms to be sent through
                            the SMTP server.''',
                    choices=['Critical', 'Major', 'Minor', 'Normal'])

    help = '''whether receipt address 1 enabled'''
    sp.add_argument('-R1-Enabled', dest='Receipt1Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)
    help = '''whether receipt address 2 enabled'''
    sp.add_argument('-R2-Enabled', dest='Receipt2Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)
    help = '''whether receipt address 3 enabled'''
    sp.add_argument('-R3-Enabled', dest='Receipt3Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)
    help = '''whether receipt address 4 enabled'''
    sp.add_argument('-R4-Enabled', dest='Receipt4Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    help = '''Receipt 4 address'''
    sp.add_argument('-R4-Addr', dest='Receipt4Address',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 3 address'''
    sp.add_argument('-R3-Addr', dest='Receipt3Address',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 2 address'''
    sp.add_argument('-R2-Addr', dest='Receipt2Address',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 1 address'''
    sp.add_argument('-R1-Addr', dest='Receipt1Address',
                    type=str, required=False,
                    help=help)

    help = '''Receipt 4 Description'''
    sp.add_argument('-R4-Desc', dest='Receipt4Description',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 3 Description'''
    sp.add_argument('-R3-Desc', dest='Receipt3Description',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 2 Description'''
    sp.add_argument('-R2-Desc', dest='Receipt2Description',
                    type=str, required=False,
                    help=help)
    help = '''Receipt 1 Description'''
    sp.add_argument('-R1-Desc', dest='Receipt1Description',
                    type=str, required=False,
                    help=help)

    parser_list['setsmtp'] = sp
    return 'setsmtp'


def str2bool(str_value):
    if str_value is None:
        return None
    elif str_value == 'True':
        return True
    else:
        return False


def remove_none_values(trap):
    return dict((k, v) for k, v in trap.iteritems() if v is not None)


def get_payload(parser, args):
    """
    #====================================================================================
    # @Method: Encapsulate the request body.
    # @Param: args, payload
    # @Return:
    # @author:
    #====================================================================================
    """
    payload = {}
    if args.ServiceEnabled is not None:
        payload['ServiceEnabled'] = args.ServiceEnabled == 'True'

    if args.TLSEnabled is not None:
        payload['TLSEnabled'] = args.TLSEnabled == 'True'

    if args.AnonymousLoginEnabled is not None:
        payload['AnonymousLoginEnabled'] = args.AnonymousLoginEnabled == 'True'

    if args.ServerAddress is not None:
        payload['ServerAddress'] = args.ServerAddress

    if args.SenderPassword is not None:
        payload['SenderPassword'] = args.SenderPassword

    if args.SenderUserName is not None:
        payload['SenderUserName'] = args.SenderUserName

    if args.SenderUserName is not None:
        payload['EmailSubject'] = args.EmailSubject

    subject_contains = args.EmailSubjectContains
    if subject_contains is not None and len(subject_contains) > 0:
        for keyword in subject_contains:
            if keyword not in EMAIL_SUBJECT_CONTAINS:
                parser.error('argument -ESC: invalid choice: %s (choose from '
                             '%s)' % (keyword, EMAIL_SUBJECT_CONTAINS))
        payload['EmailSubjectContains'] = subject_contains

    if args.AlarmSeverity is not None:
        payload['AlarmSeverity'] = args.AlarmSeverity

    receipts = [remove_none_values({
        "Enabled": str2bool(args.Receipt1Enabled),
        "EmailAddress": args.Receipt1Address,
        "Description": args.Receipt1Description
    }), remove_none_values({
        "Enabled": str2bool(args.Receipt2Enabled),
        "EmailAddress": args.Receipt2Address,
        "Description": args.Receipt2Description
    }), remove_none_values({
        "Enabled": str2bool(args.Receipt3Enabled),
        "EmailAddress": args.Receipt3Address,
        "Description": args.Receipt3Description
    }), remove_none_values({
        "Enabled": str2bool(args.Receipt4Enabled),
        "EmailAddress": args.Receipt4Address,
        "Description": args.Receipt4Description
    })]

    max_len = len(max(receipts, key=len))
    if max_len > 0:
        payload["RecipientAddresses"] = receipts

    if len(payload) == 0:
        parser.error('at least one parameter must be specified')

    return payload


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
            print('%s%s' % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1]))
        else:
            print('         %s%s' % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1]))
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
        print('Failure: you do not have the' + \
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


def setsmtp(client, parser, args):
    """
    #====================================================================================
    # @Method: Set SMTP information processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
     args, parameter list
    # @Return:
    # @author:
    #====================================================================================
    """

    payload = get_payload(parser, args)
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Managers/%s/SmtpService" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

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

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
# PRE_ERR = 'argument -PRE: the length of the parameter \
# exceeds the value range (0 to 67 characters)'
# ALT_ERR = 'argument -ALT: the length of the parameter \
# exceeds the value range (0 to 67 characters)'


def setsnmp_init(parser, parser_list):
    """
    #====================================================================================
    # @Method: Register and obtain SNMP setting commands.
    # @Param: parser, major command argparser
    # @parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    """
    sp = parser.add_parser('setsnmp',
                           help='''set SNMP protocol information''')
    sp.add_argument('-V1', dest='SnmpV1Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''whether SNMP V1 enabled''')
    sp.add_argument('-V2', dest='SnmpV2CEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''whether SNMP V2 enabled''')
    sp.add_argument('-LP', dest='LongPasswordEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help='''whether long password enabled''')

    help = '''whether read&write Community enabled'''
    sp.add_argument('-RWE', dest='RWCommunityEnabled',
                    type=str, required=False,
                    choices=['True', 'False'], help=help)
    help = '''Read Only Community Name'''
    sp.add_argument('-ROC', dest='ReadOnlyCommunity',
                    type=str, required=False, help=help)
    help = '''Read Write Community Name'''
    sp.add_argument('-RWC', dest='ReadWriteCommunity',
                    type=str, required=False, help=help)
    help = '''SNMP V3 authentication protocol'''
    sp.add_argument('-V3AP', dest='SnmpV3AuthProtocol',
                    type=str, required=False,
                    choices=['MD5', 'SHA1'],
                    help=help)
    help = '''SNMP V3 encrypt protocol'''
    sp.add_argument('-V3EP', dest='SnmpV3PrivProtocol',
                    type=str, required=False,
                    choices=['DES', 'AES'],
                    help=help)

    help = '''whether trap notification service enabled'''
    sp.add_argument('-TS', dest='ServiceEnabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    sp.add_argument('-TV', dest='TrapVersion',
                    type=str, required=False,
                    choices=['V1', 'V2C', 'V3'],
                    help='''trap version''')

    help = '''exists user for trap v3'''
    sp.add_argument('-TU', dest='TrapV3User',
                    type=str, required=False,
                    help=help)

    help = '''Trap mode'''
    sp.add_argument('-TM', dest='TrapMode',
                    type=str, required=False,
                    choices=['OID', 'EventCode', 'PreciseAlarm'],
                    help=help)

    help = '''Trap server identity'''
    sp.add_argument('-TSI', dest='TrapServerIdentity',
                    type=str, required=False,
                    choices=['BoardSN', 'ProductAssetTag', 'HostName'],
                    help=help)

    help = '''Trap Community Name'''
    sp.add_argument('-TC', dest='CommunityName',
                    type=str, required=False,
                    help=help)

    help = '''Trap alarm severity'''
    sp.add_argument('-TAS', dest='AlarmSeverity',
                    type=str, required=False,
                    choices=['Critical', 'Major', 'Minor', 'Normal'],
                    help=help)

    help = '''whether Trap server 1 enabled'''
    sp.add_argument('-TS1-Enabled', dest='TrapServer1Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    help = '''whether Trap server 2 enabled'''
    sp.add_argument('-TS2-Enabled', dest='TrapServer2Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    help = '''whether Trap server 3 enabled'''
    sp.add_argument('-TS3-Enabled', dest='TrapServer3Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    help = '''whether Trap server 4 enabled'''
    sp.add_argument('-TS4-Enabled', dest='TrapServer4Enabled',
                    type=str, required=False,
                    choices=['True', 'False'],
                    help=help)

    help = '''Trap server 4 address'''
    sp.add_argument('-TS4-Addr', dest='TrapServer4Address',
                    type=str, required=False,
                    help=help)
    help = '''Trap server 3 address'''
    sp.add_argument('-TS3-Addr', dest='TrapServer3Address',
                    type=str, required=False,
                    help=help)
    help = '''Trap server 2 address'''
    sp.add_argument('-TS2-Addr', dest='TrapServer2Address',
                    type=str, required=False,
                    help=help)
    help = '''Trap server 1 address'''
    sp.add_argument('-TS1-Addr', dest='TrapServer1Address',
                    type=str, required=False,
                    help=help)

    help = '''Trap server 4 port'''
    sp.add_argument('-TS4-Port', dest='TrapServer4Port',
                    type=int, required=False,
                    help=help)
    help = '''Trap server 3 port'''
    sp.add_argument('-TS3-Port', dest='TrapServer3Port',
                    type=int, required=False,
                    help=help)
    help = '''Trap server 2 port'''
    sp.add_argument('-TS2-Port', dest='TrapServer2Port',
                    type=int, required=False,
                    help=help)
    help = '''Trap server 1 port'''
    sp.add_argument('-TS1-Port', dest='TrapServer1Port',
                    type=int, required=False,
                    help=help)

    parser_list['setsnmp'] = sp
    return 'setsnmp'


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
    trap = {
        "ServiceEnabled": str2bool(args.ServiceEnabled),
        "TrapVersion": args.TrapVersion,
        "TrapV3User": args.TrapV3User,
        "TrapMode": args.TrapMode,
        "TrapServerIdentity": args.TrapServerIdentity,
        "CommunityName": args.CommunityName,
        "AlarmSeverity": args.AlarmSeverity,
    }
    trap = remove_none_values(trap)

    servers = [remove_none_values({
        "Enabled": str2bool(args.TrapServer1Enabled),
        "TrapServerAddress": args.TrapServer1Address,
        "TrapServerPort": args.TrapServer1Port
    }), remove_none_values({
        "Enabled": str2bool(args.TrapServer2Enabled),
        "TrapServerAddress": args.TrapServer2Address,
        "TrapServerPort": args.TrapServer2Port
    }), remove_none_values({
        "Enabled": str2bool(args.TrapServer3Enabled),
        "TrapServerAddress": args.TrapServer3Address,
        "TrapServerPort": args.TrapServer3Port
    }), remove_none_values({
        "Enabled": str2bool(args.TrapServer4Enabled),
        "TrapServerAddress": args.TrapServer4Address,
        "TrapServerPort": args.TrapServer4Port
    })]

    max_len = len(max(servers, key=len))
    if max_len > 0:
        trap["TrapServer"] = servers

    payload = {
        "SnmpV1Enabled": str2bool(args.SnmpV1Enabled),
        "SnmpV2CEnabled": str2bool(args.SnmpV2CEnabled),
        "LongPasswordEnabled": str2bool(args.LongPasswordEnabled),
        "RWCommunityEnabled": str2bool(args.RWCommunityEnabled),
        "ReadWriteCommunity": args.ReadWriteCommunity,
        "ReadOnlyCommunity": args.ReadOnlyCommunity,
        "SnmpV3AuthProtocol": args.SnmpV3AuthProtocol,
        "SnmpV3PrivProtocol": args.SnmpV3PrivProtocol,
    }

    payload = remove_none_values(payload)

    if len(trap) > 0:
        payload["SnmpTrapNotification"] = trap

    return payload


def setsnmp(client, parser, args):
    payload = get_payload(parser, args)
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/managers/%s/SnmpService" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

    resp = client.set_resource(url, payload)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        # Determine whether all attributes are set successfully. Query @Message.ExtendedInf
        check_err_info(resp['resource'], resp['status_code'])
    if resp['status_code'] == 400:
        check_err_info(resp['message']['error'], resp['status_code'])
    return resp


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

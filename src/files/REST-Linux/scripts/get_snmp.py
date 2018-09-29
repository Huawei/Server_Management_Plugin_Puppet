# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query SNMP information.
# @command: getsnmp
# @Param: 
# @author: 
# @date: 2018.9.13
#==========================================================================
'''
SNMP_FORMAT = "%-20s: %s"
SHORT_FORMAT = "%-20s: %s"


def getsnmp_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain NTP information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getsnmp', help='''get SMTP Service infomation''')
    parser_list['getsnmp'] = sub_parser
    return 'getsnmp'


def getsnmp(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain SNMP service information command processing functions.
    # @Param: client, RedfishClient object
    # @parser, subcommand argparser. Export error messages when parameters are incorrect.
    # @args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/managers/%s/SnmpService" % slotid
    resp = client.get_resource(url)

    if resp is None:
        return None
    elif resp['status_code'] == 200:
        snmp = resp['resource']
        print("[SNMP]")
        print("-" * 36)
        print(SNMP_FORMAT % ("SnmpV1Enabled", snmp.get("SnmpV1Enabled", None)))
        print(SNMP_FORMAT % ("SnmpV2CEnabled", snmp.get("SnmpV2CEnabled", None)))
        print(SNMP_FORMAT % ("SnmpV3Enabled", snmp.get("SnmpV3Enabled", None)))
        print(SNMP_FORMAT % ("LongPasswordEnabled", snmp.get("LongPasswordEnabled", None)))
        print(SNMP_FORMAT % ("RWCommunityEnabled", snmp.get("RWCommunityEnabled", None)))
        print(SNMP_FORMAT % ("SnmpV3AuthProtocol", snmp.get("SnmpV3AuthProtocol", None)))
        print(SNMP_FORMAT % ("SnmpV3PrivProtocol", snmp.get("SnmpV3PrivProtocol", None)))

        print("\n[SnmpTrapNotification]")
        print("-" * 36)
        trap = snmp.get("SnmpTrapNotification", {})
        print(SNMP_FORMAT % ("ServiceEnabled", trap.get("ServiceEnabled", None)))
        print(SNMP_FORMAT % ("TrapVersion", trap.get("TrapVersion", None)))
        print(SNMP_FORMAT % ("TrapV3User", trap.get("TrapV3User", None)))
        print(SNMP_FORMAT % ("TrapMode", trap.get("TrapMode", None)))
        print(SNMP_FORMAT % ("TrapServerIdentity", trap.get("TrapServerIdentity", None)))
        print(SNMP_FORMAT % ("AlarmSeverity", trap.get("AlarmSeverity", None)))

        headers = ["MemberId", "BobEnabled", "Enabled", "TrapServerAddress", "TrapServerPort"]
        trap_servers = trap.get("TrapServer", [])
        rows = [[r[key] for key in headers] for r in trap_servers]

        if len(trap_servers) > 0:
            print("\n[TrapServers]")
            print("-" * 36)
            for row in rows:
                for idx, column in enumerate(headers):
                    print(SHORT_FORMAT % (column, row[idx]))
                print("-" * 36)

    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    return resp

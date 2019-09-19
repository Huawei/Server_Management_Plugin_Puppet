# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query power supply health information.
# @command: getpsuhealth
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
FORMAT = "%-20s: %s"


def getpsuhealth_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register power supply information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getpsuhealth',
                                   help='get power supply health information')
    parser_list['getpsuhealth'] = sub_parser
    return 'getpsuhealth'


def getpsuhealth(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain power supply command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # date:2017.08.29 11:59
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    slotid_power = client.get_slotid()
    if slotid_power is None:
        return None

    resp = get_summary(client)
    if resp is None:
        return None

    url = "/redfish/v1/Chassis/%s/Power" % slotid_power
    resp = client.get_resource(url)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        powersupplies = resp['resource']['PowerSupplies']
        powersupplies_len = len(powersupplies)
        if powersupplies_len == 0:
            print('no data available for the resource')
            return resp
        print("-" * 40)
        idx = 0
        while idx < powersupplies_len:
            key = powersupplies[idx]
            print(FORMAT % ('Name', key.get('Name', None)))
            print(FORMAT % ('Health', key['Status']['Health']))
            print(FORMAT % ('State', key['Status']['State']))
            print("-" * 40)
            idx += 1
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    return resp


def get_summary(client):
    """
    #====================================================================================
    # @Method: Query system resource CPU information.
    # @Param: client
    # @Return:
    # @author:
    #====================================================================================
    """
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Chassis/%s/" % slotid
    sys_resp = client.get_resource(url)
    if sys_resp is None:
        return None
    if sys_resp['status_code'] == 200:
        oem = sys_resp['resource']['Oem']['Huawei']
        if oem.get('PowerSupplySummary', None):
            print('-' * 40)
            print('[Summary]')
            status = oem['PowerSupplySummary']['Status']
            print(FORMAT % ('HealthRollup', status['HealthRollup']))
    return sys_resp

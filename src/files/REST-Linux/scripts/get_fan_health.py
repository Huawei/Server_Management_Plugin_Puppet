# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query fan information.
# @command: getfanhealth
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
FAN_FORMAT = '%-13s: %s'
SUMMARY_FORMAT = '%-25s: %s'


def getfanhealth_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain fan information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getfanhealth',
                                   help='''get fan information''')
    parser_list['getfanhealth'] = sub_parser

    return 'getfanhealth'


def getfanhealth(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain fan information command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # @Return:
    # @author:
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None or parser is None or args is None:
        return None
    url = "/redfish/v1/Chassis/%s/Thermal" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    elif resp['status_code'] == 200:
        if resp['resource'].get("Oem", None) is not None:
            oem = resp['resource']['Oem']['Huawei']
            if oem.get('FanSummary', None):
                print("-" * 35)
                print('[Summary]')
                status = oem['FanSummary']['Status']
                print(SUMMARY_FORMAT % ('Count', oem['FanSummary']['Count']))
                print(SUMMARY_FORMAT % ('HealthRollup', status['HealthRollup']))
                print('')
                print('[TemperatureSummary]')
                status = oem['TemperatureSummary']['Status']
                print(SUMMARY_FORMAT % (
                'Count', oem['TemperatureSummary']['Count']))
                print(SUMMARY_FORMAT % ('HealthRollup', status['HealthRollup']))

        fan = resp['resource']['Fans']
        fan_len = len(fan)
        print("-" * 35)
        idx = 0
        while idx < fan_len:
            fan_info = fan[idx]
            print(FAN_FORMAT % ("MemberId",
                                fan_info.get("MemberId", None)))
            print(FAN_FORMAT % ("Name", fan_info.get("Name", None)))
            if fan_info.get('Status', None) is not None:
                for status_key in fan_info['Status']:
                    print(FAN_FORMAT % (status_key,
                                        fan_info['Status'][status_key]))
            print("-" * 35)
            idx += 1

    return resp

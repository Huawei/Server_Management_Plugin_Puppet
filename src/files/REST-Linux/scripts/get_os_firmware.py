# coding=utf-8
'''
#=========================================================================
#   @Description:  get os firmware
#
#   @author:
#   @Date:
#=========================================================================
'''


def getosfirmware_init(parser, parser_list):
    '''
    #=========================================================================
    #   @Description:  getosfirmware_init
    #
    #   @author:
    #   @Date:
    #=========================================================================
    '''
    sub_parser = parser.add_parser('getosfw',
                                   help='''get OS firmware that can be upgraded''')
    parser_list['getosfw'] = sub_parser

    return 'getosfw'


def getosfirmware(client, parser, args):
    '''
    #=========================================================================
    #   @Description:  getosfirmware
    #
    #   @author:
    #   @Date:
    #=========================================================================
    '''
    if parser is None and args is None:
        return None

    # Obtain upgradeable firmware collection resources.
    url = "/redfish/v1/Sms/1/UpdateService/FirmwareInventory"
    resp = client.get_resource(url, timeout=20)
    tmp_count = 0
    if resp is None:
        return None
    elif resp['status_code'] == 404:
        print('Failure: failed to obtain iBMA information')
    elif resp['status_code'] == 200:
        firmware_count = len(resp['resource']['Members'])

        if firmware_count > 0:
            print('-' * 40)
            while tmp_count < firmware_count:
                for key in resp['resource']['Members'][tmp_count]:
                    firmware_url = resp['resource']['Members'][tmp_count][key]

                    client.get_os_firmware_or_driver(firmware_url)
                    tmp_count += 1
        else:
            print('There is no firmware to be upgraded on the OS')

    return resp

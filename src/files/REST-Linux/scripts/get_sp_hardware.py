# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  get SP hardware information
#
#   @author:
#   @Date:
#=========================================================================
'''
FORMAT = '%-20s: %s'

FAIL = "Failure: insufficient permission for the file or file name " + \
       "not specified, perform this operation as system administrator/root," + \
       " or specify a file name"
from json import dumps
from os import path


def getsphardware_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  SP query subcommand
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('getsphw',
                                   help='''get SP hardware information''')
    sub_parser.add_argument('-F', dest='file',
                            required=False,
                            help='''the loacl path of get the configuration file''')

    parser_list['getsphw'] = sub_parser

    return 'getsphw'


def getsphardware(client, parser, args):
    '''
    #=====================================================================
    #   @Method: SP query subcommand processing function
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
    #   @Return:
    #   @author:
    #   @date:  2017-11-15 09:04:14
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/SPService/DeviceInfo" % slotid
    resp = client.get_resource(url)
    if resp is None or resp.get("status_code", None) is None:
        return None
    if resp['status_code'] == 200:
        info = resp.get('resource', None)
        if info is None:
            print ('no data available for the resource')
            return resp
        del info["@odata.context"]
        del info["@odata.id"]
        del info["@odata.type"]
        if info.get('Actions', None) is not None:
            del info['Actions']
        del info['Name']
        del info['Id']
        if len(info) == 0:
            print('no data available for the resource')
            return resp
        if args.file is not None:
            if creat_res_file(args.file, info) is True:
                print('Success: successfully completed request')
            else:
                return None
        else:
            print_info(info)

    elif resp['status_code'] == 404:
        print ('Failure: resource was not found')
    elif resp['status_code'] == 500:
        print ("Failure: the request failed due to an internal service error")

    return resp


def creat_res_file(file_path, dict):
    '''
    #=====================================================================
    #   @Method:  Export JSON files.
    #   @Param:   info, SP message dictionary
    #             args, command function parameter
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    # Check the path.
    file_obj = None
    file_dir = path.dirname(file_path)
    if path.exists(file_dir) is not True:
        print("Failure: the path does not exist")
        return False
    if path.isdir(file_path) is True:
        print("Failure: please specify a file name")
        return False
    try:
        file_obj = open(file_path, 'w+')
        json_obj = dumps(dict)
        file_obj.write(json_obj)

    except IOError:
        print (FAIL)
        return False
    finally:
        if file_obj:
            file_obj.close()
    return True


def print_info(info):
    '''
    #=====================================================================
    #   @Method:  print result
    #   @Param:   info，resource
    #
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if info is None:
        print('no data available for the resource')
        return

    for key in info:
        if key == "PCIeCards":
            print ('[PCIeCards]')

            if len(info['PCIeCards']) != 0:
                for pecie_item in info['PCIeCards']:
                    print("-" * 60)
                    print(FORMAT % ('DeviceName', pecie_item['DeviceName']))
                    print(FORMAT % ('DeviceLocator', pecie_item['DeviceLocator']))
                    print(FORMAT % ('Position', pecie_item['Position']))
                    print('')

                    for controller in pecie_item['Controllers']:
                        print('[Controllers]')
                        print(FORMAT % ('Model', controller['Model']))
                        print(FORMAT % ('FirmwareVersion', controller['FirmwareVersion']))
                        print(FORMAT % ('Manufacturer', controller['Manufacturer']))
                        print('')

                        for function in controller['Functions']:
                            print('-' * 40)
                            print(FORMAT % ('VendorId', function['VendorId']))
                            print(FORMAT % ('Description', function['Description']))
                            if "MacAddress" in function:
                                print(FORMAT % ('MacAddress', function['MacAddress']))
                            print(FORMAT % ('DeviceId', function['DeviceId']))
                            print(FORMAT % ('SubsystemId', function['SubsystemId']))
                            print(FORMAT % ('CardType', function['CardType']))
                            print(FORMAT % ('SubsystemVendorId', function['SubsystemVendorId']))
                            print('')

                            print('[BDFNumber]')
                            print(FORMAT % ('BDF', function['BDFNumber']['BDF']))
                            print(FORMAT % ('RootBDF', function['BDFNumber']['RootBDF']))
                        # print('-' * 40)

                print("-" * 60)

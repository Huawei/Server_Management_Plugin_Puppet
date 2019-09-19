# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query the physical disk information.
# @command: get_drive
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
import sys

PF = '{0:40}: {1}'
PF1 = '{0}{1:32}: {2}'
PF2 = '{0}{1:36}: {2}'


def getdriveinfo_init(parser, parser_list):
    '''
    #====================================================================================
    #   @Method:  Script initialization function
    #   @Param:   ；
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getpdisk',
                                   help='''get physical disk information''')
    sub_parser.add_argument('-I', dest='driveid',
                            type=int, required=False,
                            help='''physical disk id''')
    sub_parser.add_argument('-PA', dest='PAGE', choices=['Enabled', \
                               'Disabled'], required=False, \
                               help='''get physical disk information \
                        information paging display''')
    parser_list['getpdisk'] = sub_parser

    return 'getpdisk'


def print_sata_info(oem_info, key):
    '''
    #====================================================================================
    #   @Method:  Export SATA disk SMART information.
    #   @Param:   oem_info smart information, keyword
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    if oem_info is None:
        print(PF.format(key, None))
        return
    print('SATASmartInformation')
    print(PF2.format('    ', 'AttributeRevision',
                     oem_info['AttributeRevision']))
    print(PF2.format('    ', 'AttributeRevisionNumber',
                     oem_info['AttributeRevisionNumber']))
    for key in oem_info:
        if key == 'AttributeRevision' or \
                        key == 'AttributeRevisionNumber':
            continue
        elif key == 'AttributeItemList':
            length = len(oem_info[key])
            if length == 0:
                print(PF.format('    AttributeItemList', None))
                continue
            print('    AttributeItemList')
            index = 0
            while index < length:
                for key1 in oem_info[key][index]:
                    value = oem_info[key][index][key1]
                    print(PF1.format('        ', key1, value))
                index += 1
                if index != length:
                    print('%s%s' % ('        ', '-' * 33))
            continue
        print(PF.format(key, oem_info[key]))


def print_drive_oem_info(oem_info):
    '''
    #====================================================================================
    #   @Method:  Export physical disk OEM information.
    #   @Param:   oem_info OEM information
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    for key in oem_info:
        if key == 'Position' or key == 'DriveID' or \
                        key == 'SASSmartInformation' or key == 'SATASmartInformation':
            continue
        elif key == 'SpareforLogicalDrives':
            if oem_info[key]:
                volume_list = []
                get_vloume_list(oem_info[key], volume_list)
                print(PF.format(key, ','.join(volume_list)))
            else:
                print(PF.format(key, None))
            continue

        elif key == 'SASAddress':
            if oem_info[key]:
                print(PF.format(key, ','.join(oem_info[key])))
            else:
                print(PF.format(key, None))
            continue

        print(PF.format(key, oem_info[key]))


def get_vloume_list(volumeinfo, volume_list):
    '''
    #====================================================================================
    #   @Method:  Obtain logical disk information.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    length = len(volumeinfo)
    index = 0
    while index < length:
        url = volumeinfo[index]['@odata.id']
        obj = url.split(r'/')[6] + '-' + url.split(r'/')[8]
        volume_list.append(obj)
        index += 1


def print_smart_info(oem_info):
    '''
    #====================================================================================
    #   @Method:  Obtain SMART information.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    if oem_info['SASSmartInformation'] is None:
        print(PF.format('SASSmartInformation', None))
    else:
        print('SASSmartInformation')
        for key in oem_info['SASSmartInformation']:
            print(PF2.format('    ', key, oem_info['SASSmartInformation'][key]))

    if oem_info['SATASmartInformation'] is None:
        print(PF.format('SATASmartInformation', None))
    else:
        print_sata_info(oem_info['SATASmartInformation'],
                        'SATASmartInformation')


def get_drive_info(client, drive_uri, flag):
    '''
    #====================================================================================
    #   @Method:  Obtain physical disk information.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    drive_resp = client.get_resource(drive_uri)
    if drive_resp is None or drive_resp['status_code'] != 200:
        return drive_resp

    drive_info = drive_resp['resource']
    oem_info = drive_info['Oem']['Huawei']
    if flag == 0:
        print('-' * 50)
    # Display the ID. Name Container
    print(PF.format('Id', oem_info['DriveID']))
    print(PF.format('Name', drive_info['Name']))
    print(PF.format('Position', oem_info['Position']))
    print('')
    print('[Status]')
    print(PF.format('Health', drive_info['Status']['Health']))
    print(PF.format('State', drive_info['Status']['State']))
    print('')
    print(PF.format('Manufacturer', drive_info['Manufacturer']))
    print(PF.format('Model', drive_info['Model']))
    print(PF.format('Protocol', drive_info['Protocol']))
    print(PF.format('FailurePredicted',
                    drive_info['FailurePredicted']))
    print(PF.format('CapacityBytes', drive_info['CapacityBytes']))
    print(PF.format('HotspareType', drive_info['HotspareType']))
    print(PF.format('IndicatorLED', drive_info['IndicatorLED']))
    print(PF.format('PredictedMediaLifeLeftPercent',
                    drive_info['PredictedMediaLifeLeftPercent']))
    print(PF.format('MediaType', drive_info['MediaType']))
    for key in drive_info:
        if key == 'Id' or key == '@odata.context' or \
                        key == '@odata.id' or key == '@odata.type' or \
                        key == 'Location' or key == 'MediaType' or \
                        key == 'Name' or key == 'Status' or \
                        key == 'Manufacturer' or key == 'CapacityBytes' or \
                        key == 'Protocol' or key == 'FailurePredicted' or \
                        key == 'HotspareType' or key == 'IndicatorLED' or \
                        key == 'Model' or key == 'Actions' or \
                        key == 'PredictedMediaLifeLeftPercent':
            continue

        elif key == 'Oem':
            print_drive_oem_info(oem_info)
            continue

        elif key == 'Links':
            if drive_info[key]['Volumes']:
                volume_list = []
                get_vloume_list(drive_info[key]['Volumes'], volume_list)
                print(PF.format('Volumes', ','.join(volume_list)))

            else:
                print(PF.format('Volumes', None))
            continue

        print(PF.format(key, drive_info[key]))
    print_smart_info(oem_info)
    print('-' * 50)
    return drive_resp


def check_drive_id_effective(client, drives_list, driveid, url, id_list):
    '''
    #====================================================================================
    #   @Method:  Check the physical disk URL.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    index = 0
    while index < len(drives_list):
        resp = client.get_resource(drives_list[index])
        if resp is None or resp['status_code'] != 200:
            return False

        drive_id = resp['resource']['Oem']['Huawei']['DriveID']
        id_list.append(str(drive_id))
        if driveid == drive_id:
            url.append(drives_list[index])
            return True
        index += 1
    return False


def get_drives_array(client, slotid, drives_list):
    '''
    #====================================================================================
    #   @Method:  Obtain the physical disk array.
    #   @Param:   client, RedfishClient client, slotid, slot information
                    drives_list physical disk list
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    chassis_url = "/redfish/v1/Chassis/" + slotid
    resp = client.get_resource(chassis_url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp
    if resp['resource']['Links'].get('Drives') is None:
        print('Failure: resource was not found')
        return resp
    drive_array = resp['resource']['Links']['Drives']
    if drive_array:
        index = 0
        length = len(drive_array)
        while index < length:
            url = drive_array[index]['@odata.id']
            # SD cards and SSD cards are queried.
            if url.find('SD') > 0 or url.find('SSD') > 0:
                index += 1
                continue
            drives_list.append(url)
            index += 1
    else:
        print('Failure: resource was not found')
        return resp

    return resp


def getdriveinfo(client, parser, args):
    '''
    #====================================================================================
    #   @Method:  Set physical disk attribute processing functions.
    #   @Param:   client, RedfishClient object
                  parser, subcommand argparser. Export error messages when parameters are incorrect.
                  args, parameter list
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None

    # Obtain the physical disk URL list.
    drives_list = []
    resp = get_drives_array(client, slotid, drives_list)
    if resp is None or resp['status_code'] != 200:
        return resp

    if not drives_list:
        print('Failure: resource was not found')
        sys.exit(148)
        # Obtain information of all physical disks.
    if args.driveid is None:
        index = 0
        list_str = sys.version
        while index < len(drives_list):
            get_drive_info(client, drives_list[index], index)

            if args.PAGE == "Enabled":
                # Control the input.
                if len(drives_list) == 1:
                    index += 1
                    continue
                # Differentiated versions
                print("Input 'q' quit:")
                sys.stdout.flush()
                if list_str[0] != '2':
                    strtemp = input("")  # pylint: disable=W0141
                else:
                    strtemp = raw_input("")
                tmp = strtemp.replace('\r', '')
                if tmp == 'q':
                    return resp
            index += 1
    # Obtain the information of a single physical resource.
    else:
        url = []
        id_list = []
        ret = check_drive_id_effective(client, drives_list,
                                       args.driveid, url, id_list)
        if ret is True and len(url) != 0:
            resp = get_drive_info(client, url[0], 0)
        else:
            parser.error("the value of -I parameter is invalid, choose from "
                         '<' + ','.join(id_list) + '>')
    return resp

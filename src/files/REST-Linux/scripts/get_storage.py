# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query storage information.
# @command: get_storage
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
import sys

PF = '{0}{1:26}: {2}'
PF1 = '{0}{1:26}'
PF2 = '{0:30}: {1}'


def getstorage_init(parser, parser_list):
    '''
    #====================================================================================
    #   @Method:  Register and obtain storage information subcommands.
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getraid',
                                   help='''get raid information''')
    sub_parser.add_argument('-CI', dest='controllerid',
                            type=int, required=False,
                            help='''controller id''')
    sub_parser.add_argument('-LI', dest='logicaldriveid',
                            type=int, required=False,
                            help='''virtual disk id''')
    sub_parser.add_argument('-PA', dest='PAGE', choices=['Enabled', \
                               'Disabled'], required=False, \
                               help='''get raid information \
                        information paging display''')
    parser_list['getraid'] = sub_parser

    return 'getraid'


def check_span_get_drive_list(client, span_info, all_list):
    '''
    #====================================================================================
    #   @Method:  View the logical disk span, and obtain the physical disk list.
    #   @Param:   client：
    #             span_info: span object
    #             all_list: physical disk list
    #   @Return:  resp
    #   @author:
    #====================================================================================
    '''
    length = len(span_info)
    index = 0
    while index < length:
        drive_list = []
        get_drive_id_list(client, span_info[index]['Drives'],
                          drive_list, all_list)
        span_info[index]['Drives'] = drive_list
        index += 1


def get_drive_id_list(client, drive_info, drive_list, all_list):
    '''
    #====================================================================================
    #   @Method:  Obtain the physical disk list.
    #   @Param:   client RedfishClient object drive_info Physical disk URI collection
    #              drive_list  Collection of some physical disk IDs all_list Collection of all physical disk IDs
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    if drive_info:
        index = 0
        drive_length = len(drive_info)
        while index < drive_length:
            url = drive_info[index]['@odata.id']
            drive_resp = client.get_resource(url)
            if drive_resp is None:
                index += 1
                continue
            if drive_resp['status_code'] == 200:
                huawei = drive_resp['resource']['Oem']['Huawei']
                drive_id = str(huawei['DriveID'])
                drive_list.append(drive_id)
                if all_list is not None:
                    all_list.append(drive_id)
            index += 1


def get_vloume_list(volumeinfo, volume_list):
    '''
    #====================================================================================
    #   @Method:  Obtain the logical disk list.
    #   @Param:   volumeinfo Logical disk URI collection
    #             volume_list Logical disk list
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    if volumeinfo:
        length = len(volumeinfo)
        index = 0
        while index < length:
            url = volumeinfo[index]['@odata.id']
            obj = url.split(r'/')[6] + '-' + url.split(r'/')[8]
            volume_list.append(obj)
            index += 1
    return


def print_volumes_oem(oem_info, str_null):
    '''
    #====================================================================================
    #   @Method:  Export logical disk OEM information.
    #   @Param:   oem_info OEM attribute list
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    print(PF.format(str_null, 'DefaultReadPolicy',
                    oem_info['DefaultReadPolicy']))
    print(PF.format(str_null, 'DefaultWritePolicy',
                    oem_info['DefaultWritePolicy']))
    print(PF.format(str_null, 'DefaultCachePolicy',
                    oem_info['DefaultCachePolicy']))
    print(PF.format(str_null, 'CurrentReadPolicy',
                    oem_info['CurrentReadPolicy']))
    print(PF.format(str_null, 'CurrentWritePolicy',
                    oem_info['CurrentWritePolicy']))
    print(PF.format(str_null, 'CurrentCachePolicy',
                    oem_info['CurrentCachePolicy']))
    print(PF.format(str_null, 'AccessPolicy', oem_info['AccessPolicy']))
    for key in oem_info:
        if 'AssociatedCacheCadeVolume' == key:
            if oem_info[key]:
                volume_list = []
                get_vloume_list(oem_info[key], volume_list)
                print(PF.format(str_null, key, ','.join(volume_list)))
            else:
                print(PF.format(str_null, key, None))
            continue

        elif 'Spans' == key or 'SpanNumber' == key or \
                        'NumDrivePerSpan' == key or 'AccessPolicy' == key or \
                        'DefaultReadPolicy' == key or 'DefaultWritePolicy' == key or \
                        'DefaultCachePolicy' == key or 'CurrentReadPolicy' == key or \
                        'CurrentWritePolicy' == key or 'CurrentCachePolicy' == key:
            continue

        else:
            print(PF.format(str_null, key, oem_info[key]))


def getvolumesinfo(client, volumes_uri, flag):
    '''
    #====================================================================================
    #   @Method:  Export logical disk information.
    #   @Param:  client: RedfishClient object
    #            volumes_uri Logical disk URI flag tag
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    volume_resp = client.get_resource(volumes_uri)
    if volume_resp is None or volume_resp['status_code'] != 200:
        return volume_resp

    volume_info = volume_resp['resource']
    if flag:
        str_null = '    '
    else:
        print ('-' * 50)
        str_null = ''
    volumes = volumes_uri.split(r'/')[8]
    print(PF.format(str_null, 'Id', volumes[-1]))
    print(PF.format(str_null, 'Name', volume_info['Name']))
    print('')
    print(PF1.format(str_null, '[Status]'))
    print(PF.format(str_null, 'Health', volume_info['Status']['Health']))
    print(PF.format(str_null, 'State', volume_info['Status']['State']))
    print('')
    for key in volume_info:
        if '@odata.context' == key or '@odata.id' == key or \
                        '@odata.type' == key or 'Links' == key or 'Id' == key or \
                        'Name' == key or key == 'Status'or key == 'Actions':
            continue

        elif 'Oem' == key:
            print_volumes_oem(volume_info['Oem']['Huawei'], str_null)
            continue

        else:
            print(PF.format(str_null, key, volume_info[key]))

    all_list = []
    check_span_get_drive_list(client, volume_info['Oem']['Huawei']['Spans'],
                              all_list)
    print(PF.format(str_null, 'Drives', ','.join(all_list)))
    # Display span information.
    spannumber = volume_info['Oem']['Huawei']['SpanNumber']
    if spannumber > 1:
        print(PF.format(str_null, 'SpanNumber', spannumber))
        print(PF.format(str_null, 'NumDrivePerSpan',
                        volume_info['Oem']['Huawei']['NumDrivePerSpan']))
        print(PF1.format(str_null, '[Spans]'))
        index = 0
        while index < len(volume_info['Oem']['Huawei']['Spans']):
            print(PF.format(str_null, 'SpanName',
                            volume_info['Oem']['Huawei']['Spans'][index]['SpanName']))
            print(PF.format(str_null, 'Drives',
                            ','.join(volume_info['Oem']['Huawei']['Spans'][index]['Drives'])))
            index += 1
    print(PF1.format(str_null, '-' * 50))
    return volume_resp


def controller_oem_info(oem_info):
    '''
    #====================================================================================
    #   @Method:  Export OEM information.
    #   @Param:   oem_info OEM attribute list
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    print(PF2.format('SASAddress', oem_info['SASAddress']))
    print(PF2.format('ConfigurationVersion', oem_info['ConfigurationVersion']))
    print(PF2.format('MaintainPDFailHistory',
                     oem_info['MaintainPDFailHistory']))
    print(PF2.format('CopyBackState', oem_info['CopyBackState']))
    print(PF2.format('SmarterCopyBackState', oem_info['SmarterCopyBackState']))
    print(PF2.format('JBODState', oem_info['JBODState']))
    print(PF2.format('MinStripeSizeBytes', oem_info['MinStripeSizeBytes']))
    print(PF2.format('MaxStripeSizeBytes', oem_info['MaxStripeSizeBytes']))

    for key in oem_info:
        if 'PHYStatus' == key or 'SASAddress' == key or \
                        'ConfigurationVersion' == key or 'AssociatedCard' == key or \
                        'MaintainPDFailHistory' == key or 'CopyBackState' == key or \
                        'SmarterCopyBackState' == key or 'JBODState' == key or \
                        'DDRECCCount' == key or 'MinStripeSizeBytes' == key or \
                        'MaxStripeSizeBytes' == key or 'CapacitanceStatus' == key:
            continue

        elif 'SupportedRAIDLevels' == key:
            if oem_info[key]:
                print(PF2.format(key, ','.join(oem_info[key])))
            else:
                print(PF2.format(key, None))
            continue

        elif 'DriverInfo' == key:
            print(PF2.format('DriverName',
                             oem_info['DriverInfo']['DriverName']))
            print(PF2.format('DriverVersion',
                             oem_info['DriverInfo']['DriverVersion']))
            continue
        print (PF2.format(key, oem_info[key]))

    print(PF2.format('DDRECCCount', oem_info['DDRECCCount']))
    print('')
    if oem_info['CapacitanceStatus']:
        print ('[CapacitanceStatus]')
        print(PF2.format('Health', oem_info['CapacitanceStatus']['Health']))
        print(PF2.format('State', oem_info['CapacitanceStatus']['State']))
    else:
        print(PF2.format('[CapacitanceStatus]', None))
    print('')


def print_ctrl_info(controller):
    '''
    #====================================================================================
    #   @Method:  Export controller information.
    #   @Param:   controller controller dictionary 
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    for key in controller:
        if '@odata.id' == key or 'MemberId' == key or \
                        'Description' == key or 'Name' == key or 'Status' == key or \
                        'SpeedGbps' == key or 'FirmwareVersion' == key or \
                        'Manufacturer' == key or 'Model' == key:
            continue

        elif 'SupportedDeviceProtocols' == key:
            if controller[key]:
                print(PF2.format(key, ','.join(controller[key])))
            else:
                print(PF2.format(key, None))
            continue

        elif 'Oem' == key:
            controller_oem_info(controller['Oem']['Huawei'])
            continue

        else:
            print (PF2.format(key, controller[key]))


# Obtain controller information.
def getcontrollerinfo(client, controller_uri, flag, page_ctl):
    '''
    #====================================================================================
    #   @Method:  Obtain the controller.
    #   @Param:   client, RedfishClient object; controller_uri: controller URL 
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    # Obtain the controller information.
    ctrl_resp = client.get_resource(controller_uri)
    # If the required information is not obtained successfully, the returned value is None.
    if ctrl_resp is None or ctrl_resp['status_code'] != 200:
        return ctrl_resp

    controller = ctrl_resp['resource']['StorageControllers'][0]
    # Export controller information.
    storage = controller_uri.split(r'/')[6]
    if flag == 0:
        print ('-' * 60)
    print(PF2.format('Id', storage[-1]))
    print(PF2.format('Name', controller['Name']))
    print('')
    print('[Status]')
    print(PF2.format('Health', controller['Status']['Health']))
    print(PF2.format('State', controller['Status']['State']))
    print('')
    print(PF2.format('SpeedGbps', controller['SpeedGbps']))
    print(PF2.format('FirmwareVersion', controller['FirmwareVersion']))
    print(PF2.format('Manufacturer', controller['Manufacturer']))
    print(PF2.format('Model', controller['Model']))
    print_ctrl_info(controller)
    # Export logical disk information.
    volumes_uri = ctrl_resp['resource']['Volumes']['@odata.id']
    volumes_resp = client.get_resource(volumes_uri)
    if volumes_resp is None or volumes_resp['status_code'] != 200:
        return volumes_resp

    if volumes_resp['resource']['Members']:
        volumes_length = len(volumes_resp['resource']['Members'])
        print('Volumes')
        index = 0
        list_strs = sys.version
        while index < volumes_length:
            volumes_index = volumes_resp['resource']['Members'][index]
            volumes_url = volumes_index['@odata.id']
            getvolumesinfo(client, volumes_url, True)
            if page_ctl == "Enabled":
                if 1 == volumes_length:
                    index += 1
                    continue
                print("Input 'q' quit:")
                sys.stdout.flush()
                if list_strs[0] != '2':
                    strtemp = input("")  # pylint: disable=W0141
                else:
                    strtemp = raw_input("")
                tmp = strtemp.replace('\r', '')
                if 'q' == tmp:
                    return ctrl_resp
            index += 1
    else:
        print(PF2.format('Volumes', None))

    if ctrl_resp['resource']['Drives']:
        drive_list = []
        get_drive_id_list(client, ctrl_resp['resource']['Drives'],
                          drive_list, None)
        print(PF2.format('Drives', ','.join(drive_list)))
    else:
        print(PF2.format('Drives', None))

    print ('-' * 60)
    return ctrl_resp


def get_storage_info(args, resp, client):
    '''
    #====================================================================================
    #   @Method:  Obtain complete storage information.
    #   @Param:   client, RedfishClient object, slotid: environment slot information
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    # No storage device exists in the environment.
    if not resp['resource']['Members']:
        print('Failure: resource was not found')
        sys.exit(148)
    # RAID controller information
    storage_array = resp['resource']['Members']
    index = 0
    array_len = len(storage_array)

    list_str = sys.version
    while index < array_len:
        # Update controller information.
        url = resp['resource']['Members'][index]['@odata.id']

        # Filter the SD controller environment.
        if url.find("RAIDStorage") > 0:
            getcontrollerinfo(client, url, index, args.PAGE)

            if args.PAGE == "Enabled":
                if 1 == array_len:
                    index += 1
                    continue
                print("Input 'q' quit:")
                sys.stdout.flush()
                if list_str[0] != '2':
                    strtemp = input("")  # pylint: disable=W0141
                else:
                    strtemp = raw_input("")
                tmp = strtemp.replace('\r', '')
                if 'q' == tmp:
                    return
        index += 1
    return resp


def get_specify_volume_info(args, client, systems, raidstorage, parser):
    '''
    #====================================================================================
    #   @Method:  Obtain specified logical disk information.
    #   @Param:   client, RedfishClient object, slotid: environment slot information
    #   @Return:  resp
    #   @author: 
    #====================================================================================
    '''
    raid_url = systems + raidstorage + str(args.controllerid)
    resp = client.get_resource(raid_url)
    if resp is None:
        return resp
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            parser.error("the value of -CI parameter is invalid")
        return resp
    volumes = "/volumes/logicaldrive" + str(args.logicaldriveid)
    url = systems + raidstorage + str(args.controllerid) + volumes
    resp = getvolumesinfo(client, url, False)
    if resp is None:
        return resp
    elif resp['status_code'] == 404:
        parser.error("the value of -LI parameter is invalid")
    return resp


def get_specify_contrl_info(client, url, parser, page):
    '''
    #====================================================================================
    #   @Method:  Obtain specified controller information.
    #   @Param:   client, RedfishClient object, url: specified URL
    #   @Return:  resp
    #   @author:
    #   @modify: 2018.11.30 DTS2018113004239：getcontrollerinfo（）adds the fourth parameter page.
    #====================================================================================
    '''
    resp = getcontrollerinfo(client, url, 0, page)
    if resp is None:
        return resp
    elif resp['status_code'] == 404:
        # No RAID controller exists in the environment.
        parser.error("the value of -CI parameter is invalid")
    return resp


def check_storages(client, systems):
    '''
    #=================================================================
    #   @Method:  Check before the configuration.
    #   @Param:   parser, major command argparser
    #             parser_list, save subcommand parser list
    #   @Return:
    #   @author:  
    #=================================================================
    '''
    url = systems + "/Storages"
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

        # Check whether the controller URL exists and whether the version is an earlier version.
    elif resp['status_code'] == 200:
        flag = False
        if resp['resource']['Members@odata.count'] == 0:
            print('Failure: resource was not found')
            sys.exit(148)
        for i in range(0, len(resp['resource']['Members'])):
            url = resp['resource']['Members'][i]['@odata.id']
            if url.find("RAIDStorage") > 0:
                flag = True
                break
        if not flag:
            print('Failure: resource was not found')
            sys.exit(148)
    return resp


# Obtain storage information.
def getstorage(client, parser, args):
    '''
    #====================================================================================
    #   @Method:  Obtain storage information subcommand processing functions.
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
    # Determine whether a storage system exists.
    systems = "/redfish/v1/Systems/" + slotid
    resp = check_storages(client, systems)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        return resp

    raidstorage = "/storages/raidstorage"
    if args.controllerid is not None and args.logicaldriveid is None:
        url = systems + raidstorage + str(args.controllerid)
        return get_specify_contrl_info(client, url, parser, args.PAGE)

    # To query logical disk information, you must enter the controller ID.
    elif args.controllerid is None and args.logicaldriveid is not None:
        parser.error('the -CI parameter must be specified')

    # Query specified logical disk information.
    elif args.controllerid is not None and args.logicaldriveid is not None:
        return get_specify_volume_info(args, client,
                                       systems, raidstorage, parser)

    return get_storage_info(args, resp, client)

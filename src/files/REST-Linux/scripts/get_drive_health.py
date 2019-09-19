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

PF = '{0:15}: {1}'
PF1 = '{0}{1:32}: {2}'
PF2 = '{0}{1:36}: {2}'


def getdrivehealth_init(parser, parser_list):
    """
    #====================================================================================
    #   @Method:  Script initialization function
    #   @Param:   ；
    #   @Return:
    #   @author:
    #====================================================================================
    """
    sub_parser = parser.add_parser('getpdiskhealth',
                                   help='''get physical disk information''')
    sub_parser.add_argument('-I', dest='driveid',
                            type=int, required=False,
                            help='''physical disk id''')
    sub_parser.add_argument('-PA', dest='PAGE', choices=['Enabled', \
                                                         'Disabled'], required=False, \
                            help='''get physical disk information \
                        information paging display''')
    parser_list['getpdiskhealth'] = sub_parser
    return 'getpdiskhealth'


def get_drive_info(client, drive_uri, flag):
    """
    #====================================================================================
    #   @Method:  Obtain physical disk information.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    """
    drive_resp = client.get_resource(drive_uri)
    if drive_resp is None or drive_resp['status_code'] != 200:
        return drive_resp

    drive_info = drive_resp['resource']
    oem_info = drive_info['Oem']['Huawei']
    if flag == 0:
        print('-' * 28)
    # Display the ID. Name Container
    print(PF.format('Id', oem_info['DriveID']))
    print(PF.format('Name', drive_info['Name']))
    print(PF.format('Health', drive_info['Status']['Health']))
    print(PF.format('State', drive_info['Status']['State']))
    print('-' * 28)
    return drive_resp


def get_drives_array(client, slotid, drives_list):
    """
    #====================================================================================
    #   @Method:  Obtain the physical disk array.
    #   @Param:   client, RedfishClient client, slotid, slot information
                    drives_list physical disk list
    #   @Return:
    #   @author:
    #====================================================================================
    """
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


def getdrivehealth(client, parser, args):
    """
    #====================================================================================
    #   @Method:  Set physical disk attribute processing functions.
    #   @Param:   client, RedfishClient object
                  parser, subcommand argparser. Export error messages when parameters are incorrect.
                  args, parameter list
    #   @Return:
    #   @author:
    #====================================================================================
    """
    slotid = client.get_slotid()
    if slotid is None:
        return None

    resp = get_summary(client)
    if resp is None:
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
    index = 0
    while index < len(drives_list):
        get_drive_info(client, drives_list[index], index)
        index += 1

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
        if oem.get('DriveSummary', None):
            print('-' * 28)
            print('[Summary]')
            status = oem['DriveSummary']['Status']
            print(PF.format('HealthRollup', status['HealthRollup']))
    return sys_resp

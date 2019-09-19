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
PF2 = '{0:15}: {1}'


def getstoragehealth_init(parser, parser_list):
    '''
    #====================================================================================
    #   @Method:  Register and obtain storage information subcommands.
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getraidhealth',
                                   help='''get raid information''')
    parser_list['getraidhealth'] = sub_parser
    return 'getraidhealth'


# Obtain controller information.
def getcontrollerinfo(client, controller_uri, flag):
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
        print ('-' * 40)
    print(PF2.format('Id', storage[-1]))
    print(PF2.format('Name', controller['Name']))
    print(PF2.format('Health', controller['Status']['Health']))
    print(PF2.format('State', controller['Status']['State']))

    oem = controller['Oem']['Huawei']
    if oem['CapacitanceStatus']:
        print ('[CapacitanceStatus]')
        print(PF2.format('Health', oem['CapacitanceStatus']['Health']))
        print(PF2.format('State', oem['CapacitanceStatus']['State']))
    else:
        print(PF2.format('CapacitanceStatus', None))
    print ('-' * 40)
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
            getcontrollerinfo(client, url, index)
        index += 1
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
def getstoragehealth(client, parser, args):
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

    resp = get_summary(client)
    if resp is None:
        return None

    # Determine whether a storage system exists.
    systems = "/redfish/v1/Systems/" + slotid
    resp = check_storages(client, systems)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        return resp

    return get_storage_info(args, resp, client)


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
    url = "/redfish/v1/Systems/%s/" % slotid
    sys_resp = client.get_resource(url)
    if sys_resp is None:
        return None
    if sys_resp['status_code'] == 200:
        oem = sys_resp['resource']['Oem']['Huawei']
        if oem.get('StorageSummary', None):
            print('-' * 40)
            print('[Summary]')
            status = oem['StorageSummary']['Status']
            print(PF2.format('HealthRollup', status['HealthRollup']))
    return sys_resp

# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query memory information.
# @command: getmemory
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
MEM_FORMAT = '%-25s: %s'


def getmemory_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method:  Register and obtain memory commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getmemory',
                                   help='''get memory information''')
    parser_list['getmemory'] = sub_parser

    return 'getmemory'


def get_memory(client, memory_url):
    '''
    #====================================================================================
    # @Method: Query specified memory information.
    # @Param: client，memory_url
    # @Return:
    # @author: 
    #====================================================================================
    '''
    memory_resp = client.get_resource(memory_url)
    if memory_resp is None:
        return None
    if memory_resp['status_code'] == 200:
        print('-' * 50)
        key = memory_resp['resource']
        print((MEM_FORMAT) % ('DeviceLocator', \
                              key.get('DeviceLocator', None)))
        print((MEM_FORMAT) % ('CapacityMiB', \
                              key.get('CapacityMiB', None)))
        print((MEM_FORMAT) % ('Manufacturer', \
                              key.get('Manufacturer', None)))
        print((MEM_FORMAT) % ('OperatingSpeedMhz', \
                              key.get('OperatingSpeedMhz', None)))
        print((MEM_FORMAT) % ('SerialNumber', \
                              key.get('SerialNumber', None)))
        print((MEM_FORMAT) % ('MemoryDeviceType', \
                              key.get('MemoryDeviceType', None)))
        print((MEM_FORMAT) % ('DataWidthBits', \
                              key.get('DataWidthBits', None)))
        print((MEM_FORMAT) % ('RankCount', \
                              key.get('RankCount', None)))
        print((MEM_FORMAT) % ('PartNumber', \
                              key.get('PartNumber', None)))
        if key.get('Oem', None) is not None:
            for oem_key in key['Oem']['Huawei']:
                print((MEM_FORMAT) % (oem_key, key['Oem']['Huawei'][oem_key]))
        print ('\n[MemoryLocation]')
        memory_socket = key.get('MemoryLocation', None)
        if memory_socket is not None:
            print((MEM_FORMAT) % ("Socket", \
                                  memory_socket.get("Socket", None)))
            print((MEM_FORMAT) % ("Controller", \
                                  memory_socket.get("Controller", None)))
            print((MEM_FORMAT) % ("Channel", \
                                  memory_socket.get("Channel", None)))
            print((MEM_FORMAT) % ("Slot", \
                                  memory_socket.get("Slot", None)))
        print ('\n[Status]')
        if key.get('Status', None) is not None:
            for status_key in key['Status']:
                print((MEM_FORMAT) % (status_key, key['Status'][status_key]))
    return memory_resp


def get_memory_collection(client):
    '''
    #====================================================================================
    # @Method: Query memory collection information.
    # @Param: client
    # @Return:
    # @author: 
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Systems/%s/Memory/" % slotid
    collection_resp = client.get_resource(url)
    if collection_resp is None:
        return None
    if collection_resp['status_code'] != 200:
        return collection_resp
    count = 0
    while count < collection_resp['resource']['Members@odata.count']:
        get_resp = get_memory(client,
                              collection_resp['resource']['Members'][count]['@odata.id'])
        if get_resp['status_code'] != 200:
            return get_resp
        count += 1
    return collection_resp


def get_memory_sys(client):
    '''
    #====================================================================================
    # @Method: Query system resource memory information.
    # @Param: client
    # @date: 2017.8.1 11:09
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Systems/%s/" % slotid
    sys_resp = client.get_resource(url)
    if sys_resp is None:
        return None
    if sys_resp['status_code'] == 200:
        print('-' * 50)
        print((MEM_FORMAT) % ('TotalSystemMemoryGiB',
                              sys_resp['resource']['MemorySummary']['TotalSystemMemoryGiB']))
        print('\n[Status]')
        print((MEM_FORMAT) % ('HealthRollup',
                              sys_resp['resource']['MemorySummary']['Status']['HealthRollup']))
    return sys_resp


def getmemory(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain memory information command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    resp = get_memory_sys(client)
    if resp is None:
        return None
    if resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp
    resp = get_memory_collection(client)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        print('-' * 50)
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
        return resp
    return resp

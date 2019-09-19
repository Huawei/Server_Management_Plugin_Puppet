# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query CPU information.
# @command: getprocessor
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
PRO_FORMAT = '%-25s: %s'


def getprocessor_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain CPU information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getcpu',
                                   help='''get processor information''')
    parser_list['getcpu'] = sub_parser

    return 'getcpu'


def get_processor(client, processor_url):
    '''
    #====================================================================================
    # @Method: Query specified memory information.
    # @Param: client
    # @Return:
    # @author: 
    #====================================================================================
    '''
    processor_resp = client.get_resource(processor_url)
    if processor_resp is None:
        return None
    if processor_resp['status_code'] == 200:
        print ('-' * 50)
        key = processor_resp['resource']
        print((PRO_FORMAT) % ('Id', key.get("Id", None)))
        print((PRO_FORMAT) % ('Name', key.get('Name', None)))
        if key.get("Oem", None) is not None:
            print((PRO_FORMAT) % ("Position", \
                                  key['Oem']['Huawei'].get("Position", None)))
            for oem_key in key['Oem']['Huawei']:
                if oem_key == "Position":
                    continue
                print((PRO_FORMAT) % (oem_key,
                                      key['Oem']['Huawei'][oem_key]))
        print((PRO_FORMAT) % ('ProcessorType',
                              key.get('ProcessorType', None)))
        print((PRO_FORMAT) % ('ProcessorArchitecture',
                              key.get('ProcessorArchitecture', None)))
        print((PRO_FORMAT) % ('InstructionSet',
                              key.get('InstructionSet', None)))
        print((PRO_FORMAT) % ('Manufacturer', \
                              key.get('Manufacturer', None)))
        print((PRO_FORMAT) % ('Model', key.get('Model', None)))
        print((PRO_FORMAT) % ('MaxSpeedMHz',
                              key.get('MaxSpeedMHz', None)))
        print((PRO_FORMAT) % ('TotalCores',
                              key.get('TotalCores', None)))
        print((PRO_FORMAT) % ('TotalThreads',
                              key.get('TotalThreads', None)))
        print((PRO_FORMAT) % ('Socket', key.get('Socket', None)))
        print('\n[Status]')
        if key.get("Status", None) is not None:
            print((PRO_FORMAT) % ('Health',
                                  key['Status'].get('Health', None)))
            print((PRO_FORMAT) % ('State',
                                  key['Status'].get('State', None)))

        print('\n[ProcessorId]')
        if key.get("ProcessorId", None) is not None:
            print((PRO_FORMAT) % ('IdentificationRegisters',
                                  key['ProcessorId'].get('IdentificationRegisters', None)))

    return processor_resp


def get_processor_collection(client):
    '''
    #====================================================================================
    # @Method: Query CPU collection information.
    # @Param: client
    # @Return:
    # @author: 
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/Systems/%s/Processors/" % slotid
    collection_resp = client.get_resource(url)
    if collection_resp['status_code'] != 200:
        return collection_resp
    count = 0
    while count < collection_resp['resource']['Members@odata.count']:
        get_resp = get_processor(client,
                                 collection_resp['resource']['Members'][count]['@odata.id'])
        if get_resp['status_code'] != 200:
            return get_resp
        count += 1
    return get_resp


def get_summary_sys(client):
    '''
    #====================================================================================
    # @Method: Query system resource CPU information.
    # @Param: client
    # @Return:
    # @author: 
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
        print((PRO_FORMAT) % ('Count',
                              sys_resp['resource']['ProcessorSummary']['Count']))
        print((PRO_FORMAT) % ('Model',
                              sys_resp['resource']['ProcessorSummary']['Model']))
        print('\n[Summary]')
        print((PRO_FORMAT) % ('HealthRollup',
                              sys_resp['resource']['ProcessorSummary']['Status']['HealthRollup']))
    return sys_resp


def getprocessor(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain CPU information command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    resp = get_summary_sys(client)
    if resp is None:
        return None
    if resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp
    resp = get_processor_collection(client)
    if resp['status_code'] == 200:
        print('-' * 50)
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
        return resp
    return resp

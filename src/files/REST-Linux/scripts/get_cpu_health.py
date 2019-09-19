# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query CPU Health information.
# @command: getcpuhealth
# @Param: 
# @author: 
# @date: 2019.01.22
#==========================================================================
'''
PRO_FORMAT = '%-18s: %s'


def getcpuhealth_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain CPU information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getcpuhealth',
                                   help='''get processor information''')
    parser_list['getcpuhealth'] = sub_parser
    return 'getcpuhealth'


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
        print ('-' * 32)
        key = processor_resp['resource']
        print(PRO_FORMAT % ('Id', key.get("Id", None)))
        print(PRO_FORMAT % ('Name', key.get('Name', None)))
        status = key.get("Status", {})
        print(PRO_FORMAT % ('Health', status.get('Health', None)))
        print(PRO_FORMAT % ('State', status.get('State', None)))

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
        print('-' * 32)
        print('[Summary]')
        status = sys_resp['resource']['ProcessorSummary']['Status']
        print(PRO_FORMAT % ('HealthRollup', status['HealthRollup']))
    return sys_resp


def getcpuhealth(client, parser, args):
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
        print('-' * 32)
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
        return resp
    return resp

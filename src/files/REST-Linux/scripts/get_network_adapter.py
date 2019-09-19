# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Query power supply health information.
# @command: getpsuhealth
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
import sys

PF = '{0:20}: {1}'


def getnetworkadapter_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register power supply information commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('getnetworkadapter',
                                   help='get network adaptor information')
    parser_list['getnetworkadapter'] = sub_parser
    return 'getnetworkadapter'


def getnetworkadapter(client, parser, args):
    '''
    #====================================================================================
    # @Method: Obtain network adaptor command processing functions.
    # @Param: client, RedfishClient object
    parser, subcommand argparser. Export error messages when parameters are incorrect.
    args, parameter list
    # date:2017.08.29 11:59
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    slotid = client.get_slotid()
    if slotid is None:
        return None

    resp = get_summary(client)
    if resp is None:
        return None

    print('-' * 42)
    network_adapter_list = []
    resp = get_network_adapter_array(client, slotid, network_adapter_list)
    if resp is None or resp['status_code'] != 200:
        return resp

    for network_adapter in network_adapter_list:
        get_network_adapter_info(client, network_adapter)

    return resp


def get_network_ports(client, network_ports):
    print("\n[Ports]")

    for network_port in network_ports:
        url = network_port['@odata.id']
        resp = client.get_resource(url)
        if resp is None or resp['status_code'] != 200:
            return resp

        port = resp['resource']
        print('-' * 42)
        print(PF.format('Id', port['Id']))
        print(PF.format('Name', port['Name']))
        print(PF.format('PhysicalPortNumber', port['PhysicalPortNumber']))
        print(PF.format('LinkStatus', port['LinkStatus']))
        print(PF.format('NetworkAddresses',
                        ','.join(port['AssociatedNetworkAddresses'])))

        oem = resp['resource']['Oem']['Huawei']
        print(PF.format('PortType', oem['PortType']))


def get_network_adapter_info(client, resource_uri):
    """
    #====================================================================================
    #   @Method:  Obtain physical disk information.
    #   @Param:   volumeinfo Logical disk information, volume_list Export the logical disk list.
    #   @Return:
    #   @author:
    #====================================================================================
    """
    resp = client.get_resource(resource_uri)
    if resp is None or resp['status_code'] != 200:
        return resp

    adaptor = resp['resource']
    oem = resp['resource']['Oem']['Huawei']
    print(PF.format('Id', adaptor['Id']))
    print(PF.format('Name', oem['Name']))
    print(PF.format('Manufacturer', adaptor['Manufacturer']))
    print(PF.format('Model', adaptor['Model']))
    print(PF.format('CardManufacturer', oem['CardManufacturer']))
    print(PF.format('CardModel', oem['CardModel']))
    print(PF.format('DeviceLocator', oem['DeviceLocator']))
    print(PF.format('Position', oem['Position']))
    print(PF.format('RootBDF', oem['RootBDF']))

    print("\n[Status]")
    print(PF.format('Health', adaptor['Status']['Health']))
    print(PF.format('State', adaptor['Status']['State']))

    # get all related network ports
    network_ports = resp['resource']['Controllers'][0]['Link']['NetworkPorts']
    get_network_ports(client, network_ports)

    print('-' * 42)
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
    url = "/redfish/v1/Chassis/%s" % slotid
    sys_resp = client.get_resource(url)
    if sys_resp is None:
        return None
    if sys_resp['status_code'] == 200:
        oem = sys_resp['resource']['Oem']['Huawei']
        if oem.get('NetworkAdaptersSummary', None):
            print('-' * 42)
            print(PF.format('Count', oem['NetworkAdaptersSummary']['Count']))
            print('')
            print('[Summary]')
            status = oem['NetworkAdaptersSummary']['Status']
            print(PF.format('HealthRollup', status['HealthRollup']))
    return sys_resp


def get_network_adapter_array(client, slotid, members):
    """
    #====================================================================================
    #   @Method:  Obtain the network adaptor array.
    #   @Param:   client, RedfishClient client, slotid, slot information
                    drives_list physical disk list
    #   @Return:
    #   @author:
    #====================================================================================
    """
    chassis_url = "/redfish/v1/Chassis/%s/NetworkAdapters" % slotid
    resp = client.get_resource(chassis_url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

    if resp['resource']['Members@odata.count'] == 0:
        print('Failure: resource was not found')
        sys.exit(148)

    members.extend(
        [member['@odata.id'] for member in resp['resource']['Members']])
    return resp

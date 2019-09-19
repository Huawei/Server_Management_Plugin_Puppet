# -*- coding:utf-8 -*-
'''
#=============================================================
# @Method: Query Ethernet Interface information.
# @command: getethernet
# @Param:
# @author:
# @date: 2017.8.1
#=============================================================
'''
FORMAT = '%-20s: %s'


def getethernet_init(parser, parser_list):
    '''
    #===========================================================
    # @Method:Register IP address commands.
    # @Param: parser, parser_list
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    sub_parser = parser.add_parser('getethernet',
                                   help='''get IP information''')
    parser_list['getethernet'] = sub_parser

    return 'getethernet'


def get_ethernet_info(members_uri, client):
    '''
    #===========================================================
    # @Method: Query IP address information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1 11:11
    #===========================================================
    '''
    resp = client.get_resource(members_uri)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

    print_dns(resp)
    print("")
    print_vlan(resp)
    print("")
    print_ip(resp)
    print("")
    print_netport(resp)

    return resp


def print_netport(resp):
    port_message = resp["resource"]["Oem"]["Huawei"]
    print((FORMAT) % ("NetworkPortMode", \
                      port_message.get("NetworkPortMode", None)))
    print("\n[ManagementNetworkPort]")
    port_messageinfo = port_message.get("ManagementNetworkPort", None)
    if port_messageinfo is not None:
        for key in port_messageinfo:
            print((FORMAT) % (key, port_messageinfo[key]))
    print("\n[ManagementNetworkPort@AllowableValues]")
    idx = 0
    # @Redfish.AllowableValues is the [] type.
    man_port_all = port_message. \
        get("ManagementNetworkPort@Redfish.AllowableValues", "[]")
    if len(man_port_all) > 0:
        print("-" * 40)
        while idx < len(man_port_all):
            for key in man_port_all[idx]:
                print((FORMAT) % (key, man_port_all[idx][key]))
            idx += 1
            print("-" * 40)
    print("\n[AdaptivePort]")
    idx = 0
    # AdaptivePort is the [] type.
    ad_port = port_message.get("AdaptivePort", "[]")
    if len(ad_port) > 0:
        print("-" * 40)
        while idx < len(ad_port):
            for key in ad_port[idx]:
                print((FORMAT) % (key, ad_port[idx][key]))
            idx += 1
            print("-" * 40)


def print_vlan(resp):
    print("[VLAN]")
    vlan_info = resp["resource"].get("VLAN", None)
    if vlan_info is None:
        print('no data available for the resource')
        return None
    else:
        # Query VLAN information.
        for key in vlan_info:
            print((FORMAT) % (key, vlan_info[key]))


def print_ip(resp):
    print("[IP]")
    ip_version = resp["resource"]["Oem"]["Huawei"]["IPVersion"]
    ipv4_addresses = resp["resource"]["IPv4Addresses"]
    ipv6_addresses = resp["resource"]["IPv6Addresses"]
    # Display information.
    print("")
    print((FORMAT) % ("IPVersion", ip_version))
    print((FORMAT) % ("PermanentMACAddress", \
                      resp['resource']["PermanentMACAddress"]))
    print((FORMAT) % ("IPv6DefaultGateway", \
                      resp['resource']["IPv6DefaultGateway"]))
    print("\n[IPv4Addresses]")
    print("-" * 40)
    idx = 0
    while idx < len(ipv4_addresses):
        for key in ipv4_addresses[idx]:
            print((FORMAT) % (key, ipv4_addresses[idx][key]))
        print("-" * 40)
        idx += 1
    print("\n[IPv6Addresses]")
    idx = 0
    print("-" * 40)
    while idx < len(ipv6_addresses):
        for key in ipv6_addresses[idx]:
            print((FORMAT) % (key, ipv6_addresses[idx][key]))
        idx += 1
        print("-" * 40)


def print_dns(resp):
    print("[DNS]")
    name_service = resp["resource"]["NameServers"]
    mode = resp["resource"]["Oem"]["Huawei"]["DNSAddressOrigin"]
    # Display information.
    print("")
    print((FORMAT) % ("HostName", resp["resource"]["HostName"]))
    print((FORMAT) % ("FQDN", resp["resource"]["FQDN"]))
    print((FORMAT) % ("DNSAddressOrigin", mode))
    # nameservice The length must be 2.
    print((FORMAT) % ("PreferredServer", name_service[0]))
    print((FORMAT) % ("AlternateServer", name_service[1]))


def get_port_collection(client, slotid):
    '''
    #===========================================================
    # @Method:  Query collection information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp
    # 200 message
    members_count = resp['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
    # Query DNS information.
    else:
        members_uri = resp['resource']['Members'][0]["@odata.id"]
        resp = get_ethernet_info(members_uri, client)
    return resp


def getethernet(client, parser, args):
    '''
    #===========================================================
    # @Method: IP address command processing functions
    # @Param:client, parser, args
    # @Return:
    # @date: 2017.8.1 1:11
    #===========================================================
    '''
    if parser is None and args is None:
        return None
    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information.
    ret = get_port_collection(client, slotid)
    return ret

# -*- coding: utf-8 -*-
'''
#==========================================================================
# @Method:  Query Ethernet information.
# @command: getsyseth
# @Return:
# @date: 2017.7.27
#==========================================================================
'''
from sys import version

import sys

PRINT_STYLE1 = "%-20s: %s"
PRINT_STYLE2 = " " * 20
PRINT_STYLE3 = "-" * 20
PRINT_STYLE4 = "-" * 40


def getsyseth_init(parser, parser_list):
    '''
    #==========================================================================
    # @Method: Query host Ethernet information subcommands.
    # @command: getsyseth
    # @Param: parser: major command argparser
              parser_list, save subcommand parser list
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    sub_parser = parser.add_parser('getsyseth', \
                                   help='''get all system ethernet information''')
    sub_parser.add_argument('-PA', dest='PAGE', choices=['Enabled', \
                      'Disabled'], required=False, help='''get system ethernet \
                      information paging display''')
    sub_parser.add_argument('-I', dest='ID', required=False, \
                            help='''get specify system ethernet information''')
    parser_list['getsyseth'] = sub_parser

    return 'getsyseth'


def continue_or_break(list_str):
    '''
    #==========================================================================
    # @Method:  Determine whether to continue or exit.
    # @Param:
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    print("Input 'q' quit:")
    sys.stdout.flush()
    if list_str[0] != '2':
        strtemp = input("")  # pylint: disable=W0141
    else:
        strtemp = raw_input("")
    print(PRINT_STYLE4)
    tmp = strtemp.replace('\r', '')
    if tmp == 'q':
        return None
    return tmp


def get_ipv4addresses(dict1):
    '''
    #==========================================================================
    # @Method: Export IPv4 address information functions.
    # @Param: dict1, dictionary
    # @Return:
    # @date: 2017.7.27
    #==========================================================================
    '''
    # Obtain IPv4 address information.
    print("[IPv4Addresses]")
    length_ipv4 = len(dict1['IPv4Addresses'])
    if length_ipv4 != 0:
        for i in range(length_ipv4):
            if length_ipv4 > 1:
                print(PRINT_STYLE3)
            print((PRINT_STYLE1) % ("Address", \
                                    dict1["IPv4Addresses"][i]["Address"]))
            print((PRINT_STYLE1) % ("SubnetMask", \
                                    dict1["IPv4Addresses"][i]["SubnetMask"]))
            print((PRINT_STYLE1) % ("Gateway", \
                                    dict1["IPv4Addresses"][i]["Gateway"]))
    if length_ipv4 > 1:
        print(PRINT_STYLE3)
    print(PRINT_STYLE2)
    return


def get_ipv6addresses(dict1):
    '''
    #==========================================================================
    # @Method: Query IPv6 address information functions.
    # @Param: dict1, dictionary
    # @Return:
    # @date: 2017.7.27
    #==========================================================================
    '''
    # Obtain IPv6 address information.
    print("[IPv6Addresses]")
    length_ipv6 = len(dict1['IPv6Addresses'])
    if length_ipv6 != 0:
        for j in range(length_ipv6):
            if length_ipv6 > 1:
                print(PRINT_STYLE3)
            print((PRINT_STYLE1) % ("Address", \
                                    dict1["IPv6Addresses"][j]["Address"]))
            print((PRINT_STYLE1) % ("PrefixLength", \
                                    dict1["IPv6Addresses"][j]["PrefixLength"]))
            print((PRINT_STYLE1) % ("DefaultGateway", \
                                    dict1["IPv6DefaultGateway"]))
    if length_ipv6 > 1:
        print(PRINT_STYLE3)
    print(PRINT_STYLE2)
    return


def get_vlans(url, client):
    '''
    #==========================================================================
    # @Method: Query VLAN information functions.
    # @Param: url
              client, RedfishClient object
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    # Obtain VLAN information.
    print("[VLANs]")
    url1 = "%s/VLANs" % url
    resp_vlans = client.get_resource(url1)
    if resp_vlans is None or resp_vlans['status_code'] != 200:
        return
    dict_vlans = resp_vlans['resource']
    get_vlans_collection(dict_vlans, client)
    while ("Members@odata.nextLink" in dict_vlans):
        url2 = dict_vlans["Members@odata.nextLink"]
        resp_vlans_coll = client.get_resource(url2)
        if resp_vlans_coll is None:
            return None
        else:
            dict_vlans = resp_vlans_coll['resource']
            length_vlans1 = len(dict_vlans["Members"])
            if length_vlans1 == 1:
                print(PRINT_STYLE3)
            get_vlans_collection(dict_vlans, client)
            if length_vlans1 == 1:
                print(PRINT_STYLE3)
    return True


def get_eth_collection(dict_ids, client, args):
    '''
    #==========================================================================
    # @Method: Query Ethernet collection functions.
    # @Param: dict_ids,
              client, RedfishClient object
              args, parameter list
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    list_str = version
    for i in dict_ids["Members"]:
        url = i["@odata.id"]
        resp_id = client.get_resource(url)
        if resp_id is None:
            return None
        else:
            if resp_id['status_code'] == 200:
                dict_id = resp_id['resource']
                # Invoke the get_single_eth_info function.
                get_single_eth_info(url, dict_id, client)
                if (dict_ids["Members@odata.count"]) > 1:
                    print(PRINT_STYLE4)
        if args.PAGE == 'Enabled':
            tmp = continue_or_break(list_str)
            if tmp is None:
                sys.exit(0)
    return resp_id


def get_vlans_collection(dict_vlans, client):
    '''
    #==========================================================================
    # @Method: Query VLAN collection functions.
    # @Param: dict_vlans
              client, RedfishClient object
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    print_style1 = "%-20s: %-4s  %s  %s"
    length_vlans2 = len(dict_vlans["Members"])
    for k in dict_vlans["Members"]:
        url2 = k["@odata.id"]
        resp_vlan = client.get_resource(url2)
        if resp_vlan is None or resp_vlan['status_code'] != 200:
            break

        dict_vlan = resp_vlan['resource']
        if length_vlans2 > 1:
            print(PRINT_STYLE3)
        if dict_vlan["VLANEnable"] == "true":
            dict_vlan["VLANEnable"] = "enabled"
        else:
            dict_vlan["VLANEnable"] = "disabled"
        print((print_style1) % ("VLAN", dict_vlan["VLANId"], \
                                "|", dict_vlan["VLANEnable"]))
    if length_vlans2 > 1 and "Members@odata.nextLink" not in dict_vlans:
        print(PRINT_STYLE3)
    return


def get_eth_info_id(ethid, slotid, client):
    '''
    #==========================================================================
    # @Method: Query host Ethernet information with IDs.
    # @Param: ethid, slotid, client
    # @Return:
    # @date: 2017.7.27
    #==========================================================================
    '''
    url = "/redfish/v1/Systems/%s/EthernetInterfaces/%s" % (slotid, ethid)
    resp = client.get_resource(url)
    if resp is None:
        return None
    else:
        # Determine the entered ID.
        if resp['status_code'] == 404:
            print("Failure: resource was not found")
        elif resp['status_code'] == 200:
            dict1 = resp['resource']
            # Invoke the get_single_eth_info function.
            get_single_eth_info(url, dict1, client)
        return resp


def get_eth_info(slotid, client, args):
    '''
    #==========================================================================
    # @Method: Query host Ethernet information without IDs.
    # @Param: slotid, slot number
              client, RedfishClient object
              args, parameter list
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    url1 = "/redfish/v1/Systems/%s/EthernetInterfaces" % slotid
    resp = client.get_resource(url1)
    if resp is None:
        return None
    else:
        resp_ids = client.get_resource(url1)
        if resp_ids is None:
            return None
        if resp['status_code'] == 200:
            dict_ids = resp['resource']
            # Determine whether the ID collection is zero.
            if dict_ids["Members@odata.count"] == 0:
                print("no data available for the resource")
            else:
                resp = get_eth_collection(dict_ids, client, args)
                if resp is not None:
                    while ("Members@odata.nextLink" in dict_ids):
                        url2 = dict_ids["Members@odata.nextLink"]
                        resp_ids_coll = client.get_resource(url2)
                        if resp_ids_coll is not None:
                            dict_ids = resp_ids_coll['resource']
                            resp = get_eth_collection(dict_ids, client, args)
                            if resp is None:
                                return None
    return resp


def get_single_eth_info(url, dict1, client):
    '''
    #==========================================================================
    # @Method: Export host Ethernet information functions.
    # @Param: url
              dict1, dictionary
              client, RedfishClient object
    # @Return:
    # @date: 2017.7.27
    #==========================================================================
    '''
    print((PRINT_STYLE1) % ("Id", dict1["Id"]))

    if "MACAddress" in dict1.keys():
        print((PRINT_STYLE1) % ("MACAddress", dict1["MACAddress"]))
    if "PermanentMACAddress" in dict1.keys():
        print((PRINT_STYLE1) % ("PermanentMACAddress", dict1["PermanentMACAddress"]))

    print((PRINT_STYLE1) % ("LinkStatus", dict1["LinkStatus"]))
    print(PRINT_STYLE2)
    get_ipv4addresses(dict1)
    get_ipv6addresses(dict1)
    get_vlans(url, client)


def getsyseth(client, parser, args):
    '''
    #==========================================================================
    # @Method: Query host Ethernet information.
    # @command: getsyseth
    # @Param: client, RedfishClient object
              parser, subcommand argparser. Export error messages when parameters are incorrect.
              args, parameter list
    # @Return:
    # @date: 2017.8.18
    # Modify the content: DTS2017080702930
    #==========================================================================
    '''
    if parser is None:
        return None
    slotid = client.get_slotid()
    if slotid is None:
        return None
    if args.ID is not None:
        resp = get_eth_info_id(args.ID, slotid, client)
    else:
        resp = get_eth_info(slotid, client, args)
    return resp

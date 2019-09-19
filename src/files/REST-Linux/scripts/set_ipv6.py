# -*- coding:utf-8 -*-
'''
#===========================================================
# @Method: Set IPv6.
# @command: setmagenetport
# @Param: 
# @author: 
# @date: 2017.7.21
#===========================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '


def setipv6_init(parser, parser_list):
    '''
    #=========================================================
    #   @Method:  set ip addr6
    #   @Param:  
    #   @Return:
    #   @author: 
    #=========================================================
    '''
    sub_parser = parser.add_parser('setipv6', \
                                   help='''set IPv6 information of the iBMC network port''')
    sub_parser.add_argument('-IP', dest='address', required=False, \
                            help='''IPv6 address of the iBMC network port''')
    sub_parser.add_argument('-M', dest='addressorigin', \
                            required=False, choices=['Static', 'DHCPv6'], \
                            help='''how the IPv6 address of the iBMC
            network port is allocated''')
    sub_parser.add_argument('-G', dest='gateway', required=False, \
                            help='''gateway IPv6 address of the iBMC network port''')
    sub_parser.add_argument('-L', dest='prefixlength', required=False, \
                            type=int, help='''IPv6 address prefix length of
            the iBMC network port''')

    parser_list['setipv6'] = sub_parser

    return 'setipv6'


def setipv6(client, parser, args):
    '''
    #=====================================================================
    #   @Method:  set ip
    #   @Param:   
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    if args.address is None \
            and args.addressorigin is None \
            and args.gateway is None \
            and args.prefixlength is None:
        parser.error('at least one parameter must be specified')

    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information.
    uri, resp = get_port_collection(client, slotid)
    if uri is None:
        return resp

    resp_ip6 = set_ipv6_addresses_info(uri, client, args)
    return resp_ip6


def set_ipv6_addresses_info(uri, client, args):
    '''
    #===========================================================
    # @Method: 
    # @Param:uri, client, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    resp_ip6 = client.get_resource(uri)
    if resp_ip6 is None:
        return None
    elif resp_ip6['status_code'] != 200:
        if resp_ip6['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_ip6

    payload = {}
    # Encapsulate the request body.
    if args.address is not None or args.prefixlength is not None \
            or args.addressorigin is not None:
        ip_addrresses = [{}]
        if args.address is not None:
            ip_addrresses[0]['Address'] = args.address
        if args.prefixlength is not None:
            ip_addrresses[0]['PrefixLength'] = args.prefixlength
        if args.addressorigin is not None:
            ip_addrresses[0]['AddressOrigin'] = args.addressorigin
        payload['IPv6Addresses'] = ip_addrresses
    if args.gateway is not None:
        payload['IPv6DefaultGateway'] = args.gateway
    # print (payload)
    resp_ip6 = client.set_resource(uri, payload)
    if resp_ip6 is None:
        return None
    if resp_ip6['status_code'] == 200:
        check_err_info(resp_ip6['resource'], resp_ip6['status_code'])
    if resp_ip6['status_code'] == 400:
        check_err_info(resp_ip6['message']['error'], resp_ip6['status_code'])

    return resp_ip6


def check_err_info(resp_ip6, code_ipv6):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInfo
    # @Param:resp_ip6
    # @Return:
    # @author: 
    #====================================================================================
    '''
    ipv6_message = ""
    mess_ipv6 = resp_ip6.get("@Message.ExtendedInfo", "")
    if len(mess_ipv6) != 0:
        ipv6_message = resp_ip6["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs.
    if ipv6_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege" or \
                    ipv6_message[0]['MessageId'] == \
                    "Base.1.0.InsufficientPrivilege":
        print('Failure: you do not have the required' + \
              ' permissions to perform this operation')
        return None
    # ipv6 messages
    if code_ipv6 == 400:
        sys.stdout.write('Failure: ')
        all_err(ipv6_message)
        return None
    # Display 200 messages independently.
    if code_ipv6 == 200:
        print(FAILURE_MESS)
        part_err(ipv6_message)
        sys.exit(144)
    return resp_ip6


def part_err(ipv6_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, ipv6_message
    # @Return:
    # @author: 
    #====================================================================================
    '''
    idx = 0
    while idx < len(ipv6_message):
        check_info = ipv6_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("IPv6Addresses/0/", "")
        message = message.replace("IPv6Addresses/", "")
        print('         %s' % message)
        idx += 1


def all_err(ipv6_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, ipv6_message
    # @Return:
    # @date:2017.08.29 9:50
    #====================================================================================
    '''
    idx = 0
    while idx < len(ipv6_message):
        check_info = ipv6_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("IPv6Addresses/0/", "")
        message = message.replace("IPv6Addresses/", "")
        if idx == 0:
            print('%s' % message)
        else:
            print('         %s' % message)
        idx += 1


def get_port_collection(client, slotid):
    '''
    #===========================================================
    # @Method: Query collection information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1 9:45
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    resp_ip6 = client.get_resource(url)
    members_uri = None
    if resp_ip6 is None:
        return members_uri, None
    elif resp_ip6['status_code'] != 200:
        if resp_ip6['status_code'] == 404:
            print('Failure: resource was not found')
        return members_uri, resp_ip6
    members_count = resp_ip6['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
        return members_uri, resp_ip6
    else:
        members_uri = resp_ip6['resource']['Members'][0]["@odata.id"]

    return members_uri, resp_ip6

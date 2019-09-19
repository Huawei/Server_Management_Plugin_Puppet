# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set IPv4.
# @command: setmagenetport
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '


def setipv4_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  set ip addr4
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('setipv4', \
                                   help='''set IPv4 information of the iBMC network port''')
    sub_parser.add_argument('-IP', dest='address', required=False,
                            help='''IPv4 address of the iBMC network port''')
    sub_parser.add_argument('-M', dest='addressorigin', required=False,
                            choices=['Static', 'DHCP'],
                            help='''how the IPv4 address of the iBMC
                            network port is allocated''')
    sub_parser.add_argument('-G', dest='gateway', required=False,
                            help='''gateway IPv4 address of the
                            iBMC network port''')
    sub_parser.add_argument('-MASK', dest='subnetmask', required=False,
                            help='''subnet mask of the iBMC network port''')

    parser_list['setipv4'] = sub_parser

    return 'setipv4'


def setipv4(client, parser, args):
    '''
    #=====================================================================
    #   @Method:  set ip
    #   @Param:
    #   @Return:
    #   @date: 2017.8.1 11:11
    #=====================================================================
    '''
    if args.address is None \
            and args.addressorigin is None \
            and args.gateway is None \
            and args.subnetmask is None:
        parser.error('at least one parameter must be specified')

    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information.
    uri, resp = get_port_collection(client, slotid)
    if uri is None:
        return resp

    re_ipv4 = set_ipv4_addresses_info(uri, client, args)
    return re_ipv4


def set_ipv4_addresses_info(uri, client, args):
    '''
    #===========================================================
    # @Method:
    # @Param:uri, client, args
    # @Return:
    # @date: 2017.8.1 11:09
    #===========================================================
    '''
    re_ipv4 = client.get_resource(uri)
    if re_ipv4 is None:
        return None
    elif re_ipv4['status_code'] != 200:
        if re_ipv4['status_code'] == 404:
            print('Failure: resource was not found')
        return re_ipv4

    # Encapsulate the request body.
    payload = {'IPv4Addresses': [{}]}
    if args.address is not None:
        payload['IPv4Addresses'][0]['Address'] = args.address
    if args.subnetmask is not None:
        payload['IPv4Addresses'][0]['SubnetMask'] = args.subnetmask
    if args.gateway is not None:
        payload['IPv4Addresses'][0]['Gateway'] = args.gateway
    if args.addressorigin is not None:
        payload['IPv4Addresses'][0]['AddressOrigin'] = args.addressorigin
    # Set
    re_ipv4 = client.set_resource(uri, payload)
    if re_ipv4 is None:
        return None
    if re_ipv4['status_code'] == 200:
        check_err_info(re_ipv4['resource'], re_ipv4['status_code'])
    if re_ipv4['status_code'] == 400:
        check_err_info(re_ipv4['message']['error'], re_ipv4['status_code'])

    return re_ipv4


def check_err_info(re_ipv4, code_ipv4):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInfo
    # @Param:re_ipv4
    # @Return:
    # @author:
    #====================================================================================
    '''
    ipv4_message = ""
    mess_ipv4 = re_ipv4.get("@Message.ExtendedInfo", "")
    if len(mess_ipv4) != 0:
        ipv4_message = re_ipv4["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs.
    if ipv4_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege" or \
                    ipv4_message[0]['MessageId'] == \
                    "Base.1.0.InsufficientPrivilege":
        print('Failure: you do not have the required' + \
              ' permissions to perform this operation')
        return None
    # Display 400 messages independently.
    if code_ipv4 == 400:
        sys.stdout.write('Failure: ')
        all_err(ipv4_message)
        return None
    # Display 200 messages independently.
    if code_ipv4 == 200:
        print(FAILURE_MESS)
        part_err(ipv4_message)
        sys.exit(144)


def part_err(ipv4_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, ipv4_message
    # @Return:
    # @date:2017.08.29 14:26
    #====================================================================================
    '''
    idx = 0
    while idx < len(ipv4_message):
        check_info = ipv4_message[idx]['Message']
        msge_ip = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        msge_ip = msge_ip.replace("IPv4Addresses/0/", "")
        msge_ip = msge_ip.replace("IPv4Addresses/", "")
        print('         %s' % msge_ip)
        idx += 1


def all_err(ipv4_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, ipv4_message
    # @Return:
    # @date:2017.08.9 17:36
    #====================================================================================
    '''
    idx = 0
    while idx < len(ipv4_message):
        check_info = ipv4_message[idx]['Message']
        msge_ip = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        msge_ip = msge_ip.replace("IPv4Addresses/0/", "")
        msge_ip = msge_ip.replace("IPv4Addresses/", "")
        if idx == 0:
            print('%s' % msge_ip)
        else:
            print('         %s' % msge_ip)
        idx += 1


def get_port_collection(client, slotid):
    '''
    #===========================================================
    # @Method: Query collection information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    re_ipv4 = client.get_resource(url)
    members_uri = None
    if re_ipv4 is None:
        return members_uri, None
    elif re_ipv4['status_code'] != 200:
        if re_ipv4['status_code'] == 404:
            print('Failure: resource was not found')
        return members_uri, re_ipv4
    members_count = re_ipv4['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
        return members_uri, re_ipv4
    else:
        members_uri = re_ipv4['resource']['Members'][0]["@odata.id"]

    return members_uri, re_ipv4

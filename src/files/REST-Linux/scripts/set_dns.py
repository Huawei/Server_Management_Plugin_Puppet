# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set DNS information.
# @command: setdns
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '
HOSTNAME = 'specifies a host name for iBMC. value: a string of 1 \
to 64 characters setting, rule: the value can contain letters, digits, \
and hyphens (-), but cannot start or end with a hyphen'
DOMAIN = 'specifies a domain name for the server. value: \
a string of 0 to 67 characters setting rule: the value can \
contain letters, digits, and special characters including spaces'
DOMAINERR = 'Invalid domain name. value: \
a string of 0 to 67 characters, setting rule: the value can \
contain letters, digits, and special characters including spaces'
DOMAINERR1 = '         Invalid domain name. value: \
a string of 0 to 67 characters, setting rule: the value can \
contain letters, digits, and special characters including spaces'


def setdns_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain DNS commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('setdns', help='''set DNS information''')
    sub_parser.add_argument('-M', dest='DNSAddressOrigin',
                            type=str, required=False, choices=['Static', 'IPv4', 'IPv6'], \
                            help='''how DNS server information is obtained''')
    sub_parser.add_argument('-H', dest='HostName', type=str, \
                            required=False, help=HOSTNAME)
    sub_parser.add_argument('-D', dest='Domain', type=str, \
                            required=False, help=DOMAIN)
    sub_parser.add_argument('-PRE', dest='PreferredServer', \
                            type=str, required=False, \
                            help='''specifies the IP address of the preferred DNS server''')
    sub_parser.add_argument('-ALT', dest='AlternateServer', \
                            type=str, required=False, \
                            help='''specifies the IP address of the alternate DNS server''')
    parser_list['setdns'] = sub_parser

    return 'setdns'


def package_request(args, payload, host_name, ip_server):
    '''
    #====================================================================================
    # @Method: Encapsulate the request body.
    # @Param：args,payload
    # @Return:
    # @author:
    #====================================================================================
    '''
    if args.HostName is not None:
        payload["HostName"] = args.HostName
        host_name = args.HostName
    if args.Domain is not None:
        payload["FQDN"] = ("%s.%s" % (host_name, args.Domain))
    # Set active and standby server addresses.
    if args.PreferredServer is not None or args.AlternateServer is not None:
        name_service = []
        if args.PreferredServer is not None:
            name_service.append(args.PreferredServer)
        elif args.PreferredServer is None and len(ip_server[0]) != 0:
            name_service.append(ip_server[0])
        else:
            name_service.append("")
        if args.AlternateServer is not None:
            name_service.append(args.AlternateServer)
        elif args.AlternateServer is None and len(ip_server[1]) != 0:
            name_service.append(ip_server[1])
        else:
            name_service.append("")
        payload["NameServers"] = name_service
    # Address mode
    if args.DNSAddressOrigin is not None:
        huawei = {}
        oem = {}
        huawei["DNSAddressOrigin"] = args.DNSAddressOrigin
        oem["Huawei"] = huawei
        payload["Oem"] = oem


def part_err(err_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, err_message
    # @Return:
    # @date:2017.08.29 23:50
    #====================================================================================
    '''
    idx = 0
    while idx < len(err_message):
        if len(err_message[idx]['RelatedProperties']) != 0:
            if err_message[idx]['RelatedProperties'][0] \
                    == '#/FQDN':
                print(DOMAINERR1)
                idx += 1
                continue
        check_info = err_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("Oem/Huawei/", "")
        message = message.replace("NameServers/0", "PreferredServer")
        message = message.replace("NameServers/1", "AlternateServer")
        print('         %s' % message)
        idx += 1


def all_err(err_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, err_message
    # @Return:
    # @date:2017.08.29 10:50
    #====================================================================================
    '''
    idx = 0
    while idx < len(err_message):
        if len(err_message[idx]['RelatedProperties']) != 0:
            if err_message[idx]['RelatedProperties'][0] \
                    == "#/FQDN":
                if idx == 0:
                    print(DOMAINERR)
                else:
                    print(DOMAINERR1)
                idx += 1
                continue
        check_info = err_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("Oem/Huawei/", "")
        message = message.replace("NameServers/0", "PreferredServer")
        message = message.replace("NameServers/1", "AlternateServer")
        if idx == 0:
            print('%s' % message)
        else:
            print('         %s' % message)
        idx += 1


def check_err_info(resp_dns, code_dns):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInf.
    # @Param:resp_dns
    # @Return:
    # @author:
    #====================================================================================
    '''
    err_message = ""
    mess = resp_dns.get("@Message.ExtendedInfo", "")
    if len(mess) != 0:
        err_message = resp_dns["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs.
    if err_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege":
        print('Failure: you do not have the required ' + \
              'permissions to perform this operation')
        return None
    # DNS error message
    if code_dns == 400:
        sys.stdout.write('Failure: ')
        all_err(err_message)
        return None
    # Independent display of 200 messages
    if code_dns == 200:
        print(FAILURE_MESS)
        part_err(err_message)
        sys.exit(144)
    return resp_dns


def set_dns_info(members_uri, client, args):
    '''
    #===========================================================
    # @Method: Set DNS information.
    # @Param:members_uri, client, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    resp_dns = client.get_resource(members_uri)
    if resp_dns is None:
        return None
    elif resp_dns['status_code'] != 200:
        if resp_dns['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_dns
    host_name = resp_dns['resource']['HostName']
    name_service = resp_dns['resource']['NameServers']
    # Encapsulate the request body.
    payload = {}
    package_request(args, payload, host_name, name_service)
    resp_dns = client.set_resource(members_uri, payload)
    if resp_dns is None:
        return None
    if resp_dns['status_code'] == 200:
        check_err_info(resp_dns['resource'], resp_dns['status_code'])
    if resp_dns['status_code'] == 400:
        check_err_info(resp_dns['message']['error'], resp_dns['status_code'])
    return resp_dns


def get_port_collection(client, slotid, args):
    '''
    #===========================================================
    # @Method: Query collection information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    resp_dns = client.get_resource(url)
    if resp_dns is None:
        return None
    elif resp_dns['status_code'] != 200:
        if resp_dns['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_dns
    members_count = resp_dns['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
        return resp_dns
    # Set DNS information.
    else:
        members_uri = resp_dns['resource']['Members'][0]["@odata.id"]
        resp_dns = set_dns_info(members_uri, client, args)
    return resp_dns


def setdns(client, parser, args):
    '''
    #===========================================================
    # @Method: DNS command processing function
    # @Param:client, parser, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    if args.DNSAddressOrigin is None and args.HostName is None and \
                    args.Domain is None and args.PreferredServer is None and \
                    args.AlternateServer is None:
        parser.error('at least one parameter must be specified')
    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information.
    ret = get_port_collection(client, slotid, args)
    return ret

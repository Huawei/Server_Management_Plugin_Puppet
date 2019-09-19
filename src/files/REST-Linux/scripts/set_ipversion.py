# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set IP versions.
# @command: setdns
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
import sys

FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '


def setipversion_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register IP protocol commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('setipversion', help='''set IP version''')
    sub_parser.add_argument('-M', dest='IPVersion',
                            type=str, required=True, \
                            choices=['IPv4AndIPv6', 'IPv4', 'IPv6'], \
                            help='''whether IPv4/IPv6 protocol is enabled''')
    parser_list['setipversion'] = sub_parser

    return 'setipversion'


def package_request(args, payload):
    '''
    #====================================================================================
    # @Method: Encapsulate the request body.
    # @Param：args,payload
    # @Return:
    # @author:
    #====================================================================================
    '''
    huawei = {}
    oem = {}
    huawei["IPVersion"] = args.IPVersion
    oem["Huawei"] = huawei
    payload["Oem"] = oem


def part_err(ck_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, ck_message
    # @Return:
    # @date:2017.07.29 16:26
    #====================================================================================
    '''
    idx = 0
    while idx < len(ck_message):
        check_info = ck_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("Oem/Huawei/", "")
        print('         %s' % message)
        idx += 1


def all_err(ck_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, ck_message
    # @Return:
    # @date:2017.08.29 8:26
    #====================================================================================
    '''
    idx = 0
    while idx < len(ck_message):
        check_info = ck_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("Oem/Huawei/", "")
        if idx == 0:
            print('%s' % message)
        else:
            print('         %s' % message)
        idx += 1


def check_err_info(resp_ver, code_ipv):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInf
    # @Param:resp_ver
    # @Return:
    # @author:
    #====================================================================================
    '''
    ck_message = ""
    mess_ver = resp_ver.get("@Message.ExtendedInfo", "")
    if len(mess_ver) != 0:
        ck_message = resp_ver["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs.
    if ck_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege" or \
                    ck_message[0]['MessageId'] == \
                    "Base.1.0.InsufficientPrivilege":
        print('Failure: you do not have the required' + \
              ' permissions to perform this operation')
        return None
    # IP version error messages
    if code_ipv == 400:
        sys.stdout.write('Failure: ')
        all_err(ck_message)
        return None
    # Display 200 messages independently.
    if code_ipv == 200:
        print(FAILURE_MESS)
        part_err(ck_message)
        sys.exit(144)
    return resp_ver


def set_version_info(members_uri, client, args):
    '''
    #===========================================================
    # @Method: Set DNS information.
    # @Param:members_uri, client, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    # Encapsulate the request body.
    payload = {}
    package_request(args, payload)
    resp_ver = client.get_resource(members_uri)
    if resp_ver is None:
        return None
    elif resp_ver['status_code'] != 200:
        if resp_ver['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_ver
    resp_ver = client.set_resource(members_uri, payload)
    if resp_ver is None:
        return None
    if resp_ver['status_code'] == 200:
        check_err_info(resp_ver['resource'], resp_ver['status_code'])
    if resp_ver['status_code'] == 400:
        check_err_info(resp_ver['message']['error'], resp_ver['status_code'])
    return resp_ver


def get_port_collection(client, slotid, args):
    '''
    #===========================================================
    # @Method: Query collection information.
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1 11:27
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    resp_ver = client.get_resource(url)
    if resp_ver is None:
        return None
    elif resp_ver['status_code'] != 200:
        if resp_ver['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_ver
    members_count = resp_ver['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
        return resp_ver
    # Set information.
    else:
        members_uri = resp_ver['resource']['Members'][0]["@odata.id"]
        resp_ver = set_version_info(members_uri, client, args)
    return resp_ver


def setipversion(client, parser, args):
    '''
    #===========================================================
    # @Method: setipversion command processing functions
    # @Param:client, parser, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    if args.IPVersion is None:
        parser.error('at least one parameter must be specified')
    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information.
    ret = get_port_collection(client, slotid, args)
    return ret

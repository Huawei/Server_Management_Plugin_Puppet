# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Set VLAN information.
# @command: setvlan
# @Param:
# @author:
# @date: 2017.7.21
#==========================================================================
'''
FAILURE_MESS = 'Failure: some of the settings failed.\
 possible causes include the following: '
import sys


def setvlan_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register and obtain VLAN commands.
    # @Param: parser, major command argparser
    parser_list, save subcommand parser list
    # @Return:
    # @author:
    #====================================================================================
    '''
    sub_parser = parser.add_parser('setvlan', help='''set VLAN information''')
    sub_parser.add_argument('-S', dest='VLANEnable',
                            type=str, required=False, choices=['True', 'False'], \
                            help='''whether VLAN is enabled''')
    sub_parser.add_argument('-I', dest='VLANId', type=int, \
                            required=False, help='''VLAN identifier''')
    parser_list['setvlan'] = sub_parser

    return 'setvlan'


def package_request(args, payload):
    '''
    #====================================================================================
    # @Method: Encapsulate the request body
    # @Param：args,payload
    # @Return:
    # @author:
    #====================================================================================
    '''
    vlan = {}
    if args.VLANId is not None:
        vlan["VLANId"] = args.VLANId
    if args.VLANEnable is not None:
        if args.VLANEnable == "True":
            vlan["VLANEnable"] = True
        else:
            vlan["VLANEnable"] = False
    payload["VLAN"] = vlan


def part_err(vlan_message):
    '''
    #====================================================================================
    # @Method: 200 messages
    # @Param:idx, vlan_message
    # @Return:
    # @date:2017.08.29 11:26
    #====================================================================================
    '''
    idx = 0
    while idx < len(vlan_message):
        check_info = vlan_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("VLAN/", "")
        print('         %s' % message)
        idx += 1


def all_err(vlan_message):
    '''
    #====================================================================================
    # @Method: 400 messages
    # @Param:idx, vlan_message
    # @Return:
    # @date:2017.08.29 17:27
    #====================================================================================
    '''
    idx = 0
    while idx < len(vlan_message):
        check_info = vlan_message[idx]['Message']
        message = "%s%s" % \
                  (check_info[0].lower(), check_info[1:len(check_info) - 1])
        message = message.replace("VLAN/", "")
        if idx == 0:
            print('%s' % message)
        else:
            print('         %s' % message)
        idx += 1


def check_err_info(resp_vlan, code_vlan):
    '''
    #====================================================================================
    # @Method: Determine whether all attributes are set successfully. Query @Message.ExtendedInf
    # @Param:resp_vlan
    # @Return:
    # @author:
    #====================================================================================
    '''
    vlan_message = ""
    mess_vlan = resp_vlan.get("@Message.ExtendedInfo", "")
    if len(mess_vlan) != 0:
        vlan_message = resp_vlan["@Message.ExtendedInfo"]
    else:
        print('Success: successfully completed request')
        return None
    # Determine whether a permission problem occurs
    if vlan_message[0]['MessageId'] == \
            "iBMC.1.0.PropertyModificationNeedPrivilege" or \
                    vlan_message[0]['MessageId'] == \
                    "Base.1.0.InsufficientPrivilege":
        print('Failure: you do not have the required' + \
              ' permissions to perform this operation')
        return None
    # VLAN error messages
    if code_vlan == 400:
        sys.stdout.write('Failure: ')
        all_err(vlan_message)
        return None
    # Independent display of 200 messages
    if code_vlan == 200:
        print(FAILURE_MESS)
        part_err(vlan_message)
        sys.exit(144)
    return resp_vlan


def set_vlan_info(members_uri, client, args):
    '''
    #===========================================================
    # @Method: Set VLAN information
    # @Param:members_uri, client, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    # Encapsulate the request body
    payload = {}
    package_request(args, payload)
    resp_vlan = client.get_resource(members_uri)
    if resp_vlan is None:
        return None
    elif resp_vlan['status_code'] != 200:
        if resp_vlan['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_vlan
    resp_vlan = client.set_resource(members_uri, payload)
    if resp_vlan is None:
        return None
    if resp_vlan['status_code'] == 200:
        check_err_info(resp_vlan['resource'], resp_vlan['status_code'])
    if resp_vlan['status_code'] == 400:
        check_err_info(resp_vlan['message']['error'], resp_vlan['status_code'])

    return resp_vlan


def get_port_collection(client, slotid, args):
    '''
    #===========================================================
    # @Method: Query collection information
    # @Param:client, slotid
    # @Return:
    # @date: 2017.8.1 11:33
    #===========================================================
    '''
    url = "/redfish/v1/managers/%s/EthernetInterfaces" % slotid
    resp_vlan = client.get_resource(url)
    if resp_vlan is None:
        return None
    elif resp_vlan['status_code'] != 200:
        if resp_vlan['status_code'] == 404:
            print('Failure: resource was not found')
        return resp_vlan
    members_count = resp_vlan['resource']["Members@odata.count"]
    if members_count == 0:
        print("no data available for the resource")
        return resp_vlan
    # Set VLAN information
    else:
        members_uri = resp_vlan['resource']['Members'][0]["@odata.id"]
        resp_vlan = set_vlan_info(members_uri, client, args)
    return resp_vlan


def setvlan(client, parser, args):
    '''
    #===========================================================
    # @Method: VLAN command processing function
    # @Param:client, parser, args
    # @Return:
    # @date: 2017.8.1
    #===========================================================
    '''
    if args.VLANEnable is None and args.VLANId is None:
        parser.error('at least one parameter must be specified')
    if args.VLANId is not None and (args.VLANId < 1 or args.VLANId > 4094):
        parser.error('argument -I: invalid choice: %s (choose from 1 to 4094)' \
                     % args.VLANId)
    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Query collection information
    ret = get_port_collection(client, slotid, args)
    return ret

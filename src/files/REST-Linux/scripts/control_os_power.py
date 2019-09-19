#!/usr/bin/env python
# -*- coding: utf-8 -*-
import upgrade_sp
'''
#=========================================================================
#   @Description:  control os power
#
#   @Date:
#=========================================================================
'''


def controlospower_init(parser, parser_list):
    '''
    #=========================================================================
    #   @Description:  control os power subcommand init
    #   @Method:  controlospower
    #   @Param:
    #   @Return:
    #   @Date:
    #=========================================================================
    '''
    sub_parser = parser.add_parser('syspowerctrl',
                                   help='''system power control''')
    sub_parser.add_argument('-T', dest='ResetType',
                            choices=['On', 'ForceOff', 'GracefulShutdown', \
                                     'ForceRestart', 'Nmi', 'ForcePowerCycle'],
                            required=True,
                            help='''System power control options''')
    parser_list['syspowerctrl'] = sub_parser

    return 'syspowerctrl'


def controlospower(client, parser, args):
    '''
    #=========================================================================
    #   @Description:  control os power entry
    #   @Method:  controlospower
    #   @Param:
    #   @Return:
    #   @Date:
    #=========================================================================
    '''
    if parser is None or args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/systems/%s/Actions/ComputerSystem.Reset" % slotid

    payload = {"ResetType": args.ResetType}

    resp = client.create_resource(url, payload)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print('Success: successfully completed request')

    else:
        if resp['status_code'] == 400:
            # messages = resp['message']['error']['@Message.ExtendedInfo']
            # print(messages)
            # ResetOperationNotAllowed
            print('Failure: operation not allowed')

        else:
            upgrade_sp.print_status_code(resp)

    return resp

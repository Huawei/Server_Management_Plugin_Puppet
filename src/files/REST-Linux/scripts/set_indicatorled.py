# -*- coding:utf-8 -*-

"""
#=========================================================================
#   @Description:  Set indicator State of Chassis
#
#   @author:
#   @Date:
#=========================================================================
"""
import sys


def setindicatorled_init(parser, parser_list):
    """
    #=====================================================================
    #   @Method:  set indicator LED state
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    """
    sub_parser = parser.add_parser('setindicatorled',
                                   help='''set product information''')
    sub_parser.add_argument('-S', dest='state', required=True,
                            choices=['Lit', 'Off', 'Blinking'],
                            help='state of indicator led')

    parser_list['setindicatorled'] = sub_parser
    return 'setindicatorled'


def setindicatorled(client, parser, args):
    """
    #=====================================================================
    #   @Method:  set product info
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    """

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Chassis/%s" % slotid

    resp = client.get_resource(url)
    if resp is None:
        return None
    if resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        return resp

    payload = {
        "IndicatorLED": args.state
    }

    resp = client.set_resource(url, payload)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print('Success: successfully completed request')
    else:
        from common_function import display_error_message
        display_error_message(client, resp)

    return resp

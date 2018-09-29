# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  restore BIOS defaults
#
#   @author:
#   @Date:
#=========================================================================
'''


def setbiosdefault_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  BIOS default setting restoration subcommand
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('restorebios',
                                   help='''restore BIOS setup defaults''')

    parser_list['restorebios'] = sub_parser

    return 'restorebios'


def setbiosdefault(client, parser, args):
    '''
    #=====================================================================
    #   @Method: BIOS default setting restoration subcommand processing function
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Systems/%s/Bios/Actions/Bios.ResetBios" % slotid

    payload = {}
    resp = client.create_resource(url, payload)

    if resp is None:
        return None

    if resp['status_code'] == 200:
        print("Success: successfully completed request")
    else:
        error_message(resp)

    return resp


def error_message(resp):
    '''
    #=====================================================================
    #   @Method: error handling
    #   @Param:  error_code
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if resp['status_code'] == 404:
        print("Failure: resource was not found")
    elif resp['status_code'] == 400:
        message = resp['message']['error']['@Message.ExtendedInfo']
        messageid = message[0]['MessageId'].split('.')[-1]
        if messageid == 'ResourceMissingAtURI':
            print("Failure: resource was not found")
        else:
            print("Failure: the request failed " + \
                  "due to an internal service error")
    else:
        print("Failure: the request failed due to an internal service error")

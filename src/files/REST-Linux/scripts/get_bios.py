# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  get BIOS information
#
#   @author:
#   @Date:
#=========================================================================
'''


def getbios_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  BIOS menu item query subcommands
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('getbios',
                                   help='''get BIOS setup information''')
    sub_parser.add_argument('-A', dest='attribute',
                            required=False,
                            help='''attribute name''')

    parser_list['getbios'] = sub_parser

    return 'getbios'


def getbios(client, parser, args):
    '''
    #=====================================================================
    #   @Method: BIOS menu item query subcommand processing functions
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
    #   @Return:
    #   @author:
    #   @date:  2017-8-30 09:04:14
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Systems/%s/Bios" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        info = resp['resource']['Attributes']
        if info is None:
            print('no data available for the resource')
            return resp

        print_resource(info, args)

    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    elif resp['status_code'] == 400:
        print("Failure: the request failed due to an internal service error")

    return resp


def print_resource(info, args):
    '''
    #=====================================================================
    #   @Method:  Display the returned BIOS data.
    #   @Param:   info, BIOS message dictionary
    #             args, command parameter
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if args.attribute is not None:
        # Display data specified by parameters.
        if args.attribute in info:
            print("-" * 70)
            print("%-42s%-2s%-s" %
                  (args.attribute, ":", info[args.attribute]))
            print("-" * 70)
        else:
            print('Failure: attribute not found')
    else:
        print("-" * 70)
        for key in info:
            print("%-42s%-2s%-s" % (key, ":", info[key]))

        print("-" * 70)

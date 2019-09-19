# -*- coding:utf-8 -*-
import re
import os

'''
#=====================================================================
# @Method: Set uREST to support communication with iBMC in IPv4 mode..
# @command: setibmaipv4
# @Param:
# @author:
# @date: 2018.8.16
#=====================================================================
'''


def setprotocol_init(parser, parser_list):
    """
    #=================================================================
    #   @Method:  Register subcommands for reset iBMC.
    #   @Param:   parser, major command argparser
                  parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=================================================================
    """
    sub_parser = parser.add_parser('setprotocol',
                                   help='''Set uREST to support communication with iBMC in IPv4 mode.''')
    sub_parser.add_argument('-M', dest='CommunicationMethod', required=True,
                            help='''Communication method IPv6 or IPv4''', choices=['IPv4', 'IPv6'])
    sub_parser.add_argument('-I', dest='iBMCIp', required=False,
                            help='''User has configured iBMC ip''', )
    parser_list['setprotocol'] = sub_parser

    return 'setprotocol'


def edit_code(mode, bmc_ip):
    """
    Modify redfish_client.py
    :param mode:Communication mode
    :param bmc_ip:ip address
    :return:
    """
    try:
        old_mode = ""
        old_ip = ""
        cur_path = os.path.split(os.path.realpath(__file__))[0]
        pos = cur_path.rfind('scripts')
        rest_path = cur_path[0:pos]
        redfish_path = rest_path + 'redfish'
        file_path = redfish_path + '//redfish_client.py'
        f = open(file_path, 'r+')
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.find('ibmcmode =') != -1:
                old_mode = line.split("=")[1].strip()[1:-1]
                new_line = "ibmcmode = '%s'" % mode
                line_mode = line.replace(line.strip(), new_line)
                lines[index] = line_mode

            if line.find('ibmcip =') != -1:
                old_ip = line.split("=")[1].strip()[1:-1]
                new_line1 = "ibmcip = '%s'" % bmc_ip
                line_ip = line.replace(line.strip(), new_line1)
                lines[index] = line_ip
        f = open(file_path, 'w+')
        f.writelines(lines)
        f.close()
        return [old_mode, old_ip]
    except:
        print("Setting urest to communicate with BMA failed!")
        return None


def setprotocol(client, parser, args):
    """
    #==================================================================
    #   @Method:  Set iBMA to support communication with iBMC in IPv4 mode
    #   @Param:   client, RedfishClient object
    #             parser, subcommand argparser. Export error messages when parameters are incorrect.
    #             args, parameter list
    #   @Return:
    #   @author:
    #==================================================================
    """
    if parser is None or args is None:
        return None
    mode = args.CommunicationMethod
    bmc_ip = args.iBMCIp
    if mode == "IPv4":
        if bmc_ip is None:
            parser.error("The ip address cannot be empty. Please enter the IP address.")

        p = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not p.match(bmc_ip):
            parser.error("The IPv4 address format is incorrect. Please enter the correct IP address.")

    if args.CommunicationMethod == "IPv6":
        if bmc_ip is not None:
            parser.error("-I is not needed parameter.")
    # Detection interface
    url = "/redfish/v1"
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print('Success: successfully completed request')
    else:
        error_code = "0"
        if resp['status_code']:
            error_code = resp['status_code']
        print('Failure: error code ' + error_code)
        return None
    return resp

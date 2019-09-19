# -*- coding:utf-8 -*-

"""
Function:Get license information
Date:2018.12.12
"""


def getlicenseinfo_init(parser, parser_list):
    """
    :Function:Get license information subcommand
    :param parser:major command argparser
    :param parser_list:save subcommand parser list
    :return:
    """
    sub_parser = parser.add_parser('getlicenseinfo',
                                   help='''get license information''')

    parser_list['getlicenseinfo'] = sub_parser

    return 'getlicenseinfo'


def getlicenseinfo(client, parser, args):
    """
    :Function:get license information
    :param client:RedfishClient object
    :param parser:subcommand argparser. Export error messages when parameters are incorrect.
    :param args:parameter list
    :return:
    """
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/LicenseService" % slotid
    resp = client.get_resource(url)

    if resp is None:
        return None

    if resp['status_code'] == 200:
        print_resource(resp['resource'])

    elif resp['status_code'] == 404:
        print 'Failure: resource was not found'

    else:
        print "Failure: the request failed due to an internal service error"

    return resp


def recur_display(keyv, count):
    """
    :Function:Handle license information display matter
    :param keyv:response license information list or dict
    :param count:indentation times
    :return:
    """
    if isinstance(keyv, list):
        for lst in keyv:
            recur_display(lst, count)
    elif isinstance(keyv, dict):
        for dct in keyv:
            if not isinstance(keyv[dct], (list, dict)):
                print " " * count * 2 + str(dct) + ':',
                print keyv[dct]
            else:
                print " " * count * 2 + str(dct) + ':'
                recur_display(keyv[dct], count+1)
    else:
        print " " * count * 2 + str(keyv)


def print_resource(info):
    """
    :Function:print license information
    :param info:response license infomation
    :return:
    """
    print "%s%-2s%s" % ("Id", ":", info['Id'])
    print "%s%-2s%s" % ("Name", ":", info['Name'])
    print "%s%-2s%s,%s" % ("Capability", ":", info['Capability'][0], info['Capability'][1])
    print "%s%-2s%s" % ("DeviceESN", ":", info['DeviceESN'])
    print "%s%-2s%s" % ("InstalledStatus", ":", info['InstalledStatus'])
    print "%s%-2s%s" % ("RevokeTicket", ":", info['RevokeTicket'])
    print "%s%-2s%s" % ("LicenseClass", ":", info['LicenseClass'])
    print "%s%-2s%s" % ("LicenseStatus", ":", info['LicenseStatus'])
    print "LicenseInfo:"
    recur_display(info['LicenseInfo'], 1)
    print "AlarmInfo:"
    recur_display(info['AlarmInfo'], 1)

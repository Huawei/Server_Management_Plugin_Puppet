#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function:Delete license
Date:2019.01.18
"""
from common_function import display_error_message


def deletelicense_init(parser, parser_list):
    """
    :Function:Install license subcommand
    :param parser:major command argparser
    :param parser_list:save subcommand parser list
    :return:
    """
    sub_parser = parser.add_parser('deletelicense', help='delete license')
    parser_list['deletelicense'] = sub_parser
    return 'deletelicense'


def deletelicense(client, parser, args):
    """
    :Function:Install license
    :param client:RedfishClient object
    :param parser:subcommand argparser. Export error messages when parameters are incorrect.
    :param args:parameter list
    :return:
    """
    # Parameter verification
    if parser is None or args is None:
        return None

    # Obtain the slot number.
    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/LicenseService" \
          "/Actions/LicenseService.DeleteLicense" % slotid
    resp = client.create_resource(url, {})

    if resp is None:
        return None

    status_code = resp['status_code']
    if status_code == 200:
        print('Success: successfully completed request')
    elif status_code == 404:
        print('Failure: resource was not found')
    elif status_code < 500:
        display_error_message(client, resp)
    else:
        print("Failure: the request failed due to an internal service error")

    return resp

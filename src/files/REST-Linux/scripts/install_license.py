#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function:Install license
Date:2018.12.13
"""
import sys
import time
from os import path

CONTENT_HELP = '''Content of license.
License text content if type is 'Text' while license file uri if type is 'URI'.
License file URI supports both bmc local path URI (only under the /tmp directory), 
and remote path URI (protocols HTTPS, SFTP, NFS, CIFS, and SCP are supported).
'''

TYPE_HELP = '''Content type.
Text: indicates the value is the license content.
URI: indicates the value is URI (local path or remote path).
'''


def installlicense_init(parser, parser_list):
    """
    :Function:Install license subcommand
    :param parser:major command argparser
    :param parser_list:save subcommand parser list
    :return:
    """
    sub_parser = parser.add_parser('installlicense',
                                   help='''install license''')
    sub_parser.add_argument('-S', dest='source',
                            default="iBMC",
                            choices=['iBMC', 'FusionDirector', 'eSight'],
                            help='License source, iBMC by default.')
    sub_parser.add_argument('-T', dest='type',
                            required=True,
                            choices=['URI', 'Text'],
                            help=TYPE_HELP)
    sub_parser.add_argument('-C', dest='content',
                            type=str,
                            required=True,
                            help=CONTENT_HELP)

    parser_list['installlicense'] = sub_parser
    return 'installlicense'


def installlicense(client, parser, args):
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

    url = "/redfish/v1/Managers/%s/LicenseService/Actions" \
          "/LicenseService.InstallLicense" % slotid
    # Construct payload.
    payload = {
        "FileSource": args.source,
        "Type": args.type,
    }

    # treat it as local file
    image_uri = args.content
    if path.isfile(image_uri):
        if str(image_uri).split('.')[-1] != 'xml':
            print('Failure: license file type should be \'.xml\'')
            return None
        if str(image_uri).split('/')[-1] == image_uri:
            filename = str(image_uri).split("\\")[-1]
        else:
            filename = str(image_uri).split('/')[-1]
        ret = upload_file(client, args, filename)
        if ret is False:
            return None
        payload['Content'] = ('/tmp/web/' + filename)
    else:
        protocol = None
        protocol_list = ['https', 'scp', 'sftp', 'cifs', 'nfs']
        for item in protocol_list:
            if image_uri.lower().startswith(item + "://"):
                lower_scheme = image_uri[:len(item)].lower()
                image_uri = lower_scheme + image_uri[len(item):]
                protocol = item.upper()
                payload['Content'] = (image_uri)
                break

        if protocol == None:
            message = ('Failure: File Uri %s is not exits or not supported, '
                       'file transfer protocols should be one of %s.')
            print (message % (image_uri, ','.join(protocol_list)))
            return None

    resp = client.create_resource(url, payload)

    if resp is None:
        return None

    if resp.get('status_code') == 202:
        time.sleep(1)
        resp_task = client.print_task_prog(resp)
        if resp_task is None:
            return None

        if resp_task == 'Exception':
            _resptaskparse(resp, client)
            sys.exit(144)
    else:
        _respparse(resp)

    return resp


def upload_file(client, args, filesname):
    '''
    #====================================================================================
    #   @Method:  upload file
    #   @Param:
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    url_upload = "/redfish/v1/UpdateService/FirmwareInventory"
    if not path.isfile(args.content):
        print ("Failure: the file does not exist")
        return False
    files = {
        'imgfile': (
            filesname, open(args.content, 'rb'),
            "multipart/form-data",
            {'user_name': client.username}
        )
    }

    if files is None:
        print ("Failure: the file open failed, please try again")
        return False

    resp = client.create_resource(url_upload, files=files, timeout=300)
    if resp is None:
        return False
    if resp['status_code'] != 202:
        print('Failure: Upload files failed. local file is only supported by iBMC version 2.97 or later')
        return False

    return None


def _resptaskparse(resp, client):
    """
    :Function:Handle exception task state
    :param client:RedfishClient object
    :param resp:response information
    :return:
    """

    taskid = resp['resource']['@odata.id']

    sys_resp = client.get_resource(taskid)
    if sys_resp is None:
        sys.exit(127)

    if sys_resp['status_code'] != 200:
        message = (sys_resp['message']['error']['@Message.ExtendedInfo'][0]['Message']).lower()
        print 'Failure: ' + message[:-1]
    else:
        # Return the task failure details
        message = (sys_resp['resource']['Messages']['Message']).lower()
        print 'Failure: ' + message[:-1]


def _respparse(resp):
    """
    :Function:Handle resp which is not 202
    :param resp:response information
    :return:
    """
    if resp['status_code'] == 200:
        print 'Success: successfully completed request'
        return None
    else:
        extended_info = resp['message']['error']['@Message.ExtendedInfo'][0]
        message_id = extended_info.get('MessageId')
        if 'Format' in message_id:
            print 'Failure: import failed due to invalid path'
        else:
            message = (extended_info.get('Message')).lower()
            print 'Failure: ' + message[:-1]

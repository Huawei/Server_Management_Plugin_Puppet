# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  set BIOS attributes
#
#   @author:
#   @Date:
#=========================================================================
'''

from json import load
from os import path


def setbios_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  BIOS menu item setting subcommand
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('setbios',
                                   help='''set BIOS setup attributes''')
    sub_parser.add_argument('-A', dest='attribute',
                            required=False,
                            help='''attribute name''')
    sub_parser.add_argument('-V', dest='value',
                            required=False,
                            help='''attribute value''')
    sub_parser.add_argument('-F', dest='file',
                            required=False,
                            help='''Set the local BIOS configuration file ''' + \
                                 '''in JSON format. The file contains the attributes ''' + \
                                 '''to be configured, for example, ''' + \
                                 '''{"attribute":"value", "attribute2":"value2" ...}''')

    parser_list['setbios'] = sub_parser

    return 'setbios'


def setbios(client, parser, args):
    '''
    #=====================================================================
    #   @Method: BIOS menu item setting subcommand processing function
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

    payload = parameter_processing(client, parser, args, slotid)
    if payload is None:
        return None

    resp = set_bios_info(client, payload, slotid)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print('Success: successfully completed request')
    else:
        error_message(resp['message']['error']['@Message.ExtendedInfo'],
                      resp['status_code'])

    return resp


def parameter_processing(client, parser, args, slotid):
    '''
    #=====================================================================
    #   @Method: parameter processing
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
                 slotid, slot number
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if (args.attribute and args.value) and (args.file is None):
        # attribute
        payload = payload_attribute(client, parser, args, slotid)
        if payload is None:
            return None

    elif (args.file) and (args.attribute is None and args.value is None):
        # file
        payload = payload_file(args)
        if payload is None:
            return None

    else:
        parser.error('parameter error. set -A and -V or set -F only')
        return None

    return payload


def payload_attribute(client, parser, args, slotid):
    '''
    #=====================================================================
    #   @Method: single BIOS item setting parameter processing
    #   @Param:  client, RedfishClient object
                 args, parameter list
                 slotid, slot number
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    resp = getbios_attribute(client, slotid)
    if resp is None:
        return None

    if args.attribute in resp:
        if isinstance(resp[args.attribute], int):
            # int
            try:
                value = int(args.value)
            except ValueError:
                parser.error("incorrect -V value")
                return None

            payload = {'Attributes': {args.attribute: value}}
            return payload

        # str
        payload = {'Attributes': {args.attribute: args.value}}
        return payload

    else:
        print('Failure: the attribute does not exist')

    return None


def getbios_attribute(client, slotid):
    '''
    #=====================================================================
    #   @Method: Obtain BIOS items.
    #   @Param:  client, RedfishClient object
                 slotid, slot number
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    url = "/redfish/v1/Systems/%s/Bios" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        info = resp['resource']['Attributes']
        return info
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    else:
        print("Failure: the request failed due to an internal service error")

    return None


def payload_file(args):
    '''
    #=====================================================================
    #   @Method: file BIOS item setting parameter processing
    #   @Param:  args, parameter list
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if not path.isfile(args.file):
        print("Failure: the file does not exist")
        return None

    try:
        file_obj = open(args.file, 'r')

        json_obj = load(file_obj)

    except ValueError:
        # JSON file format error
        print("Failure: JSON file format fail")
        return None
    except IOError:
        print("Failure: failed to open the file")
        return None

    payload = {'Attributes': json_obj}

    return payload


def set_bios_info(client, payload, slotid):
    '''
    #=====================================================================
    #   @Method: Set BIOS information.
    #   @Param:  client, RedfishClient object
    #            payload, request message
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    url = "/redfish/v1/Systems/%s/Bios/Settings" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        else:
            print("Failure: the request failed " + \
                  "due to an internal service error")
        return None

    resp = client.set_resource(url, payload, timeout=20)

    return resp


def error_message(message, error_code):
    '''
    #=====================================================================
    #   @Method:  error handling
    #   @Param:  error_code
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if error_code == 404:
        print("Failure: resource was not found")
    elif error_code == 400:
        messageid = message[0]['MessageId'].split('.')[-1]

        if messageid == 'PropertyModificationNeedPrivilege':
            print('Failure: you do not have the required permissions' + \
                  ' to perform this operation')
        elif messageid == 'MalformedJSON':
            print("Failure: JSON file format fail")
        elif messageid == 'PropertyUnknown':
            print("Failure: " + change_message(message[0]['Message']). \
                  replace('properties', 'attributes'))
        elif messageid == 'SettingPropertyFailed' \
                or messageid == 'PropertyValueTypeError' \
                or messageid == 'PropertyValueNotInList' \
                or messageid == 'PropertyImmutable' \
                or messageid == 'PropertyNotWritable' \
                or messageid == 'SettingPropertyFailedExtend' \
                or messageid == 'PropertyValueFormatError' \
                or messageid == 'ValueOutOfRange' \
                or messageid == 'PropertyScalarIncrement' \
                or messageid == 'SettingBootOrderFailed' \
                or messageid == 'PropertyModificationNotSupported':
            print("Failure: " + change_message(message[0]['Message']))
        else:
            print('Failure: the request failed' + \
                  ' due to an internal service error')
    else:
        print("Failure: the request failed due to an internal service error")


def change_message(messageinfo):
    '''
    #====================================================================================
    #   @Method:  changemessage
    #             Delete 'Attributes/'.  Replace 'property' with 'attribute'.
    #             Change strings with capitalized first letters and ended with '.' into strings with lowercase first letters and delete '.'.
    #   @Param:
    #   @Return:
    #   @author:
    #====================================================================================
    '''
    messageinfo = (messageinfo.replace('Attributes/', '')). \
        replace('property', 'attribute')

    if (messageinfo[0] >= 'A' and messageinfo[0] <= 'Z') \
            and (messageinfo[-1] == '.'):
        return messageinfo[0].lower() + messageinfo[1:-1]

    return messageinfo

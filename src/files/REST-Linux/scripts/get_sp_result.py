# -*- coding:utf-8 -*-

"""
#=========================================================================
#   @Description:  get SP information
#   @author:
#   @Date:
#=========================================================================
"""
from json import dumps
from os import path
FORMAT = '%-30s: %s'
FAIL = "Failure: insufficient permission for the file or file name " + \
       "not specified, perform this operation as system administrator/root," + \
       " or specify a file name"


def getspresult_init(parser, parser_list):
    """
    #=====================================================================
    #   @Method:  SP query subcommand
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author:
    #=====================================================================
    """
    sub_parser = parser.add_parser('getspresult',
                                   help='''get SP result information''')
    sub_parser.add_argument('-F', dest='file',
                            required=False,
                            help='''the loacl path of get the configuration file''')

    parser_list['getspresult'] = sub_parser

    return 'getspresult'


def getspresult(client, parser, args):
    """
    #=====================================================================
    #   @Method: SP query subcommand processing function
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
    #   @Return:
    #   @author:
    #   @date:  2017-8-30 09:04:14
    #=====================================================================
    """
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/SPService/SPResult/1" % slotid
    resp = client.get_resource(url)
    if resp is None or resp.get("status_code", None) is None:
        print 'no data available for the resource'
        return None
    if resp['status_code'] == 200:
        info = resp.get('resource', None)
        if info is None:
            print 'no data available for the resource'
            return resp
        del info["@odata.context"]
        del info["@odata.id"]
        del info["@odata.type"]
        if info.get('Actions', None) is not None:
            del info['Actions']
        del info['Name']
        del info['Id']
        len_info = len(info)
        if len_info == 0:
            print 'no data available for the resource'
            return resp
        if args.file is not None:
            if creat_res_file(args.file, info) is True:
                print 'Success: successfully completed request'
            else:
                return None
        else:
            print_info(info)

    elif resp['status_code'] == 404:
        print 'Failure: resource was not found'
    elif resp['status_code'] == 500:
        print "Failure: the request failed due to an internal service error"

    return resp


def creat_res_file(file_path, dict_info):
    """
    #=====================================================================
    #   @Method:  Export JSON files.
    #   @Param:   info, SP message dictionary
    #             args, command function parameter
    #   @Return:
    #   @author:
    #=====================================================================
    """
    # Check the path.
    file_dir = path.dirname(file_path)
    if path.exists(file_dir) is not True:
        print "Failure: the path does not exist"
        return False
    if path.isdir(file_path) is True:
        print "Failure: please specify a file name"
        return False
    try:
        file_obj = open(file_path, 'w+')

    except IOError:
        print FAIL
        return False

    json_obj = dumps(dict_info)
    file_obj.write(json_obj)
    file_obj.close()

    return True


def print_info(info):
    """
    #=====================================================================
    #   @Method:  print result
    #   @Param:   info，resource
    #   @Return:
    #   @author:
    #   @Modify: Print diagnostic progress.
    #=====================================================================
    """
    if info is None:
        print 'no data available for the resource'
        return

    for key in info:
        if key == "Upgrade":
            print "-" * 60
            print '[Upgrade]\n'
            print FORMAT % ('Progress', info['Upgrade']['Progress'])
            print FORMAT % ('Operation', info['Upgrade']['Operation'])

            # Display details.
            len_info = len(info['Upgrade']['Detail'])
            if len_info != 0:
                detail_info = info['Upgrade']['Detail']
                for i in range(0, len(detail_info)):
                    print "-" * 40
                    for detail_key in detail_info[i]:
                        print FORMAT % (detail_key, detail_info[i][detail_key])
                print "-" * 40

        if key == "OSInstall":
            print "-" * 60
            print '[OSInstall]\n'

            os_install = info['OSInstall']
            if len(os_install):
                print FORMAT % ('Progress', os_install['Progress'])
                results = os_install.get('Results', [])
                if len(results) == 1:
                    print FORMAT % ("OSType", results[0].get('OSType', ''))
                    print FORMAT % ("Status", results[0].get('Status', ''))
                    print FORMAT % ("Step", results[0].get('Step', ''))
                    print FORMAT % ("StartTime", results[0].get('StartTime', ''))
                    print FORMAT % ("EndTime", results[0].get('EndTime', ''))
                    print FORMAT % ("ErrorInfo", results[0].get('ErrorInfo', ''))

        if key == "RaidCfg":
            print "-" * 60
            print '[RaidCfg]\n'
            print FORMAT % ('Progress', info['RaidCfg']['Progress'])

            # Display details.
            len_info = len(info['RaidCfg']['Detail'])
            if len_info != 0:
                detail_info = info['RaidCfg']['Detail']
                for i in range(0, len(detail_info)):
                    print "-" * 40
                    for detail_key in detail_info[i]:
                        print FORMAT % (detail_key, detail_info[i][detail_key])
                print "-" * 40
        if key == "Diagnose":
            print "-" * 60
            print '[Diagnose]\n'
            print FORMAT % ('Operate', info['Diagnose']['Operate'])
            print FORMAT % ('DiagFinished', info['Diagnose']['DiagFinished'])

            # Display details.
            len_info = len(info['Diagnose']['Detail'])
            if len_info != 0:
                detail_info = info['Diagnose']['Detail']
                for i in range(0, len(detail_info)):
                    print "-" * 40
                    for detail_key in detail_info[i]:
                        print FORMAT % (detail_key, detail_info[i][detail_key])
                print "-" * 40

    print "-" * 60

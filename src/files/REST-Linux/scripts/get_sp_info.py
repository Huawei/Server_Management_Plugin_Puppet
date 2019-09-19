# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  get SP information
#    
#   @author: 
#   @Date: 
#=========================================================================
'''
FORMAT = '%-30s: %s'


def getspinfo_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  SP query subcommand
    #   @Param:   parser, major command argparser
    #                    parser_list, save subcommand parser list
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    sub_parser = parser.add_parser('getspinfo',
                                   help='''get SP service information''')

    parser_list['getspinfo'] = sub_parser

    return 'getspinfo'


def getspinfo(client, parser, args):
    '''
    #=====================================================================
    #   @Method: SP query subcommand processing function
    #   @Param:  client, RedfishClient object
                 parser, subcommand argparser. Export error messages when parameters are incorrect.
                 args, parameter list
    #   @Return:
    #   @author: 
    #   @date:  2017-11-14 09:04:14
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/SPService" % slotid
    resp = client.get_resource(url)
    if resp is None or resp.get("status_code", None) is None:
        print ('no data available for the resource')
        return None
    if resp['status_code'] == 200:
        info = resp.get('resource', None)
        if info is None:
            print ('no data available for the resource')
            return resp

        for key in info:
            if key == "SPStartEnabled" or key == "SysRestartDelaySeconds":
                print((FORMAT) % (key, info[key]))
            if key == "Version":
                print('')
                print('[%s]' % key)
                ver = info['Version']
                if ver is None:
                    continue
                for ver_key in ver:
                    print((FORMAT) % (ver_key, ver[ver_key]))

    elif resp['status_code'] == 404:
        print ('Failure: resource was not found')
    elif resp['status_code'] == 500:
        print ("Failure: the request failed due to an internal service error")

    return resp

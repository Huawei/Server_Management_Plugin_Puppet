# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  get user
#
#   @author:
#   @Date:
#=========================================================================
'''


def getuser_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Method:  get user information
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('getuser',
                                   help='''get user information''')
    sub_parser.add_argument('-N', dest='name',
                            required=False,
                            help='''user name''')

    parser_list['getuser'] = sub_parser

    return 'getuser'


def getuser(client, parser, args):
    '''
    #=====================================================================
    #   @Method: get user information
    #   @Param:
    #   @Return:
    #   @author:
    #   @date:   2017-8-30 09:16:34
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    url = "/redfish/v1/AccountService/Accounts"

    resp = client.get_resource(url)
    if (resp is None) or (resp['status_code'] != 200):
        error_message(client, resp)
        return resp

    resp = getuser_info(client, resp, args)
    return resp


def getuser_info(client, resp, args):
    '''
    #=====================================================================
    #   @Method:  getuser_info
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if args.name is None:
        for user_id in resp['resource']['Members']:
            url = user_id['@odata.id']
            user_resp = client.get_resource(url)
            if user_resp is None:
                return None
            if user_resp['status_code'] != 200:
                error_message(client, user_resp)
                return None

            print_resource(user_resp['resource'])

        print('-' * 55)
    else:
        for user_id in resp['resource']['Members']:
            url = user_id['@odata.id']
            user_resp = client.get_resource(url)
            if user_resp is None:
                return None
            if user_resp['status_code'] != 200:
                error_message(client, user_resp)
                return None

            if args.name == user_resp['resource']['UserName']:
                print_resource(user_resp['resource'])
                print('-' * 55)
                return user_resp

        print('Failure: the user does not exist')

    return None


def print_resource(info):
    '''
    #=====================================================================
    #   @Method:  print resource
    #   @Param:
    #   @Return:
    #   @author:
    #   @date: 2017-8-30 09:05:52
    #=====================================================================
    '''
    print('-' * 55)
    print("%-16s: %s" % ('UserId', info['Id']))
    print("%-16s: %s" % ('UserName', info['UserName']))
    print("%-16s: %s" % ('RoleId', info['RoleId']))
    print("%-16s: %s" % ('Locked', info['Locked']))
    print("%-16s: %s" % ('Enabled', info['Enabled']))
    print("%-16s: %s" % ('LoginInterface',
                         ','.join(info['Oem']['Huawei']['LoginInterface'])))


def error_message(client, resp):
    '''
    #=====================================================================
    #   @Method:  print error message
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if resp is None:
        return None

    if resp['status_code'] == 404:
        print('Failure: resource was not found')
    else:
        message = resp['message']['error']['@Message.ExtendedInfo']
        print("Failure: %s" % client.change_message(message[0]['Message']))

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

    # ���������û�
    url = "/redfish/v1/AccountService/Accounts"

    resp = client.get_resource(url)
    if (resp is None) or (resp['status_code'] != 200):
        error_message(client, resp)
        return resp

    resp = getuser_info(client, resp, args, parser)
    return resp


def getuser_info(client, resp, args, parser):
    '''
    #=====================================================================
    #   @Method:  getuser_info
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if args.name is None:
        # ��ӡ��������
        for user_id in resp['resource']['Members']:
            url = user_id['@odata.id']
            user_resp = client.get_resource(url)
            if user_resp is None:
                return None
            if user_resp['status_code'] != 200:
                error_message(client, user_resp)
                return user_resp

            print_resource(user_resp['resource'])

        print('-' * 60)
    else:
        # ��ӡһ��ָ������
        for user_id in resp['resource']['Members']:
            url = user_id['@odata.id']
            user_resp = client.get_resource(url)
            if user_resp is None:
                return None
            if user_resp['status_code'] != 200:
                error_message(client, user_resp)
                return user_resp

            if args.name == user_resp['resource']['UserName']:
                # �ҵ���ӡ����
                print_resource(user_resp['resource'])
                print('-' * 60)
                return user_resp

        # ������û���ҵ�
        parser.error('Failure: the user does not exist')

    return resp


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
    format_str = "%-28s%-2s%-s"
    print('-' * 60)
    print(format_str % ('UserId', ":", info['Id']))
    print(format_str % ('UserName', ":", info['UserName']))
    print(format_str % ('RoleId', ":", info['RoleId']))
    print(format_str % ('Locked', ":", info['Locked']))
    print(format_str % ('Enabled', ":", info['Enabled']))
    print(format_str % ('LoginInterface', ":",
                            ','.join(info['Oem']['Huawei']['LoginInterface'])))
    if 'AccountInsecurePromptEnabled' in info['Oem']['Huawei'].keys():
        print(format_str % ('AccountInsecurePromptEnabled', ":",
                                info['Oem']['Huawei']['AccountInsecurePromptEnabled']))


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

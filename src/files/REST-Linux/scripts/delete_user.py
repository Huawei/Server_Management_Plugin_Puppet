# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  delete user
#
#   @author:
#   @Date:
#=========================================================================
'''


def deleteuser_init(parser, parser_list):
    '''
    #=====================================================================
    #  @Method: delete user
    #  @Param:
    #  @Return:
    #  @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('deluser',
                                   help='''delete user''')
    sub_parser.add_argument('-N', dest='name', required=True,
                            help='''user to be deleted''')

    parser_list['deluser'] = sub_parser

    return 'deluser'


def deleteuser(client, parser, args):
    '''
    #=====================================================================
    #   @Method: delete user
    #   @Param:
    #   @Return:
    #   @author:
    #   @date:  2017-8-29 09:15:58
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    # �����û���Ϣ
    url = "/redfish/v1/AccountService/Accounts"

    resp = client.get_resource(url)
    if (resp is None) or (resp['status_code'] != 200):
        error_message(client, resp)
        return resp

    for user_id in resp['resource']['Members']:
        url = user_id['@odata.id']
        user_resp = client.get_resource(url)
        if user_resp is None:
            return None
        if user_resp['status_code'] != 200:
            error_message(client, user_resp)
            return None

        if args.name == user_resp['resource']['UserName']:
            # �ҵ�ָ���û� ɾ���˻�
            account_resp = delete_account(client, url)
            return account_resp

    # ������û���ҵ�
    print('Failure: the user does not exist')

    return None


def delete_account(client, url):
    '''
    #=====================================================================
    #   @Method: delete user account
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    resp = client.delete_resource(url)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print('Success: successfully completed request')
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    elif resp['status_code'] == 400:
        error_message(client,
                      resp['message']['error']['@Message.ExtendedInfo'])
    else:
        print("Failure: the request failed due to' + \
                        ' an internal service error")
    return resp


def error_message(client, message):
    '''
    #=====================================================================
    #   @Method:  print deleteuser error message
    #   @Param:
    #   @Return:
    #   @author:
    #   @date:   2017-8-29 09:15:14
    #=====================================================================
    '''
    if message is None:
        return None
    messageid = message[0]['MessageId'].split('.')[-1]

    if messageid == 'UserIsLoggingIn':
        print('Failure: the user has already logged in to the CLI')
    elif messageid == 'AccountForbidRemoved':
        print('Failure: emergency users and trap v3 users cannot be deleted')
    elif messageid == 'AccountNotModified':
        print('Failure: the account modification request failed')
    else:
        print('Failure: %s' % client.change_message(message[0]['Message']))

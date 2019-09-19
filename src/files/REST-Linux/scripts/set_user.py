# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  add user
#
#   @author:
#   @Date:
#=========================================================================
'''


def setuser_init(parser, parser_list):
    '''
    #=====================================================================
    #  @Method: add user
    #  @Param:
    #  @Return:
    #  @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('setuser', help='''update user''')
    sub_parser.add_argument('-N', dest='name', required=True,
                            help='''indicates the user to be updated''')
    sub_parser.add_argument('-NN', dest='newusername', required=False,
                            help='''new user name''')
    sub_parser.add_argument('-NP', dest='newpassword', required=False,
                            help='''new user password''')
    sub_parser.add_argument('-NR', dest='newrole', required=False,
                            choices=['Administrator', 'Operator', 'Commonuser', 'NoAccess', \
                                     'CustomRole1', 'CustomRole2', 'CustomRole3', 'CustomRole4'],
                            help='''new user role''')
    sub_parser.add_argument('-Locked', dest='locked', required=False,
                            action='store_true',
                            help='''set user locked''')
    sub_parser.add_argument('-Enabled', dest='enabled', required=False,
                            choices=['True', 'False'],
                            help='''user enabled status''')

    parser_list['setuser'] = sub_parser
    return 'setuser'


def setuser(client, parser, args):
    '''
    #=====================================================================
    #   @Method: add user
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    if parser is None and args is None:
        return None

    if args.newrole == 'NoAccess':
        args.newrole = 'Noaccess'

    payload = {
        "UserName": args.newusername,
        "Password": args.newpassword,
        "RoleId": args.newrole,
        "Locked": args.locked,
        "Enabled": args.enabled == 'True'
    }

    # remove None values
    payload = dict((k, v) for k, v in payload.iteritems() if v is not None)
    if len(payload) == 0:
        print("Failure: at least one update parameter must be set")

    url = "/redfish/v1/AccountService/Accounts"
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] != 200:
        error_message(client, resp)
        return resp

    resp = setuser_info(client, resp, args.name, payload)
    return resp


def setuser_info(client, resp, username, payload):
    '''
    #=====================================================================
    #   @Method:  set user
    #   @Param:
    #   @Return:
    #   @author:
    #=====================================================================
    '''
    for user_id in resp['resource']['Members']:
        url = user_id['@odata.id']
        user_resp = client.get_resource(url)
        if user_resp is None:
            return None
        if user_resp['status_code'] != 200:
            error_message(client, user_resp)
            return None

        if username == user_resp['resource']['UserName']:
            set_resp = client.set_resource(url, payload)
            if resp is None:
                return None

            if set_resp['status_code'] == 200:
                print('Success: successfully completed request')
                return set_resp

            error_message(client, set_resp)
            return set_resp
    print('Failure: user does not exist')
    return None


def error_message(client, message):
    '''
    #=====================================================================
    #   @Method:  print setuser error message
    #   @Param:
    #   @Return:
    #   @author:
    #   @date:   2017-8-30 09:14:26
    #=====================================================================
    '''
    messageid = message[0]['MessageId'].split('.')[-1]

    if messageid == 'CreateLimitReachedForResource':
        print('Failure: the number of users reached the limit')
    elif messageid == 'InvalidUserName':
        print("Failure: %s" % client.change_message(message[0]['Message']))
    elif messageid == 'ResourceAlreadyExists':
        print('Failure: the user already exists')
    elif messageid == 'PropertyValueExceedsMaxLength':
        print('Failure: the user name cannot exceed 16 characters')
    elif messageid == 'UserNameIsRestricted':
        print('Failure: the user name cannot be root')
    elif messageid == 'RoleIdIsRestricted':
        print('Failure: the root user must be an administrator')
    elif messageid == 'InvalidPasswordLength':
        print('Failure: invalid password length, ' + \
              'a valid password must contain 1 to 20 characters')
    elif messageid == 'PasswordComplexityCheckFail':
        print('Failure: the password does not ' + \
              'meet password complexity requirements')
    elif messageid == 'InvalidPassword':
        print('Failure: the password cannot be empty')
    elif messageid == 'PropertyValueNotInList':
        print("Failure: %s" % client.change_message(message[0]['Message']))
    elif messageid == 'AccountNotModified':
        print('Failure: the account modification request failed')
    elif messageid == 'EmergencyLoginUser':
        print('Failure: the role cannot be modified ' + \
              'because the user is an emergency login user')
    elif messageid == 'AccountNotModified':
        print('Failure: failed to set the role')
    elif messageid == 'PropertyModificationNeedPrivilege':
        print('Failure: you do not have the' + \
              ' required permissions to perform this operation')
    else:
        print("Failure: %s" % client.change_message(message[0]['Message']))

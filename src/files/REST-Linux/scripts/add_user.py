# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  add user
#
#   @author:
#   @Date:
#=========================================================================
'''


def adduser_init(parser, parser_list):
    '''
    #=====================================================================
    #  @Method: add user
    #  @Param:
    #  @Return:
    #  @author:
    #=====================================================================
    '''
    sub_parser = parser.add_parser('adduser',
                                   help='''add user''')
    sub_parser.add_argument('-N', dest='newusername', required=True,
                            help='''new user name''')
    sub_parser.add_argument('-P', dest='newpassword', required=True,
                            help='''new user password''')
    sub_parser.add_argument('-R', dest='role', required=True,
                            choices=['Administrator', 'Operator', 'Commonuser', 'NoAccess', \
                                     'CustomRole1', 'CustomRole2', 'CustomRole3', 'CustomRole4'],
                            help='''new user role''')

    parser_list['adduser'] = sub_parser

    return 'adduser'


def adduser(client, parser, args):
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

    url = "/redfish/v1/AccountService/Accounts"

    if args.role == 'NoAccess':
        args.role = 'Noaccess'

    payload = {
        "UserName": args.newusername,
        "Password": args.newpassword,
        "RoleId": args.role
    }

    resp = client.create_resource(url, payload)
    if resp is None:
        return None

    if resp['status_code'] == 201:
        print('Success: successfully completed request')
    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    elif resp['status_code'] == 400:
        error_message(client, resp['message']['error']['@Message.ExtendedInfo'])
    else:
        print("Failure: the request failed ' + \
                'due to an internal service error")
    return resp


def error_message(client, message):
    '''
    #=====================================================================
    #   @Method:  print adduser error message
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
    else:
        print("Failure: %s" % client.change_message(message[0]['Message']))

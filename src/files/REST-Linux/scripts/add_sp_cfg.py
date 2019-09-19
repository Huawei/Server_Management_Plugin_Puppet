# -*- coding:utf-8 -*-
'''
#=====================================================================
#   @Description:  create spservice config
#    
#   @Date: 
#=====================================================================
'''
from json import load
from os import path


def addspcfg_init(parser, parser_list):
    '''
    #=====================================================================
    #   @Description:  add sp config init
    #    
    #   
    #   @Date: 
    #=====================================================================
    '''

    sub_parser = parser.add_parser('addspcfg',
                                   help='''Create sp service config ''')
    # SPNetDev SPCfg is not implemented currently and is temporarily shielded.
    sub_parser.add_argument('-T', dest='ServiceType',
                            type=str, required=True,
                            choices=['SPNetDev', 'SPRAID', 'SPOSInstallPara'],
                            help='''Create service type''')
    sub_parser.add_argument('-F', dest='file',
                            required=True,
                            help='''Create sp the local configuration file ''' + \
                                 '''in JSON format. The file contains the attributes ''' + \
                                 '''to be configured, for example, ''' + \
                                 '''{"attribute":"value", "attribute2":"value2" ...}''')
    parser_list['addspcfg'] = sub_parser

    return 'addspcfg'


def addspcfg(client, parser, args):
    '''
    #=====================================================================
    #   @Description:  add csr
    #    
    #   @Date: 
    #=====================================================================
    '''
    if parser is None or args is None:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None
    # Distinguish the configuration to be delivered.
    url = "/redfish/v1/Managers/" + slotid + "/SPService/" + args.ServiceType
    resp = client.get_resource(url)
    if resp is None:
        return None
    elif resp['status_code'] != 200:
        if resp['status_code'] == 404:
            print('Failure: resource was not found')
        else:
            print('Failure: status code ' + str(resp['status_code']))
        return resp
    # Read the file content.

    payload = payload_file(args)
    if payload is None:
        return None
    if args.ServiceType == 'SPNetDev' or args.ServiceType == 'SPRAID':
        if payload.get('Id') is None:
            print("Failure: The file must contain the Id attribute")
            return None

    resp = client.create_resource(url, payload)
    # print(resp)
    if resp is None:
        return None

    elif resp['status_code'] == 201:
        print('Success: successfully completed request')

    else:
        error_message(resp['message']['error']['@Message.ExtendedInfo'],
                      resp['status_code'])
    return resp


def payload_file(args):
    '''
    #=====================================================================
    #   @Method: Read parameters from the file and process them.
    #   @Param:  args, parameter list
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    # print (args.file)
    file_obj = None
    if not path.isfile(args.file):
        print ("Failure: the file does not exist")
        return None
    try:
        file_obj = open(args.file, 'r')

        json_obj = load(file_obj)
    except ValueError:
        print ("Failure: JSON file format fail")
        return None
    except IOError:
        print ("Failure: failed to open the file")
        return None
    finally:
        if file_obj:
            file_obj.close()
    return json_obj


def error_message(message, error_code):
    '''
    #=====================================================================
    #   @Method: Handle errors.
    #   @Param:  error_code
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    if error_code == 404:
        print ("Failure: resource was not found")

    elif error_code == 400:
        messageid = message[0]['MessageId'].split('.')[-1]
        if messageid == "OperationNotSupported":
            print("Failure: this operation is not supported")
        elif messageid == "FileCountReachedLimit":
            mesg = "the number of configuration files has reached the limit"
            print("Failure: " + mesg)
        else:
            print ("Failure: " + change_message(message[0]['Message']))

    else:
        return None


def change_message(messageinfo):
    '''
    #====================================================================================
    #   @Method:  changemessage
    #             Change strings with capitalized first letters and ended with '.' into strings with lowercase first letters and delete '.'.
    #   @Param:   
    #   @Return:  
    #   @author: 
    #====================================================================================
    '''
    if (messageinfo[0] >= 'A' and messageinfo[0] <= 'Z') \
            and (messageinfo[-1] == '.'):
        return messageinfo[0].lower() + messageinfo[1:-1]

    else:
        return messageinfo

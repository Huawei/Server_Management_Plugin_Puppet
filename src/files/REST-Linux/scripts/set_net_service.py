# coding=utf-8

'''
#==========================================================================
# @Method: Set network service information commands.
# @command: setnetservice
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''

HELP_INFO = '''set network service'''
NMIS_INFO = '''indicates the protocol SSDP property NotifyMultica''' + \
            '''stIntervalSeconds range is 0 to 1800'''
RESP = ''
FAILURE_INFO = \
    'Failure: some of the settings failed. possible causes include the following:'


def setnetservice_init(parser, parser_list):
    '''
    #==========================================================================
    #   @Method:  Register and set network service information commands.
    #   @Param:   parser      major command argparser
                parser_list   save subcommand parser list
    #   @Return:  
    #   @author: 
    #   @date: 2017.7.22
    #==========================================================================
    '''
    sub_parser = parser.add_parser('setnetsvc', help=HELP_INFO)
    sub_parser.add_argument('-PRO', dest='Protocol',
                            choices=['HTTP', 'HTTPS', 'SNMP', 'VirtualMedia', 'IPMI', 'SSH', \
                                     'KVMIP', 'SSDP', 'VNC'],
                            required=True,
                            help='''set specify service information(State and Port value)''')
    sub_parser.add_argument('-S', dest='State', choices=['True', 'False'],
                            required=False, \
                            help='''indicates if the protocol property State is enabled ''' + \
                                 '''or disabled''')
    sub_parser.add_argument('-p', dest='Port', type=int, \
                            required=False, \
                            help='''indicates the protocol property port range is 1 to 65535''')
    sub_parser.add_argument('-NTTL', dest='NotifyTTL', type=int, \
                            required=False, \
                            help='''indicates the protocol SSDP property''' + \
                                 ''' NotifyTTL range is 1 to 255''')
    sub_parser.add_argument('-NIPS', dest='NotifyIPv6Scope', \
                            choices=['Link', 'Site', 'Organization'], \
                            required=False, \
                            help='''indicates the protocol SSDP property NotifyIPv6Scope''')
    sub_parser.add_argument('-NMIS', dest='NotifyMulticastIntervalSeconds', \
                            required=False, type=int, help=NMIS_INFO)

    parser_list['setnetsvc'] = sub_parser

    return 'setnetsvc'


def check_args_rang(parser, args):
    '''
    #==========================================================================
    #   @Method:  Check the input parameter range.
    #   @Param:   parser;args;ps_name;slotid;payload                
    #   @Return:  False: The input parameter is incorrect. True: The input parameter is correct.
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    if args.Port is not None:
        if args.Port > 65535 or args.Port < 1:
            parser.error('''argument -p: invalid choice: '%s' (''' % \
                         args.Port + '''choose from '1' to '65535')''')
            return None
    elif args.NotifyTTL is not None:
        if args.NotifyTTL > 255 or args.NotifyTTL < 1:
            parser.error('''argument -NTTL: invalid choice: '%s' (''' % \
                         args.NotifyTTL + '''choose from '1' to '255')''')
            return None
    elif args.NotifyMulticastIntervalSeconds is not None:
        if args.NotifyMulticastIntervalSeconds > 1800 or \
                        args.NotifyMulticastIntervalSeconds < 0:
            parser.error('''argument -NIPS: invalid choice: '%s' (''' % \
                         args.NotifyMulticastIntervalSeconds + \
                         '''choose from '0' to '1800')''')

    return None


def check_args(parser, args):
    '''
    #==========================================================================
    #   @Method:  Check input parameters.
    #   @Param:   parser;args;ps_name;slotid;payload                
    #   @Return:  False: The input parameter is incorrect. True: The input parameter is correct.
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    # You must import the configured protocol type.
    if args.Protocol is None:
        parser.error('the -PRO parameter is required')
        return None
        # Check whether the parameters are in the specified ranges.
    else:
        check_args_rang(parser, args)
    # If the protocol type is non-SSDP, check whether mandatory parameters are lacked or whether unnecessary parameters are contained.
    if args.Protocol != 'SSDP':
        if (args.State or args.Port) is None:
            parser.error('at least another one parameter must' + \
                         ' be specified besides -PRO')
            return None
        if (args.NotifyTTL) is not None:
            parser.error('argument -NTTL: %s is not required for this protocol' \
                         % args.NotifyTTL)
        if (args.NotifyIPv6Scope) is not None:
            parser.error('argument -NIPS: %s is not required for this protocol' \
                         % args.NotifyIPv6Scope)
        if (args.NotifyMulticastIntervalSeconds) is not None:
            parser.error('argument -NMIS: %s is not required for this protocol' \
                         % args.NotifyMulticastIntervalSeconds)
    # If the protocol type is SSDP, check whether mandatory parameters are lacked.
    else:
        if (args.State or args.Port or args.NotifyTTL or \
                    args.NotifyIPv6Scope or args.NotifyMulticastIntervalSeconds) is None:
            parser.error('at least another one parameter must ' + \
                         'be specified besides -PRO')
            return None

    return True


def add_oem_payload(prol, args, payload):
    '''
    #==========================================================================
    #   @Method:  Combine the OEM request body.
    #   @Param:   args;payload                
    #   @Return:  False: The input parameter is incorrect. True: The input parameter is correct. 
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    if prol != 'Oem':
        return False
    else:
        # If the VNC protocol is used, add OEM attributes.
        payload['Oem']['Huawei']['VNC'] = {}
        if args.State is not None:
            if args.State == 'True':
                state = True
            if args.State == 'False':
                state = False
            payload['Oem']['Huawei']['VNC']['ProtocolEnabled'] = state
        # DTS2017082412035
        if args.Port is not None:
            payload['Oem']['Huawei']['VNC']['Port'] = args.Port
        else:
            return None
    return True


def add_payload(args, payload):
    '''
    #==========================================================================
    #   @Method:  Combine the request body.
    #   @Param:   parser;args;payload                
    #   @Return:  False: The input parameter is incorrect. True: The input parameter is correct.
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    for prol in payload:
        ret = add_oem_payload(prol, args, payload)
        # Add other protocol attributes.
        if ret is False:
            if args.State is not None:
                if args.State == 'True':
                    state = True
                if args.State == 'False':
                    state = False
                payload[prol]['ProtocolEnabled'] = state
            if args.Port is not None:
                payload[prol]['Port'] = args.Port
        else:
            pass
        # If the SSDP protocol is used, add the other three attributes.
        if args.Protocol == 'SSDP':
            if args.NotifyTTL is not None:
                payload[prol]['NotifyTTL'] = args.NotifyTTL
            if args.NotifyIPv6Scope is not None:
                payload[prol]['NotifyIPv6Scope'] = args.NotifyIPv6Scope
            if args.NotifyMulticastIntervalSeconds is not None:
                payload[prol]['NotifyMulticastIntervalSeconds'] = \
                    args.NotifyMulticastIntervalSeconds

    return


def prt_err(flg, msg):
    '''
    #==========================================================================
    #   @Method:  Display error information.
    #   @Param:   parser：   parser_list：                   
    #   @Return:  dict: Successful, 'resource', URL node information 
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    if flg > 1:
        print(("         %s") % msg)
    else:
        print(("%s: %s") % ('Failure', msg))
    return


def print_err_message(info):
    '''
    #==========================================================================
    #   @Method:  Display error information.
    #   @Param:   parser：   parser_list：                   
    #   @Return:  dict: Successful, 'resource', URL node information 
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    idx = 0
    if info is None:
        return None
        # If the number of array members in the error message array is greater than 0, multiple error messages exist.
    flag = len(info)
    if flag < 1:
        print('Success: successfully completed request')
    elif flag > 1:
        print(FAILURE_INFO)
    else:
        pass

    for idx in range(0, flag):
        # Insufficient permission
        if 'iBMC.1.0.PropertyModificationNeedPrivilege' == \
                info[idx]['MessageId'] or \
                        'Base.1.0.InsufficientPrivilege' == info[idx]['MessageId']:
            info[idx]['Message'] = \
                'you do not have the required permissions to perform this operation'
        # The attribute cannot be set.
        if 'iBMC.1.0.PropertyModificationNotSupported' == \
                info[idx]['MessageId']:
            info[idx]['Message'] = \
                'the server did not support the functionality required'
        # Duplicate ports
        elif 'iBMC.1.0.PortIdModificationFailed' == info[idx]['MessageId']:
            info[idx]['Message'] = info[idx]['RelatedProperties'][0] \
                                       .split('#/')[-1] + ' operation failed due to conflict port id'
        # The attribute value is out of range
        elif 'Base.1.0.PropertyValueNotInList' == info[idx]['MessageId']:
            info[idx]['Message'] = 'the property ' + info[idx] \
                ['RelatedProperties'][0].split('#/')[-1] + ' is out of range'
        # The attribute value type is incorrect.
        elif 'Base.1.0.PropertyValueTypeError' == info[idx]['MessageId']:
            info[idx]['Message'] = 'the property ' + \
                                   info[idx]['RelatedProperties'][0].split('#/')[-1] + ' type invalid'
        else:
            pass

        prt_err(flag, info[idx]['Message'])

    return


def check_result(resp):
    '''
    #==========================================================================
    #   @Method:  Check the setting results.
    #   @Param:   resp                  
    #   @Return:  None 
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    err_message = ''

    if resp is None:
        return None
    else:
        if resp['status_code'] == 200:
            # Traverse keys. If errormessage exists, display error messages.
            for key in resp['resource']:
                if key == '@Message.ExtendedInfo':
                    err_message = resp['resource'][key]

        # Traverse keys, and display error messages.
        elif resp['status_code'] == 400 or resp['status_code'] == 501:
            for key in resp['message']['error']:
                if key == '@Message.ExtendedInfo':
                    err_message = resp['message']['error'][key]

        else:
            err_message = None

        print_err_message(err_message)

    return None


def setnetservice(client, parser, args):
    '''
    #==========================================================================
    #   @Method:  Set the network service.
    #   @Param:   client:   parser: ; args: CLI parameter                  
    #   @Return:  dict: Successful, 'resource', URL node information
    #   @author:  
    #   @date: 2017.7.22
    #==========================================================================
    '''
    # Parameter check
    ret = check_args(parser, args)
    if ret is not True:
        return None

    slotid = client.get_slotid()
    if slotid is None:
        return None

    url = "/redfish/v1/Managers/%s/NetworkProtocol" % slotid
    resp = client.get_resource(url)
    if resp == None or resp.get("status_code", "") == "":
        return None

    if resp['status_code'] == 200:
        # Combine the request body.
        key = args.Protocol
        payload = {key: {}}
        huawei = {'Huawei': payload}
        oem = {'Oem': huawei}
        # If the VNC is used, add a request body for the OEM object; otherwise, add it for payload.
        if key == 'VNC':
            add_payload(args, oem)
            payload = oem
        else:
            add_payload(args, payload)

            # Invoke the set method to set values.
        resp_patch = client.set_resource(url, payload)
        # Check returned values and returned messages.
        check_result(resp_patch)

    elif resp['status_code'] == 404:
        print('Failure: resource was not found')

    return resp

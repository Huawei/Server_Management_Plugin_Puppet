# -*- coding:utf-8 -*-
'''
#==========================================================================
# @Method: Perform operations on virtual media.
# @command: operatevmm
# @Param: 
# @author: 
# @date: 2017.8.7
#==========================================================================
'''
import sys

HELP = "virtual media control operation path. only the URI \
connections using the Network File System (NFS) or common \
Internet file system (CIFS) protocols are supported. \
for example: \
protocol://[username:password@]IP[:port]/directory/filename"


def operatevmm_init(parser, parser_list):
    '''
    #====================================================================================
    # @Method: Register commands.
    # @Param: parser, parser_list
    # @Return:
    # @author: 
    #====================================================================================
    '''
    sub_parser = parser.add_parser('connectvmm',
                                   help='''connect or disconnect virtual media''')
    sub_parser.add_argument('-T', dest='Type',
                            type=str, required=True, choices=['Disconnect', 'Connect'],
                            help='''operation type''')
    sub_parser.add_argument('-i', dest='Image',
                            type=str, required=False, help=HELP)
    parser_list['connectvmm'] = sub_parser

    return 'connectvmm'


def operatevmm(client, parser, args):
    '''
    #====================================================================================
    # @Method: Command processing function
    # @Param:client, parser, args
    # @Return:
    # @author: 
    # @date: 2017.8.1 11:09
    #====================================================================================
    '''
    if parser is None and args is None:
        return None
    # Analyze parameters.
    ret = analyze_parameters(args, parser)
    if ret is None:
        return None
    resp_vmm = get_response(ret, client)
    return resp_vmm


def get_response(payload, client):
    '''
    #====================================================================================
    # @Method: Query response information.
    # @Param:payload,client,slotid
    # @Return:
    # @date: 2017.8.1 11:09
    #====================================================================================
    '''
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url_cd, resp = client.get_cd_info(client, slotid)
    if url_cd == "":
        return resp
    url = url_cd + "/Oem/Huawei/Actions/VirtualMedia.VmmControl"
    # Perform operations on virtual media.
    resp_vmm = client.create_resource(url, payload)
    if resp_vmm is None:
        return None
    ret = resp_vmm.get("status_code", "")
    if ret == 200:
        print('Success: successfully completed request')
    elif ret == 400:
        print('Failure: operation failed')
    elif ret == 404:
        print('Failure: resource was not found')
    elif ret == 202:
        # Query the progress.
        resp_vmm = query_progress(client, resp_vmm)
    return resp_vmm


def query_progress(client, resp_vmm):
    '''
    #====================================================================================
    # @Method: Query the progress.
    # @Param:payload,client,slotid
    # @date: 2017.8.1 11:09
    # @Return:
    #====================================================================================
    '''
    task_resp = client.print_task_prog(resp_vmm, 10)
    if task_resp == "Exception":
        uri = resp_vmm["resource"].get("@odata.id", "")
        get_rsp = client.get_resource(uri)
        if get_rsp is None:
            return None
        if get_rsp.get("status_code", "") == 200:
            message = get_rsp.get("resource", "")
            err_message = message.get("Messages", "").get("Message", "")
            err_message = ("%s%s" % (err_message[0].lower(), \
                                     err_message[1:len(err_message) - 1]))
            print('Failure: %s' % (err_message))
            sys.exit(144)
        elif get_rsp.get("status_code", "") == 404:
            print('Failure: resource was not found')
            return get_rsp
        else:
            return get_rsp
    return task_resp


def analyze_parameters(args, parser):
    '''
    #====================================================================================
    # @Method: Encapsulate the request body.
    # @Param:args,payload
    # @Return:
    # @date: 2017.8.1 11:09
    #====================================================================================
    '''
    payload = {}
    payload['VmmControlType'] = args.Type
    # URI parameters are required for connections.
    if args.Type == "Connect":
        if args.Image is None:
            parser.error('the following arguments are required: -i')
        else:
            payload['Image'] = args.Image
    # URI parameters must be removed for disconnections.
    if args.Type == "Disconnect":
        if args.Image is not None:
            parser.error('the following parameters are redundant: -i')

    return payload

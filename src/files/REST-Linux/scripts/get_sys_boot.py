#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=========================================================================
#   @Description:  get system boot information
#    
#   @Date: 
#=========================================================================
'''


def getsysboot_init(parser, parser_list):
    '''
    #=========================================================================
    #   @Description: get system boot information subcommand init
    #   @Method:  getsysboot_init
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    sub_parser = parser.add_parser('getsysboot',
                                   help='''get system boot information''')
    parser_list['getsysboot'] = sub_parser

    return 'getsysboot'


def _boottsequencev5tov3(inputs):
    '''
    #=========================================================================
    #   @Description:  get sequence
    #   @Method:  getsequence
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''
    if inputs == 'HardDiskDrive':
        return 'Hdd'
    if inputs == 'DVDROMDrive':
        return 'Cd'
    if inputs == 'PXE':
        return 'Pxe'
    if inputs == 'Others':
        return 'Others'


def _getsequence(oemhuawei, client, slotid):
    '''
    #=========================================================================
    #   @Description:  get sequence
    #   @Method:  getsequence
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''
    # v5
    url = "/redfish/v1/Systems/%s/Bios" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None
    if resp['status_code'] == 200:
        attributes = resp['resource']['Attributes']
        ouput = ''
        for i in range(0, 4):
            if i == 3:
                temp = _boottsequencev5tov3(attributes["BootTypeOrder%s" % i])
                ouput = ouput + temp
            else:
                temp = _boottsequencev5tov3(attributes["BootTypeOrder%s" % i])
                ouput = ouput + temp + ','

    else:
        sequence = oemhuawei['BootupSequence']
        ouput = ''
        for i in range(0, len(sequence)):
            if i == len(sequence) - 1:
                ouput = ouput + sequence[i]
            else:
                ouput = ouput + sequence[i] + ','

    return ouput


def getsysboot(client, parser, args):
    '''
    #=========================================================================
    #   @Description:  get system boot information
    #   @Method:  getstateless_init
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''
    if parser is None or args is None:
        return None

    slotid = client.get_slotid()

    if slotid is None:
        return None

    length = 35
    mformat = '%-*s:%s'

    url = "/redfish/v1/systems/%s" % slotid
    resp = client.get_resource(url)

    if resp is None:
        return None

    if resp['status_code'] == 200:
        target = resp['resource']['Boot']['BootSourceOverrideTarget']
        tenabled = resp['resource']['Boot']['BootSourceOverrideEnabled']
        mode = resp['resource']['Boot']['BootSourceOverrideMode']
        mnabled = ""

        if "BootModeChangeEnabled" in resp['resource']['Oem']['Huawei'].keys():
            mnabled = resp['resource']['Oem']['Huawei']['BootModeChangeEnabled']
        if "BootModeConfigOverIpmiEnabled" in resp['resource']['Oem']['Huawei'].keys():
            mnabled = resp['resource']['Oem']['Huawei']['BootModeConfigOverIpmiEnabled']

        seq = _getsequence(resp['resource']['Oem']['Huawei'], client, slotid)
        print(mformat %(length, 'BootSourceOverrideTarget', target))
        print(mformat %(length, 'BootSourceOverrideEnabled', tenabled))
        print(mformat %(length, 'BootSourceOverrideMode', mode))

        if "BootModeChangeEnabled" in resp['resource']['Oem']['Huawei'].keys():
            print(mformat % (length, 'BootModeChangeEnabled', mnabled))
        if "BootModeConfigOverIpmiEnabled" in resp['resource']['Oem']['Huawei'].keys():
            print(mformat % (length, 'BootModeConfigOverIpmiEnabled', mnabled))

        print(mformat %(length, 'BootupSequence', seq))
       
    return resp

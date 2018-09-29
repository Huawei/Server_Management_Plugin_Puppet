#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=========================================================================
#   @Description:  set system boot information
#    
#   @Date: 
#=========================================================================
'''


def setsysboot_init(parser, parser_list):
    '''
    #=========================================================================
    #   @Description:  set system boot information init
    #   @Method:  setsysboot_init
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    sub_parser = parser.add_parser('setsysboot',
                                   help='''set system boot information''')
    sub_parser.add_argument('-T', dest='target',
                            type=str, required=False,
                            help='''boot source override target''',
                            choices=['None', 'Pxe', 'Floppy', 'Cd', 'Hdd', 'BiosSetup'])
    sub_parser.add_argument('-TS', dest='tenabled',
                            type=str, required=False,
                            help='''boot source override Enabled''',
                            choices=['Once', 'Disabled', 'Continuous'])
    sub_parser.add_argument('-M', dest='mode',
                            type=str, required=False,
                            help='''boot source override mode''',
                            choices=['Legacy', 'UEFI'])
    sub_parser.add_argument('-MS', dest='menabled',
                            type=str, required=False,
                            help='''boot source override mode change enabled''',
                            choices=['True', 'False'])
    sub_parser.add_argument('-Q', dest='sequence', nargs='*',
                            type=str, required=False,
                            help='''system boot order,four parameters that are not duplicate \
        must be specified, example: -Q Cd Pxe Hdd Others ''')

    parser_list['setsysboot'] = sub_parser

    return 'setsysboot'


def _printferrormessages(k, msgs):
    '''
    #=========================================================================
    #   @Description:  _printf error messages
    #   @Method:  _printferrormessages
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''
    if msgs is None:
        return

    if k == 1:
        error = 'Failure: some of the settings failed. '
        error = error + 'possible causes include the following:'
        print(error)
        for i in range(0, len(msgs)):
            mgsagr = msgs[i]['RelatedProperties'][0]
            msg = ""

            if mgsagr == '#/Boot/BootSourceOverrideMode':
                msg = mgsagr.replace('#/Boot/', '')
            if "BootModeChangeEnabled" in mgsagr:
                msg = "BootModeChangeEnabled"
            print('         the property %s cannot be changed.' % msg)
    if k == 0:

        for i in range(0, len(msgs)):

            mgsagr = msgs[i]['RelatedProperties'][0]

            msg = ""
            if mgsagr == '#/Boot/BootSourceOverrideMode':
                msg = mgsagr.replace('#/Boot/', '')
            if "BootModeChangeEnabled" in mgsagr:
                msg = "BootModeChangeEnabled"

            if i == 0:
                print('Failure: the property %s cannot be change' % msg)
            else:
                print('         the property %s cannot be change' % msg)


def _sequencev3tov5(inputs):
    '''
    #=======================================================================
    #   @Description:  _sequencev3tov5
    #   @Method:  _sequencev3tov5
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=======================================================================
    '''
    if inputs == 'Hdd':
        return 'HardDiskDrive'
    if inputs == 'Cd':
        return 'DVDROMDrive'
    if inputs == 'Pxe':
        return 'PXE'
    if inputs == 'Others':
        return 'Others'


def _checkbootsequence(sequence):
    '''
    #=======================================================================
    #   @Description:  set boot sequence
    #   @Method:  _setbootsequence
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    if len(sequence) != 4:
        return False

    cddvd = False
    hdd = False
    pxe = False
    other = False

    for i in range(0, 4):
        if sequence[i] == 'Cd':
            cddvd = True
        if sequence[i] == 'Hdd':
            hdd = True
        if sequence[i] == 'Pxe':
            pxe = True
        if sequence[i] == 'Others':
            other = True

    if cddvd != True or hdd != True or pxe != True or other != True:
        return False

    return True


def _setbootsequence(payload, client, slotid, sequence):
    '''
    #=========================================================================
    #   @Description:  set boot sequence
    #   @Method:  _setbootsequence
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    if _checkbootsequence(sequence) == False:
        print('Failure: four parameters that are not duplicate ' + \
              'must be specified for the system boot order.')
        return False

    url = "/redfish/v1/Systems/%s/Bios/Settings" % slotid
    resp = client.get_resource(url)

    if resp.get('status_code') == 200:

        attributes = resp['resource']['Attributes']
        if attributes is None:
            attributes = {}

        payloads = {"Attributes": attributes}
        for i in range(0, 4):
            value = _sequencev3tov5(sequence[i])
            payloads['Attributes']["BootTypeOrder%s" % i] = value

        resp = client.set_resource(url, payloads, timeout=65)

        if resp is None:
            return False

        elif resp.get('status_code') == 200:
            return 'Success'
        else:
            print('Failure: unknown error ')
            return False

    else:
        value = [sequence[0], sequence[1], sequence[2], sequence[3]]
        payload['BootupSequence'] = value

        return True


def _makepayload(boot, huawei):
    '''
    #=========================================================================
    #   @Description:  set system boot
    #   @Method:  setsysboot
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    if boot != {} and huawei != {}:
        payload = {"Boot": boot, "Oem": {"Huawei": huawei}}
        return payload
    if boot != {} and huawei == {}:
        payload = {"Boot": boot}
        return payload
    if boot == {} and huawei != {}:
        payload = {"Oem": {"Huawei": huawei}}
        return payload

    return None


def _stringtobool(strs):
    '''
    #=========================================================================
    #   @Description:  string to boolean
    #   @Method:  _stringtobool
    #   @Param:   
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''
    if strs == 'False':
        return False
    else:
        return True


def setsysboot(client, parser, args):
    '''
    #=========================================================================
    #   @Description:  set system boot information
    #   @Method:  setsysboot
    #   @Param:  
    #   @Return:   
    #   @Date: 
    #=========================================================================
    '''

    slotid = client.get_slotid()

    if slotid is None:
        return None

    if args.target == None and args.tenabled == None and args.mode == None and \
                    args.menabled == None and args.sequence == None:
        parser.error('at least one parameter must be specified')
        return None

    boot = {}
    huawei = {}
    if args.target != None:
        boot['BootSourceOverrideTarget'] = args.target

    if args.tenabled != None:
        boot['BootSourceOverrideEnabled'] = args.tenabled

    if args.mode != None:
        boot['BootSourceOverrideMode'] = args.mode

    if args.menabled != None:
        huawei['BootModeChangeEnabled'] = _stringtobool(args.menabled)

    ret = None
    if args.sequence != None:
        ret = _setbootsequence(huawei, client, slotid, args.sequence)
        if ret != True and ret != 'Success':
            return None

    payload = _makepayload(boot, huawei)

    if payload is None and ret == 'Success':
        print('Success: successfully completed request')
        return None

    url = "/redfish/v1/systems/%s" % slotid
    resp = client.get_resource(url)
    if resp.get('status_code') != 200:
        return None

    resp = client.set_resource(url, payload)

    if resp is None:
        return None

    if resp['status_code'] == 200:
        # Some of the settings failed
        if resp['resource'].get('@Message.ExtendedInfo') != None:
            messages = resp['resource']['@Message.ExtendedInfo']
            _printferrormessages(1, messages)
        # Success
        else:
            print('Success: successfully completed request')
    else:
        # Failure

        if resp['status_code'] == 400:
            messages = resp['message']['error']['@Message.ExtendedInfo']
            _printferrormessages(0, messages)

    return None

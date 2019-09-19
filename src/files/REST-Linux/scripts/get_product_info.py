# -*- coding:utf-8 -*-

'''
#=========================================================================
#   @Description:  get product information
#    
#   @author: 
#   @Date: 
#=========================================================================
'''

def getproductinfo_init(parser, parser_list):
    '''
    #=====================================================================
    #  @Method: get product information
    #  @Param: 
    #  @Return:
    #  @author: 
    #=====================================================================
    '''    
    sub_parser = parser.add_parser('getproductinfo', 
                                    help = '''get product information''')
    
    parser_list['getproductinfo'] = sub_parser
    
    return 'getproductinfo'

def getproductinfo(client, parser, args):    
    '''
    #=====================================================================
    #   @Method: get product information
    #   @Param:  
    #   @Return:
    #   @author: 
    #=====================================================================
    ''' 
    if parser is None and args is None:
        return None
    
    slotid = client.get_slotid()
    if slotid is None:
        return None
    
    url = "/redfish/v1/Systems/%s" % slotid
    resp = client.get_resource(url)
    if resp is None:
        return None

    if resp['status_code'] == 200:
        print_resource(resp['resource'])

    elif resp['status_code'] == 404:
        print ('Failure: resource was not found')
    else:
        print ("Failure: the request failed due to an internal service error")

    return resp

def print_resource(info):
    '''
    #=====================================================================
    #   @Method:  print information
    #   @Param:   
    #   @Return:
    #   @author: 
    #=====================================================================
    '''
    
    print ("%-18s%-2s%-s" % ("Name", ":", info['Name']))
    print ("%-18s%-2s%-s" % ("AssetTag", ":", info['AssetTag']))
    print ("%-18s%-2s%-s" % ("Manufacturer", ":", info['Manufacturer']))
    print ("%-18s%-2s%-s" % ("Model", ":", info['Model']))
    print ("%-18s%-2s%-s" % ("SerialNumber", ":", info['SerialNumber']))
    print ("%-18s%-2s%-s" % ("UUID", ":", info['UUID']))
    print ("%-18s%-2s%-s" % ("HostName", ":", info['HostName']))
    print ("%-18s%-2s%-s" % ("ProductAlias", ":", 
                    info['Oem']['Huawei']['ProductAlias']))
    print ("%-18s%-2s%-s" % ("ProductVersion", ":", 
                    info['Oem']['Huawei']['ProductVersion']))
    print ("%-18s%-2s%-s" % \
                ("HostingRole", ":", ','.join(info['HostingRole'])))
    print ("%-18s%-2s%-s" % ("BiosVersion", ":", info['BiosVersion']))
    print ("%-18s%-2s%-s" % ("DeviceOwnerID", ":", 
                    info['Oem']['Huawei']['DeviceOwnerID']))
    print ("%-18s%-2s%-s" % ("DeviceSlotID", ":", 
                    info['Oem']['Huawei']['DeviceSlotID']))
    
    print ("%-18s%-2s%-s" % ("PowerState", ":", info['PowerState']))
    print ("\r\n%-18s" % ("[Status]"))
    print ("%-18s%-2s%-s" % ("State", ":", info['Status']['State']))
    print ("%-18s%-2s%-s" % ("Health", ":", info['Status']['Health']))

# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  RedfishClient Class
#
#   @author:
#   @Date:
#=========================================================================
'''
import json
import sys
import time
from os import path
from lib import requests

import getbmcinfo
import getbmctoken

PRINT_FORMAT = '%-17s%-2s%-20s'
flag_state = ['collectsel']


def error_info_check(r):
    """
    check error information
    :param r:
    :return:
    """
    ret = {'status_code': r.status_code,
           'message': json.loads(r.content.decode('utf8')),
           'headers': r.headers}
    try:
        message = ret['message']['error']['@Message.ExtendedInfo'][0]['Message']
        print("Failure: %s" % message)
    except Exception as e:
        print('Failure: status code ' + str(ret['status_code']))


def set_exit_code(resp):
    """
        exit code
        :param resp:
        :return:
    """
    status_dic = {201: 0, 202: 0, 200: 0, 400: 144, 401: 145, 403: 147, 404: 148, 405: 149, 409: 153, 500: 244,
                  501: 245}
    if resp.get('status_code') is not None:
        status_code = status_dic.get(resp['status_code'])
        sys.exit(status_code)
    else:
        sys.exit(0)


def get_error_info(ret):
    """
    print error information
    :return:
    """
    try:
        message = ret['message']['error']['@Message.ExtendedInfo']
        print("Failure: %s" % message[0]['Message'])
    except Exception as e:
        print('Failure: status code ' + str(ret['status_code']))


class RedfishClient():
    '''
    REST服务访问接口封装
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.host = ''
        self.port = ''
        self.username = ''
        self.password = ''
        self.timeout = None

        self.token = ''
        self.etag = ''
        self.headerhost = None
        self.auth = None

        requests.packages.urllib3.disable_warnings()

    def setself(self, host, port, username, password, timeout):
        '''
        #=====================================================================
        #   @Method:  设置带内hos，port,username,password值
        #   @Param:
        #   @Return:
        #   @author:
        #=====================================================================
        '''
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def request(self, method, resource, headers=None, stream=None,
                data=None, files=None, timeout=60):
        '''
        #=====================================================================
        #   @Method:  进行RESTful接口的HTTP请求
        #   @Param:   method, 为HTTP Method，如 ：'GET', 'POST', 'DELETE' 等
        #             resource, 请求的RESTful资源路径
        #             data，可选参数，请求Body部分携带的数据，dict类型
        #             headers, 可选参数，请求Header携带的数据，dict类型
        #             tmout,可选参数，http操作的超时时间,默认为10秒；
        #   @Return:  正常，返回response对象；异常，返回None。
        #   @author: 
        #=====================================================================
        '''
        # If the user sets the timeout parameter and passes the check,
        # the user timeout is set.
        # Otherwise, the default value is used.
        if self.timeout is not None:
            timeout = self.timeout

        if headers is None:
            if self.headerhost is not None:
                headers = {'X-Auth-Token': self.token,
                           'If-Match': self.etag,
                           'Host': self.headerhost}
            else:
                headers = {'If-Match': self.etag}

        if type(data) is dict:
            payload = json.dumps(data)
        else:
            payload = data

        if self.port is not None:
            url = r'https://%s:%d%s' % (self.host, self.port, resource)
        else:
            url = r'https://%s%s' % (self.host, resource)

        try:
            if method == 'POST':
                r = requests.post(url, data=payload, files=files, headers=headers,
                                  auth=self.auth, verify=False, timeout=timeout)
            elif method == 'GET':
                r = requests.get(url, data=payload, headers=headers,
                                 auth=self.auth, verify=False, timeout=timeout)
            elif method == 'DELETE':
                r = requests.delete(url, data=payload, headers=headers,
                                    auth=self.auth, verify=False, timeout=timeout)
            elif method == 'PATCH':
                r = requests.patch(url, data=payload, headers=headers,
                                   auth=self.auth, verify=False, timeout=timeout)
            else:
                sys.exit(127)
        except Exception as dummy_e:
            print('Failure: failed to establish a new connection to the host')
            sys.exit(127)

        if r.status_code == 401:
            self.err_401_proc(r)
            sys.exit(145)
        elif r.status_code == 403:
            if files is not None:
                print('Failure: insufficient privilege or server is doing another request')
            else:
                print('Failure: you do not have the required permissions to ' +
                      'perform this operation')
            sys.exit(147)
        elif r.status_code == 500:
            print('Failure: the request failed due to an internal ' +
                  'service error')
            sys.exit(244)
        elif r.status_code == 501:
            print('Failure: the server did not support the functionality ' +
                  'required')
            sys.exit(245)
        elif r.status_code == 409:
            error_info_check(r)
            sys.exit(153)
        elif r.status_code == 405:
            print('Failure: A request was made of a resource using a request method not supported by that resource.')
            sys.exit(149)
        else:
            return r

    def get_resource(self, url, headers=None, timeout=60):
        '''
        #=====================================================================
        #   @Method:  通过RESTful接口获取URL对应的信息。
        #   @Param:   url:资源路径；headers:请求头信息，默认为空时由request接口拼接
                      timeout:查询操作默认超时时间；
        #   @Return:  dict：成功，'status_code', 响应状态码200; 'resource', URL节点信息，
        #                   失败，'status_code', 响应状态码; 'message', 错误提示信息。
        #   @author:
        #=====================================================================
        '''
        r = self.request('GET', url, headers, timeout=timeout)
        if r is None:
            return None
        elif r.status_code == 200:
            ret = {'status_code': r.status_code,
                   'resource': json.loads(r.content.decode('utf8')),
                   'headers': r.headers}

            if 'ETag' in ret['headers'].keys():
                self.etag = ret['headers']['ETag']
            elif 'etag' in ret['headers'].keys():
                self.etag = ret['headers']['etag']
        else:
            try:
                ret = {'status_code': r.status_code,
                       'message': r.json(),
                       'headers': r.headers}
            except Exception as dummy_e:
                ret = {'status_code': r.status_code,
                       'message': r,
                       'headers': r.headers}
            if 'ETag' in ret['headers'].keys():
                self.etag = ret['headers']['ETag']
            elif 'etag' in ret['headers'].keys():
                self.etag = ret['headers']['etag']

        return ret

    def delete_resource(self, url, headers=None, timeout=60):
        '''
        #=====================================================================
        #   @Method:  delete_resource
        #   @Return:
        #   @Date: 20170829
        #=====================================================================
        '''
        r = self.request('DELETE', url, headers, timeout=timeout)
        if r is None:
            return None

        elif r.status_code == 200:
            ret = {'status_code': r.status_code,
                   'resource': json.loads(r.content.decode('utf8')),
                   'headers': r.headers}
        else:
            try:
                ret = {'status_code': r.status_code,
                       'message': r.json(),
                       'headers': r.headers}
            except Exception as dummy_e:
                ret = {'status_code': r.status_code,
                       'message': r,
                       'headers': r.headers}
        return ret

    def set_resource(self, url, payload, headers=None, timeout=60):
        '''
        #=====================================================================
        #   @Method:  set_resource
        #   @Param:   url
        #   @Return:  dict
        #   @Date: 20170830
        #=====================================================================
        '''
        resp = self.request('PATCH', url, headers=headers,
                            data=payload, timeout=timeout)
        if resp is None:
            return None
        elif resp.status_code == 200:

            ret = {'status_code': resp.status_code,
                   'resource': json.loads(resp.content.decode('utf8')),
                   'headers': resp.headers}

        else:
            try:
                ret = {'status_code': resp.status_code,
                       'message': resp.json(),
                       'headers': resp.headers}

            # set_resource exception
            except Exception as dummy_e:
                ret = {'status_code': resp.status_code,
                       'message': resp,
                       'headers': resp.headers}
        return ret

    def create_resource(self, url, payload=None, headers=None, files=None, timeout=60):
        '''
        #=====================================================================
        #   @Method:  create_resource
        #=====================================================================
        '''
        r = self.request('POST', url, headers=headers,
                         data=payload, files=files, timeout=timeout)

        if r is None:
            return None
        elif r.status_code in {201, 200, 202}:
            if url == "/redfish/v1/UpdateService/FirmwareInventory":
                resource = r.content
            elif "/Actions/Oem/Huawei/Manager.GeneralDownload" in url:
                resource = r.content.decode('utf8')
            else:
                resource = json.loads(r.content.decode('utf8'))
            ret = {'status_code': r.status_code,
                   'resource': resource,
                   'headers': r.headers}

        else:
            try:
                ret = {'status_code': r.status_code,
                       'message': r.json(),
                       'headers': r.headers}
            # create_resource exception
            except Exception as dummy_e:
                ret = {'status_code': r.status_code,
                       'message': r,
                       'headers': r.headers}
        return ret

    def get_managers_info(self, url="/redfish/v1/Managers/"):
        '''
        #=====================================================================
        #   @Method:  通过RESTful接口获取Managers资源信息。
        #   @Param:   url:资源路径；
        #   @Return:  dict
        #   @author:
        #=====================================================================
        '''
        return self.get_resource(url)

    def get_slotid(self):
        '''
        #=====================================================================
        #   @Method:  通过RESTful接口获取slotid。
        #   @Param:
        #   @Return:  成功：slotid值；
                      失败：None
        #   @author:
        #   @Modify: DTS2018112803983:Modify prompt information.
        #=====================================================================
        '''
        managers_info = self.get_managers_info()
        if managers_info is None:
            return None

        slotid = None
        if managers_info['status_code'] == 200:
            if managers_info.has_key('resource') and managers_info['resource'].has_key('Members'):
                if isinstance(managers_info['resource']['Members'], list):
                    if managers_info['resource']['Members'][0].has_key('@odata.id'):
                        slotid = managers_info['resource']['Members'] \
                            [0]['@odata.id'].split(r'/')[4]
            else:
                print("The slotid is not found.")
        else:
            get_error_info(managers_info)
            set_exit_code(managers_info)
        return slotid

    # Add flag parameter, when task is completed,return 'Completed' instead of exiting
    def print_task_prog(self, response=None, maxtime=10, flag=None):
        '''
        #=====================================================================
        #   @Method:  打印task进度。
        #   @Param:   response:task对应的资源信息；
        #             maxtime:默认的task运行的最大时间
        #   @Return:  成功：返回None
        #             失败：字符串Exception
        #   @author:
        #=====================================================================
        '''
        if response is None:
            return None  
        taskid = response['resource']['@odata.id']
        task_resp = self.get_resource(taskid, timeout=100)
        # DTS2017080403626
        if task_resp is None:
            return None
        elif task_resp['status_code'] != 200:
            print('Failure: failed to establish a new connection to the host')
            set_exit_code(task_resp)

        task_state = task_resp['resource']['TaskState']
        if task_state == 'Exception':
            return 'Exception'

        if task_state == 'Completed':
            if flag in flag_state:
                return 'Completed'
            else:
                print('Success: successfully completed request')
                sys.exit(0)

        step = float(100) / maxtime
        cur_perc = step

        # TaskPercentage有值，取TaskPercentage；TaskPercentage没值，按输入时间计算
        while task_state == 'Running':
            # task_percent = task_resp['resource']['Oem']\
            # ['Huawei']['TaskPercentage']
            # sys.stdout.write('                                            \r')
            # sys.stdout.flush()
            # if task_percent is not None:
            #     sys.stdout.write("Progress: %s\r" % task_percent)
            #     sys.stdout.flush()
            # else:
            #     cur_perc_int = int(cur_perc)
            #     if cur_perc_int >= 99:
            #         cur_perc_int = 99
            #     sys.stdout.write("Progress: %d%%\r" % cur_perc_int)
            #     sys.stdout.flush()
            #
            #     cur_perc = cur_perc + step

            time.sleep(1)
            task_resp = self.get_resource(taskid, timeout=100)
            # DTS2017080403626
            if task_resp is None:
                return None
            elif task_resp['status_code'] != 200:
                print('Failure: failed to establish a new '
                      'connection to the host')
                set_exit_code(task_resp)

            task_state = task_resp['resource']['TaskState']

        # sys.stdout.write('                                                \r')
        # sys.stdout.flush()
        if task_state == 'Exception':
            return 'Exception'

        if task_state == 'Completed':
            if flag in flag_state:
                return 'Completed'
            else:
                sys.stdout.write('Success: successfully completed request\n')
                sys.stdout.flush()
                sys.exit(0)
        return None

    def create_inner_session(self):
        '''
        #====================================================================================
        #   @Method:  获取带内Session
        #   @Param:
        #   @Return:
        #   @author:
        #====================================================================================
        '''

        self.token = getbmctoken.getinnersession()
        if self.token is not None:
            return True
        else:
            return False

    def delete_inner_session(self):
        '''
        #====================================================================================
        #   @Method:  删除带内Session
        #   @Param:
        #   @Return:
        #   @author:
        #====================================================================================
        '''
        self.token = None
        return True

    def set_inner_bmcinfo(self):
        '''
        #====================================================================================
        #   @Method:  设置带内ip，port值
        #   @Param:
        #   @Return:
        #   @author:
        #====================================================================================
        '''
        ibmcmode = 'IPv6'
        ibmcip = ''
        try:
            self.host = getbmcinfo.getinnerhost(ibmcmode, ibmcip)
            self.port = getbmcinfo.getinnerport()
            self.headerhost = getbmcinfo.getinnerheaderhost(ibmcmode, ibmcip)
        except Exception as dummy_e:
            print('Failure: failed to establish a new connection to the host')
            return False
        return True

    def check_storages(self, systems, storage, parser, str_args='-I'):
        '''
        #=====================================================================
        #   @Method: 对存储资源预先检查
        #   @Param:
        #   @Return:
        #   @author:
        #=====================================================================
        '''
        url = systems + "/Storages"
        resp = self.get_resource(url)
        if resp is None:
            return None

        elif resp['status_code'] != 200:
            if resp['status_code'] == 404:
                print('Failure: resource was not found')
            return resp
        # 看控制器url是否存在是否为以前版本
        elif resp['status_code'] == 200:
            if resp['resource']['Members@odata.count'] == 0:
                print('Failure: resource was not found')
                return resp
            for i in range(0, len(resp['resource']['Members'])):
                flag = False
                url = resp['resource']['Members'][i]['@odata.id']
                if url.find("RAIDStorage") > 0:
                    flag = True
                    break
            if flag:
                url = systems + storage
                resp = self.get_resource(url)
                if resp is None:
                    return None

                elif resp['status_code'] != 200:
                    if resp['status_code'] == 404:
                        str1 = "the value of "
                        error = str1 + str_args + " parameter is invalid"
                        parser.error(error)
                    return resp
            else:
                print('Failure: resource was not found')
                sys.exit(148)
        return resp

    def get_cd_info(self, client, slotid):
        '''
        #===========================================================
        # @Method: 查询cd信息
        # @Param:client, parser, args
        # @Return:
        # @date: 2017.8.1
        #===========================================================
        '''
        url_cd = "/redfish/v1/Managers/%s/VirtualMedia" % slotid
        resp = client.get_resource(url_cd)
        url = ""
        if resp is None:
            return url, None
        elif resp['status_code'] == 200:
            vmm = resp["resource"].get("Members", "")
            # 考虑到查询vmm信息，没有则是没有资源，跟404一样
            if len(vmm) == 0:
                print('Failure: resource was not found')
                return url, resp
            idx = 0
            while idx < len(vmm):
                cd_info = vmm[idx]["@odata.id"].split("/")
                if cd_info[-1] == "1" or cd_info[-1] == "CD":
                    url = vmm[idx]["@odata.id"]
                    break
                idx += 1
            # url是"",则没有VMM资源信息
            if url == "":
                print('Failure: resource was not found')
                return url, resp
        elif resp['status_code'] == 404:
            print('Failure: resource was not found')
            return url, resp
        return url, resp

    def set_auth(self):
        '''
        #======================================================================
        #   @Method:  设置basic auth信息
        #   @Param:
        #   @Return:
        #   @author:
        #======================================================================
        '''
        self.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        return True

    def err_401_proc(self, resp):
        '''
        #======================================================================
        #   @Method:  处理401错误
        #   @Param:
        #   @Return:
        #   @author:
        #   @Modify: DTS2018112803983:Modify the prompt for 'NoValidSession'.
        #======================================================================
        '''
        try:
            ret = {'status_code': resp.status_code,
                   'message': resp.json(),
                   'headers': resp.headers}

            message_id = ret['message']['error'] \
                ['@Message.ExtendedInfo'][0]['MessageId'].split(".")[3]

            if message_id == 'LoginFailed' \
                    or message_id == 'AuthorizationFailed':
                print('Failure: user name or password ' + \
                      'is incorrect, or your account is locked')
            elif message_id == 'NoAccess':
                print('Failure: the user gains no access')
            elif message_id == 'UserPasswordExpired':
                print('Failure: password overdued')
            elif message_id == 'UserLoginRestricted':
                print('Failure: login restricted')
            elif message_id == 'NoValidSession':
                print('Failure: Request timed out. Please try again later.')
            else:
                print('Failure: status code 401')

        except Exception as dummy_e:
            print('Failure: incomplete response from the server')

    def change_message(self, messageinfo):
        '''
        #====================================================================================
        #   @Method:  changemessage
        #
        #             将字串首字母大写以'.'结尾的 修改为首字母小写 删除'.'
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

    def get_os_firmware_or_driver(self, os_url):
        '''
        #=========================================================================
        #   @Description:  get_os_firmware_or_driver
        #
        #   @author:
        #   @Date:
        #=========================================================================
        '''
        resp_os_info = self.get_resource(os_url, timeout=60)

        if resp_os_info is None:
            return None
        if resp_os_info['status_code'] == 200:
            # 可升级固件/驱动信息
            print((PRINT_FORMAT) % ('Name', ':',
                                    resp_os_info['resource']['Name']))
            print((PRINT_FORMAT) % ('BDF', ':',
                                    resp_os_info['resource']['Oem']['Huawei']
                                    ['BDFNumber']['BDF']))
            print((PRINT_FORMAT) % ('RootBDF', ':',
                                    resp_os_info['resource']['Oem']['Huawei']
                                    ['BDFNumber']['RootBDF']))
            print((PRINT_FORMAT) % ('Model', ':',
                                    resp_os_info['resource']['Oem']['Huawei']['Model']))
            print((PRINT_FORMAT) % ('VendorID', ':',
                                    resp_os_info['resource']['Oem']['Huawei']['VendorID']))
            print((PRINT_FORMAT) % ('DeviceID', ':',
                                    resp_os_info['resource']['Oem']['Huawei']['DeviceID']))
            print((PRINT_FORMAT) % ('SubsystemVendorID', ':',
                                    resp_os_info['resource']['Oem']
                                    ['Huawei']['SubsystemVendorID']))
            print((PRINT_FORMAT) % ('SubsystemDeviceID', ':',
                                    resp_os_info['resource']['Oem']
                                    ['Huawei']['SubsystemDeviceID']))
            print((PRINT_FORMAT) % ('DeviceSilkScreen', ':',
                                    resp_os_info['resource']['DeviceSilkScreen']))
            print((PRINT_FORMAT) % ('DeviceLocation', ':',
                                    resp_os_info['resource']['DeviceLocation']))
            print('-' * 40)

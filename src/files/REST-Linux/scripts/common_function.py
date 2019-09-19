import sys

status_dic = {201: 0, 202: 0, 200: 0, 400: 144, 401: 145, 403: 147, 404: 148, 405: 149, 409: 153, 500: 244, 501: 245}


def set_exit_code(resp):
    """
    exit code
    :param resp:
    :return:
    """
    if resp is None:
        sys.exit(127)
    if resp.get('status_code') is not None:
        status_code = status_dic.get(resp['status_code'])
        sys.exit(status_code)
    else:
        sys.exit(0)


def display_error_message(client, resp):
    """
    #=====================================================================
    #   @Method:  print error message
    #   @Param:
    #   @Return:
    #   @author:
    #   @date:   2017-8-29 09:15:14
    #=====================================================================
    """
    messages = resp['message']['error']['@Message.ExtendedInfo']
    if messages is None or len(messages) == 0:
        return None

    message = messages[0]
    print(message)
    failure = client.change_message(message['Message'])
    resolution = message['Resolution']
    print('Failure: %s; Resolution: %s.' % (failure, resolution))
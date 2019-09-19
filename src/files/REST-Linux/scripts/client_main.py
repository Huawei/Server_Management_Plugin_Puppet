# -*- coding:utf-8 -*-
'''
#=========================================================================
#   @Description:  client main
#    
#   @author: 
#   @Date: 
#=========================================================================
'''
# DTS2017081104686
import common_function

__version__ = '113'

import os
import sys
from sys import path
import argparse
import signal
import set_protocol
import re
import platform

new_command_list = ["request"]


def clientmain(current_path, old_mode, old_ip):
    '''
    #=====================================================================
    #   @Method:  CLI entry function
    #   @Param:   cur_path, directory of the local file
    #   @Return:
    #   @author:
    #   @Modify: Exit code compatibility processing when the command format is incorrect.
    #   @Modify: DTS2018112813765: The exit code when pressing Ctrl + C is consistent with the system definition.
                 Delete the modified code.
    #=====================================================================
    '''

    try:
        command_flag = False
        # DTS2017080111254
        class CustomHelpFormatter(argparse.HelpFormatter):
            '''
            Custom help formatter
            '''

            # pylint: disable=W0212
            def _iter_indented_subactions(self, action):
                self._max_help_position = 30
                self._action_max_length = 30

                try:
                    get_subactions = action._get_subactions
                except AttributeError:
                    pass
                else:
                    self._indent()
                    if isinstance(action, argparse._SubParsersAction):
                        for subaction in sorted(get_subactions(), \
                                                key=lambda x: x.dest):
                            yield subaction
                    else:
                        for subaction in get_subactions():
                            yield subaction
                    self._dedent()

            # DTS2018121810742
            def _format_actions_usage(self, actions, groups):
                """
                :Function: Change '--timeout= TIMEOUT' in usage in the help information to '--timeout=TIMEOUT'.
                :param actions: helpactions
                :param groups: groups
                :return: text
                """
                text = super(CustomHelpFormatter, self)._format_actions_usage(actions, groups)
                if '--timeout= TIMEOUT' in text:
                    text = text.replace('--timeout= TIMEOUT', '--timeout=TIMEOUT', 1)
                return text

            # DTS2018121810742
            def _format_action(self, action):
                """
                :Function: Change '--timeout= TIMEOUT' in optional arguments in the help information to '--timeout=TIMEOUT '.
                :param action: helpaction
                :return: text
                """
                text = super(CustomHelpFormatter, self)._format_action(action)
                if '--timeout= TIMEOUT' in text:
                    text = text.replace('--timeout= TIMEOUT', '--timeout=TIMEOUT ', 1)
                return text

        try:
            # Construct argparser and add major command parameters.
            # DTS2017081104686
            parser = argparse.ArgumentParser(prog='urest',
                                             add_help=True, formatter_class=CustomHelpFormatter,
                                             description='urest version ' + \
                                                         '%s, which supports iBMC version 2.53 or later' % __version__)

            client = redfish_client.RedfishClient()
            resp = client.create_inner_session()

            if not resp:
                flag = True
            else:
                flag = False

            # DTS2017081104686
            parser.add_argument('-V', '--version', action='version',
                                version="urest version %s" % __version__)

            parser.add_argument('--error-code', dest='code', action='store_true',
                                help='Exit code. When an error occurs, the exit code is not 0.')
            # DTS2017080209079
            parser.add_argument('-H', dest='host', required=flag,
                                help='domain name, IPv4 address, ' + \
                                     'or [IPv6 address]')
            parser.add_argument('-p', dest='port', type=int,
                                help='port')

            parser.add_argument('-U', dest='username', required=flag,
                                help='local or LDAP username')

            parser.add_argument('-P', dest='password', required=flag,
                                help='password')

            # DTS2018121812592
            # Optimize the description of parameter timeout to help users understand the parameter.
            parser.add_argument('--timeout=', dest='timeout', type=int,
                                help='Timeout interval for connecting to the iBMC Redfish interface. '
                                     'In most cases, the timeout interval is 10 seconds by default.')

            subparsers = parser.add_subparsers(title='sub commands',
                                               dest='subcommand',
                                               help='sub-command help',
                                               metavar="sub command")

            met_dict = {}
            subparser_list = {}
            sub_cmd = ''
            files = os.listdir(current_path)

            # Traverse the current folder, and add subcommands and parameters based on the subcommand Python file names.
            for fil in files:
                if (not os.path.isdir(fil)) \
                        and (os.path.splitext(fil)[1] == '.py') \
                        and (fil != '__init__.py') and (fil != 'client_main.py') and (fil != 'common_function.py'):
                    mod = os.path.splitext(fil)[0]
                    mod_split = mod.split("_")
                    mod_join = ''.join(mod_split)
                    mod_init = mod_join + '_init'
                    mod_im = import_module(mod)
                    met = getattr(mod_im, mod_join)
                    met_init = getattr(mod_im, mod_init)
                    sub_cmd = met_init(subparsers, subparser_list)
                    met_dict[sub_cmd] = met

            try:
                args = parser.parse_args()
            except SystemExit, error:
                if "--error-code" in sys.argv:
                    command_flag = True
                sys.exit(error)

            if args.subcommand in new_command_list or args.code is True:
                command_flag = True

            try:
                # DTS2017080310099
                if args.host is not None and len(args.host) > 0:
                    if args.host[-1] == '#' \
                            or args.host[-1] == '?' \
                            or ('/' in args.host):
                        print('Failure: failed to establish a new connection ' + \
                              'to the host')

                        if command_flag:
                            sys.exit(127)
                        return None
                # DTS2018121812592
                # Optimization code
                if args.timeout is not None:
                    if '--timeout=%d' % args.timeout not in sys.argv \
                            or not (args.timeout >= 10 and args.timeout <= 1000):
                        parser.error('Parameter timeout is invalid. The timeout range 10-1000 seconds.')

                client.setself(args.host, args.port, args.username, args.password, args.timeout)

                if flag is False:
                    # Local OS access
                    if args.host is not None and args.username is not None \
                            and args.password is not None:
                        if args.subcommand == "setprotocol":
                            print ('Set protocol only supports in-band operation ')
                            if command_flag:
                                sys.exit(127)
                            return None
                        # out-band access.
                        resp = client.set_auth()
                    elif args.host is None and args.username is None \
                            and args.password is None:
                        # In-band access
                        resp = client.set_inner_bmcinfo()
                    else:
                        # exit status code:126
                        parser.error('-H, -U, -P and -p are not required for ' + \
                                     'local access. -H, -U and -P are mandatory for remote access')
                        return None
                else:
                    # Non-local OS
                    resp = client.set_auth()

                if not resp:
                    if args.subcommand == "setprotocol":
                        if old_mode != "" and old_ip != "":
                            set_protocol.edit_code(old_mode, old_ip)
                    if command_flag:
                        sys.exit(127)
                    return None

                # Execute corresponding processing functions according to the entered subcommands.
                if args.subcommand is not None:
                    met = met_dict.get(args.subcommand)
                    if met is not None:
                        print("*" * 45)
                        result = met(client, subparser_list[args.subcommand], args)
                        common_function.set_exit_code(result)
                        if args.subcommand == "setprotocol":
                            if result is None:
                                if old_mode != "" and old_ip != "":
                                    set_protocol.edit_code(old_mode, old_ip)
            except SystemExit, error:
                if command_flag:
                    sys.exit(error)
                return None
            finally:
                if flag is False and args.host is None \
                        and args.username is None and args.password is None:
                    client.delete_inner_session()
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, sys.exit(130))
    except (AttributeError, IOError, ImportError, IndexError, NameError, TypeError, ValueError) as e:
        print e
        if command_flag:
            sys.exit(2)
    except SystemExit, error:
        if command_flag:
            sys.exit(error)
        if "126" in str(error):
            if "Windows" in platform.system():
                sys.exit(0)
            else:
                sys.exit(2)


def edit_protocol():
    """
    Modify the urest and bmc communication code
    :return:
    """
    check_result = []
    p = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if len(sys.argv) >= 4 and sys.argv[1] == "setprotocol" and sys.argv[2] == "-M":
        if len(sys.argv) == 6 and sys.argv[3] == "IPv4" and sys.argv[4] == "-I" and p.match(sys.argv[5]):
            check_result = set_protocol.edit_code(sys.argv[3], sys.argv[5])
        if len(sys.argv) == 4 and sys.argv[3] == "IPv6":
            check_result = set_protocol.edit_code(sys.argv[3], '')
    if check_result is None:
        return None
    return check_result


if __name__ == '__main__':    
    # import logging
    # FORMAT = '%(asctime)-15s %(message)s'
    # logging.basicConfig(format=FORMAT)
    # root_log = logging.getLogger()
    # root_log.setLevel(logging.DEBUG)
    # requests_log = logging.getLogger('requests.packages.urllib3')
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    # Find the redfish directory according to the current file path, and import redfish_client.py.
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    pos = cur_path.rfind('scripts')
    rest_path = cur_path[0:pos]
    libs_path = rest_path + 'libs'
    path.insert(1, libs_path)
    redfish_path = rest_path + 'redfish'

    path.insert(1, redfish_path)
    check_command = edit_protocol()
    old_mode = ""
    old_ip = ""
    if check_command:
        old_mode = check_command[0]
        old_ip = check_command[1]
    import redfish_client
    from lib.importlib import import_module

    clientmain(cur_path, old_mode, old_ip)
    
    # delegate system built in print function
    # error_occur = False
    # sys.stdout, sys.stderr = print_buffer, print_buffer
    # try:
    #     clientmain(cur_path)
    # except:
    #     error_occur = True
    # finally:
    #     sys.stdout, sys.stderr = sys_stdout, sys_stderr
    #     # reset system built in print function
    #     buffer_content = print_buffer.getvalue()
    #     output = buffer_content.lower().strip()

    #     if error_occur or output.startswith("failure:"):
    #         sys.stderr.write(buffer_content)
    #         exit(-1)

    #     # if output.startswith("success:"):
    #     #     sys.stdout.write(buffer_content)
    #     #     exit(0)

    #     sys.stdout.write(buffer_content)
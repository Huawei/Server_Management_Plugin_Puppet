# -*- coding:utf-8 -*-
"""
#=========================================================================
#   @Description:  client main
#
#   @author:
#   @Date:
#=========================================================================
"""
import StringIO
import argparse
import os
import signal
import sys
from sys import path

# DTS2017081104686
__version__ = '107'

def clientmain(current_path):
    '''
    #=====================================================================
    #   @Method:  CLI entry function
    #   @Param:   cur_path, directory of the local file
    #   @Return:
    #   @author: 
    #=====================================================================
    '''

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

    try:
        # Construct argparser and add major command parameters.
        # DTS2017081104686
        parser = argparse.ArgumentParser(prog='rest',
                                         add_help=True, formatter_class=CustomHelpFormatter,
                                         description='rest version ' + \
                                                     '%s, which supports iBMC version 2.97 or later' % __version__)

        client = redfish_client.RedfishClient()
        resp = client.create_inner_session()

        if resp == False:
            flag = True
        else:
            flag = False

        # DTS2017081104686
        parser.add_argument('-V', '--version', action='version',
                            version="rest version %s" % __version__)
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
                    and (fil != '__init__.py') and (fil != 'client_main.py'):
                mod = os.path.splitext(fil)[0]
                mod_split = mod.split("_")
                mod_join = ''.join(mod_split)
                mod_init = mod_join + '_init'
                mod_im = import_module(mod)
                met = getattr(mod_im, mod_join)
                met_init = getattr(mod_im, mod_init)
                sub_cmd = met_init(subparsers, subparser_list)
                met_dict[sub_cmd] = met

        args = parser.parse_args()

        # DTS2017080310099
        if args.host is not None and len(args.host) > 0:
            if args.host[-1] == '#' \
                    or args.host[-1] == '?' \
                    or ('/' in args.host) is True:
                print('Failure: failed to establish a new connection ' + \
                      'to the host')
                return None

        client.setself(args.host, args.port, args.username, args.password)

        if flag is False:
            # Local OS access
            if args.host is None and args.username is None \
                    and args.password is None:
                # In-band access
                resp = client.set_inner_bmcinfo()
            elif args.host is not None and args.username is not None \
                    and args.password is not None:
                # The local OS requires the specified IP address, user name, and password for access.
                resp = client.set_auth()
            else:
                # The IP address, user name, and password are required for the local OS to access another BMC.
                parser.error('-H, -U, -P and -p are not required for ' + \
                             'local access. -H, -U and -P are mandatory for remote access')
                return None
        else:
            # Non-local OS
            resp = client.set_auth()

        if resp == False:
            return None

        # Execute corresponding processing functions according to the entered subcommands.
        if args.subcommand is not None:
            met = met_dict.get(args.subcommand)
            if met is not None:
                met(client, subparser_list[args.subcommand], args)

        if flag is False and args.host is None \
                and args.username is None and args.password is None:
            client.delete_inner_session()

    except KeyboardInterrupt:
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGINT, s)


print_buffer = StringIO.StringIO()
sys_stdout, sys_stderr = sys.stdout, sys.stderr

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

    # delegate system built in print function
    import redfish_client
    from lib.importlib import import_module

    error_occur = False
    sys.stdout, sys.stderr = print_buffer, print_buffer
    try:
        clientmain(cur_path)
    except:
        error_occur = True
    finally:
        sys.stdout, sys.stderr = sys_stdout, sys_stderr
        # reset system built in print function
        buffer_content = print_buffer.getvalue()
        output = buffer_content.lower().strip()

        if error_occur or output.startswith("failure:"):
            sys.stderr.write(buffer_content)
            exit(-1)

        sys.stdout.write(buffer_content)

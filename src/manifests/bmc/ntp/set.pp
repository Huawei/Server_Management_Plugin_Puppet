# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bmc::ntp::set (
  String $ibmc_username                       = 'username',
  String $ibmc_password                       = 'password',
  String $ibmc_host                           = '127.0.0.1',
  String $ibmc_port                           = '443',
  Optional[Boolean] $enabled                  = undef,
  Optional[Rest::NtpAddrOrigin] $addr_origin  = undef,
  Optional[String[1, 68]] $preferred_server   = undef,
  Optional[String[1, 68]] $alternate_server   = undef,
  Optional[Boolean] $auth_enabled             = undef,
  Optional[Integer[3, 17]] $min_interval      = undef,
  Optional[Integer[3, 17]] $max_interval      = undef,
) {

  # -M {Static,IPv4,IPv6}
  #                       NTP mode
  # -S {True,False}       NTP enable status
  # -PRE PREFERREDNTPSERVER
  #                       preferred NTP server address
  # -ALT ALTERNATENTPSERVER
  #                       alternative NTP server address
  # -MIN MINPOLLINGINTERVAL
  #                       minimum NTP synchronization interval. the value ranges
  #                       from 3 to 17
  # -MAX MAXPOLLINGINTERVAL
  #                       maximum NTP synchronization interval. the value ranges
  #                       from 3 to 17
  # -AUT {False,True}     enable auth status

  # init rest
  include ::rest

  # if defined($http_port) {
  #   $run_command = "$run_command --http-port $http_port"
  # }

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"


  $params = {
    '-S'   => $enabled ? {
      undef   => undef,
      default => bool2str($enabled, 'True', 'False')
    },
    '-M'   => $addr_origin,
    '-PRE' => $preferred_server,
    '-ALT' => $alternate_server,
    '-AUT' => $auth_enabled ? {
      undef   => undef,
      default => bool2str($auth_enabled, 'True', 'False')
    },
    '-MIN' => $min_interval,
    '-MAX' => $max_interval,
  }


  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setntp '${joined}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}

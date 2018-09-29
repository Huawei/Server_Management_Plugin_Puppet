# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bmc::service::set (
  String $ibmc_username                       = 'username',
  String $ibmc_password                       = 'password',
  String $ibmc_host                           = '127.0.0.1',
  String $ibmc_port                           = '443',
  Rest::Protocol $protocol                   = undef,
  Optional[Boolean] $enabled                  = undef,
  Optional[Integer[1, 65535]] $port           = undef,
  Optional[Integer[1, 255]] $notify_ttl       = undef,
  Optional[Rest::NotifyScope] $notify_scope  = undef,
  Optional[Integer[0, 1800]] $notify_interval = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}'"

  $params = {
    "-S"    => $enabled ? {
      undef   => undef,
      default => bool2str($enabled, 'True', 'False')
    },
    "-p"    => $port,
    "-NTTL" => $notify_ttl,
    "-NIPS" => $notify_scope,
    "-NMIS" => $notify_interval,
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setnetsvc -PRO ${protocol} '${joined}'"

  exec { "$title":
    command => "${script} ${command}",
    *       => $rest::service::context,
  }
}

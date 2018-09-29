# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::user::get (
  $ibmc_username                    = 'username',
  $ibmc_password                    = 'password',
  $ibmc_host                        = '127.0.0.1',
  $ibmc_port                        = '443',
  Optional[String[1, 16]] $username = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}'"
  $command = $username ? {
    undef   => "getuser",
    default => "getuser -N ${username}"
  }

  exec { "$title":
    command => "${script} ${command}",
    *       => $rest::service::context,
  }
}

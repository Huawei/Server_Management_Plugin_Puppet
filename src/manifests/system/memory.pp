# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::system::memory (
  $ibmc_username  = 'username',
  $ibmc_password  = 'password',
  $ibmc_host      = '127.0.0.1',
  $ibmc_port      = '443',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}'"
  $command = "getmemory"

  exec { "$title":
    command => "${script} ${command}",
    *       => $rest::service::context,
  }
  
}

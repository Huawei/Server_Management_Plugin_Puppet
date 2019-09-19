# A description of what this class does
#
# @summary Restart iBMC 
#
# @example
#   include rest::service
define rest::bmc::power::restart (
  String $ibmc_username  = 'username',
  String $ibmc_password  = 'password',
  String $ibmc_host      = '127.0.0.1',
  String $ibmc_port      = '443',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = 'bmcpowerctrl'

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}

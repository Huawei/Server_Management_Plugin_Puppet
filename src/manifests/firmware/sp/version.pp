# A description of what this class does
#
# @summary Get SP version
#
# @example
#   ../../../examples/firmware_sp_version_get.pp
#
define rest::firmware::sp::version (
  $ibmc_username  = 'username',
  $ibmc_password  = 'password',
  $ibmc_host      = '127.0.0.1',
  $ibmc_port      = '443',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = 'getspinfo'

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

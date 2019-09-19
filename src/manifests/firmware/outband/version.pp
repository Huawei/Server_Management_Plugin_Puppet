# A description of what this class does
#
# @summary Get Outband firmware version
#
# @example
#   ../../../examples/firmware_outband_version_get.pp
#
define rest::firmware::outband::version (
  $ibmc_username  = 'username',
  $ibmc_password  = 'password',
  $ibmc_host      = '127.0.0.1',
  $ibmc_port      = '443',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = 'getfw'

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

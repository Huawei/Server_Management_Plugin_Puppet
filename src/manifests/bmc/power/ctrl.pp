# A description of what this class does
#
# @summary Computer System Power Control
#
# @example
#   include rest::service
define rest::bmc::power::ctrl (
  String $ibmc_username        = 'username',
  String $ibmc_password        = 'password',
  String $ibmc_host            = '127.0.0.1',
  String $ibmc_port            = '443',
  Rest::ResetType $reset_type = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "syspowerctrl -T ${reset_type}"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

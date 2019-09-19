# A description of what this class does
#
# @summary Upgrade outband firmware
#
# @example
#   ../../../examples/firmware_outband_upgrade.pp
#
define rest::firmware::outband::upgrade (
  $ibmc_username     = 'username',
  $ibmc_password     = 'password',
  $ibmc_host         = '127.0.0.1',
  $ibmc_port         = '443',
  $firmware_file_uri = undef,
) {

  # init rest
  include ::rest


  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "upgradefw -i '${firmware_file_uri}'"

  warning("Upgrade outband firmware may takes a long time, please be patient.")

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
    timeout => 0,
  }

}

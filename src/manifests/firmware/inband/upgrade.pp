# A description of what this class does
#
# @summary Upgrade inband firmware
#
# @example
#   ../../../examples/firmware_inband_upgrade.pp
#
define rest::firmware::inband::upgrade (
  $ibmc_username                                     = 'username',
  $ibmc_password                                     = 'password',
  $ibmc_host                                         = '127.0.0.1',
  $ibmc_port                                         = '443',
  $firmware_file_uri                                 = undef,
  $signal_file_uri                                   = undef,
  Optional[Rest::UpgradeMode] $mode                  = 'Recover',
  Optional[Rest::UpgradeActiveMethod] $active_method = 'Restart',
) {

  # init rest
  include ::rest

  $params = {
    '-i'    => $firmware_file_uri,
    '-si'   => $signal_file_uri,
    '-T'    => 'Firmware',
    '-PARM' => 'all',
    '-M'    => $mode,
    '-ACT'  => $active_method,
  }

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "upgradesp '${joined}'"

  warning("Upgrade inband firmware may takes a long time, please be patient.")

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
    timeout => 0,
  }

}

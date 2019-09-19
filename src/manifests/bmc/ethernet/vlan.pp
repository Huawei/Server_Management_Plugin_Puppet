# A description of what this class does
#
# @summary Set VLAN properties
#
# @example
#   ../../examples/vlan_set.pp
#
define rest::bmc::ethernet::vlan (
  $ibmc_username                      = 'username',
  $ibmc_password                      = 'password',
  $ibmc_host                          = '127.0.0.1',
  $ibmc_port                          = '443',
  Optional[Boolean] $enabled          = undef,
  Optional[Integer[1, 4094]] $vlan_id = undef,
) {

  # init rest
  include ::rest
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-S' => $enabled ? {
      undef   => undef,
      default => bool2str($enabled, 'True', 'False'),
    },
    '-I'  => $vlan_id,
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setvlan '${joined}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

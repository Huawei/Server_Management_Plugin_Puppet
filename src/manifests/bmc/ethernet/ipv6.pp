# A description of what this class does
#
# @summary Set BMC IPV6 properties
#
# @example
#   ../../examples/ipv6_set.pp
define rest::bmc::ethernet::ipv6 (
  $ibmc_username                                       = 'username',
  $ibmc_password                                       = 'password',
  $ibmc_host                                           = '127.0.0.1',
  $ibmc_port                                           = '443',
  Optional[Stdlib::IP::Address::V6::Nosubnet] $ip      = undef,
  Optional[Stdlib::IP::Address::V6::Nosubnet] $gateway = undef,
  Optional[Rest::IPv6AddressOrigin] $address_origin    = undef,
  Optional[Integer[1, 65535]] $prefix_length           = undef,
) {

  # init rest
  include ::rest
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-IP' => $ip,
    '-G'  => $gateway,
    '-L'  => $prefix_length,
    '-M'  => $address_origin,
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setipv6 '${joined}'"


  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

# A description of what this class does
#
# @summary Set BMC IPV4 properties
#
# @example
#   ../../examples/ipv4_set.pp
#
define rest::bmc::ethernet::ipv4 (
  $ibmc_username                                       = 'username',
  $ibmc_password                                       = 'password',
  $ibmc_host                                           = '127.0.0.1',
  $ibmc_port                                           = '443',
  Optional[Stdlib::IP::Address::V4::Nosubnet] $ip      = undef,
  Optional[Stdlib::IP::Address::V4::Nosubnet] $gateway = undef,
  Optional[Stdlib::IP::Address::V4::Nosubnet] $mask    = undef,
  Optional[Rest::IPv4AddressOrigin] $address_origin    = undef,
) {

  # init rest
  include ::rest
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-IP'   => $ip,
    '-G'    => $gateway,
    '-MASK' => $mask,
    '-M'    => $address_origin,
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setipv4 '${joined}'"


  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

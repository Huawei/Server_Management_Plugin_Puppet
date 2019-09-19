# A description of what this class does
#
# @summary Set DNS/Domain properties
#
# @example
#   ../../examples/dns_set.pp
#
define rest::bmc::ethernet::dns (
  $ibmc_username                                   = 'username',
  $ibmc_password                                   = 'password',
  $ibmc_host                                       = '127.0.0.1',
  $ibmc_port                                       = '443',
  Optional[Rest::DNSAddressOrigin] $address_origin = undef,
  Optional[String[1, 64]] $hostname                = undef,
  Optional[String] $domain                         = undef,
  Optional[String] $preferred_server               = undef,
  Optional[String] $alternate_server               = undef,
) {

  # init rest
  include ::rest
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-M'   => $address_origin,
    '-H'   => $hostname,
    '-D'   => $domain,
    '-PRE' => $preferred_server,
    '-ALT' => $alternate_server,
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $command = "setdns '${joined}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

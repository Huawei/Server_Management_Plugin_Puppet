# A description of what this class does
#
# @summary Set Ethernet IP Version
#
# @example
#   ../../examples/ip_version_set.pp
#
define rest::bmc::ethernet::ipversion (
  $ibmc_username         = 'username',
  $ibmc_password         = 'password',
  $ibmc_host             = '127.0.0.1',
  $ibmc_port             = '443',
  Rest::IPVersion $value = undef,
) {

  # init rest
  include ::rest
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "setipversion -M '${value}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

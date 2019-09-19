# A description of what this class does
#
# @summary Set System Asset Tag
#
# @example
#   ../../../examples/asset_tag_set.pp
#
define rest::system::assettag::set (
  $ibmc_username       = 'username',
  $ibmc_password       = 'password',
  $ibmc_host           = '127.0.0.1',
  $ibmc_port           = '443',
  String[1, 48] $value = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "setproductinfo -Tag ${value}"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}

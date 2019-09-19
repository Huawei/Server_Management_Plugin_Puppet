# A description of what this class does
#
# @summary Install License
# @example ../../examples/license_install.pp
#
define rest::bmc::license::install (
  String $ibmc_username                 = 'username',
  String $ibmc_password                 = 'password',
  String $ibmc_host                     = '127.0.0.1',
  String $ibmc_port                     = '443',
  Optional[Rest::LicenseSource] $source = 'iBMC',
  Rest::ContentType $type               = undef,
  String $content                       = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "installlicense -S ${source} -T $type -C $content"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}

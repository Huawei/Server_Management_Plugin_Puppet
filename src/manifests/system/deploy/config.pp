# A description of what this class does
#
# @summary Set SP properties
#
# @example
#   ../../../examples/os_install_config.pp
#
define rest::system::deploy::config (
  $ibmc_username                      = 'username',
  $ibmc_password                      = 'password',
  $ibmc_host                          = '127.0.0.1',
  $ibmc_port                          = '443',
  String $os_deploy_config_file_path = undef,
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "addspcfg -T SPOSInstallPara -F '${os_deploy_config_file_path}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

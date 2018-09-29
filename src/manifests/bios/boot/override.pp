# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bios::boot::override (
  $ibmc_username              = 'username',
  $ibmc_password              = 'password',
  $ibmc_host                  = '127.0.0.1',
  $ibmc_port                  = '443',
  Rest::BootSource $target   = 'Pxe',
  Rest::BootEnabled $enabled = 'Once',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}'"
  $command = "setsysboot -T ${target} -TS ${enabled}"

  exec { "$title":
    command => "${script} ${command}",
    *       => $rest::service::context,
  }

}

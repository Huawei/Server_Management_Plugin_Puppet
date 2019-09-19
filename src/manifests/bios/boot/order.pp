# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bios::boot::order (
  String $ibmc_username           = 'username',
  String $ibmc_password           = 'password',
  String $ibmc_host               = '127.0.0.1',
  String $ibmc_port               = '443',
  Array[Rest::BootSeq] $sequence = undef,
) {

  # init rest
  include ::rest

  # convert sequence to string
  $joined = join($sequence, ' ')
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "setsysboot -Q ${joined}"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::user::set (
  $ibmc_username                       = 'username',
  $ibmc_password                       = 'password',
  $ibmc_host                           = '127.0.0.1',
  $ibmc_port                           = '443',
  String[1, 16] $username              = undef,
  Optional[String[1, 16]] $newusername = undef,
  Optional[String[1, 20]] $newpassword = undef,
  Optional[Rest::UserRole] $newrole    = undef,
  Optional[Boolean] $enabled           = undef,
  Optional[Boolean] $locked            = undef,
) {

  # init rest
  include ::rest

  $params = {
    "-NN"      => $newusername ? {
      undef   => undef,
      default => $newusername
    },
    "-NP"      => $newpassword ? {
      undef   => undef,
      default => $newpassword
    },
    "-NR"      => $newrole ? {
      undef   => undef,
      default => $newrole
    },
    "-Enabled"    => $enabled ? {
      undef   => undef,
      default => bool2str($enabled, 'True', 'False')
    },
  }
   
  $locked2  = $locked ? {
    undef   => '',
    default => "-Locked"
  }

  $joined = join(join_keys_to_values(delete_undef_values($params), "' '"), "' '")
  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}'"
  $command = "setuser -N ${username} '${joined}' ${locked2}"
  
  exec { "$title":
    command => "${script} ${command}",
    *       => $rest::service::context,
  }
}

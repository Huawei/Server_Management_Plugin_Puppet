# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
class rest::service() {

  include ::rest

  if $::osfamily == 'Debian' or $::osfamily == 'redhat' {
    $context = {
      path      => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
      cwd       => '/etc/puppet/modules/rest/files/REST-Linux/bin',
      provider  => 'shell',
      logoutput => true,
      loglevel  => notice,
    }
  }
  else {
    fail("OS '${::operatingsystem}' is not support by rest module")
  }
}

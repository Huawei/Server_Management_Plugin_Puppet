# Copy rest to client server
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::install
class rest::install {

  if $::osfamily == 'Debian' or $::osfamily == 'redhat' {

    # Ensure puppet module folder exists in client server
    $dirs = [
      '/etc/puppet',
      '/etc/puppet/modules',
      '/etc/puppet/modules/rest'
    ]
    file { $dirs:
      ensure => directory,
      mode   => '0755',
    }

    # Copy module files to client server
    file { '/etc/puppet/modules/rest/files':
      ensure  => directory,
      source  => 'puppet:///modules/rest',
      recurse => true,
      require => File['/etc/puppet/modules/rest'],
    }
  }
}

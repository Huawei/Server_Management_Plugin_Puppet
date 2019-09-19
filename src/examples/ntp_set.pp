# The baseline for module testing used by Puppet Inc. is that each manifest
# should have a corresponding test manifest that declares that class or defined
# type.
#
# Tests are then run by using puppet apply --noop (to check for compilation
# errors and view a log of events) or by fully applying the test in a virtual
# environment (to compare the resulting system state to the desired state).
#
# Learn more about module testing here:
# https://puppet.com/docs/puppet/latest/bgtm.html#testing-your-module
#
node default {

  # load hosts from hiera data-source
  $hosts = lookup('hosts')

  # addr_origin -> Enum["Static", "IPv4", "IPv6"]
  # max_interval & min_interval -> [3, 17]

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {
    rest::bmc::ntp::set { $hostname:
      ibmc_host        =>  $hostname,
      ibmc_username    =>  $data['username'],
      ibmc_password    =>  $data['password'],
      enabled          =>  true,
      addr_origin      =>  'IPv4',
      preferred_server =>  'pre.huawei.com',
      alternate_server =>  'alt.huawei.com',
      auth_enabled     =>  false,   # true | false
      min_interval     =>  3,   # value range [3, 17]
      max_interval     =>  17   # value range [3, 17]
    }
  }
}

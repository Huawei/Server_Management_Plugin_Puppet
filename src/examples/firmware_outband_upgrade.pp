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

  # tips: if upgrade CPLD and BIOS, it takes effect when OS power off.

  # $firmware_file_uri indicates the file uri of firmware update image file
  # firmware file uri should be a string of up to 256 characters. it supports:
  #   1. local file
  #   2. remote network file with protocols: HTTPS, SCP, SFTP, CIFS, NFS
  # $firmware_file_uri = "/home/ubuntu/2288H_V5_5288_V5-iBMC-V318.hpm"
  $firmware_file_uri = 'nfs://10.10.1.2/data/nfs/2288H_V5_5288_V5-iBMC-V318.hpm'

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {
    rest::firmware::outband::upgrade { $hostname:
      ibmc_host         => $hostname,
      ibmc_username     => $data['username'],
      ibmc_password     => $data['password'],
      firmware_file_uri => $firmware_file_uri
    }
  }
}

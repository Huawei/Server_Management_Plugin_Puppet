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


  # Indicates the file uri of firmware update firmware file.
  #   - The firmware upgrade file is in .ISO format. support only the CIFS and NFS protocols.
  #   - The URI cannot contain the following special characters: ||, ;, &&, $, |, >>, >, <
  $firmware_file_uri = 'nfs://10.10.1.2/data/nfs/SmartProvisioning-V113.ISO'

  # mode          -> Enum['Auto', 'Full', 'Recover', 'APP', 'Driver']
  # active_method -> Enum['Restart']

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {

    # Tips: Only V5 servers used with BIOS version later than 0.39 support this function.
    # transfered(upload) ISO files
    rest::firmware::sp::upgrade { $hostname:
      ibmc_host         => $hostname,
      ibmc_username     => $data['username'],
      ibmc_password     => $data['password'],
      firmware_file_uri => $firmware_file_uri,
      mode              => 'Recover', # optional
      active_method     => 'Restart', # optional
    }
  }
}

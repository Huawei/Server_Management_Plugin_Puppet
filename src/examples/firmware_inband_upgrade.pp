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
  #   - The firmware upgrade file is in .zip format.
  #   - It supports HTTPS, SFTP, NFS, CIFS, SCP file transfer protocols.
  #   - The URI cannot contain the following special characters: ||, ;, &&, $, |, >>, >, <
  $firmware_file_uri = 'nfs://10.10.1.2/data/nfs/NIC(X722)-Electrical-05022FTM-FW(3.33).zip'

  # Indicates the file path of the certificate file of the upgrade file.
  #   - Signal file should be in .asc format
  #   - it supports HTTPS, SFTP, NFS, CIFS, SCP file transfer protocols.
  #   - The URI cannot contain the following special characters: ||, ;, &&, $, |, >>, >, <
  $signal_file_uri = 'nfs://10.10.1.2/data/nfs/NIC(X722)-Electrical-05022FTM-FW(3.33).zip.asc'

  # mode          -> Enum['Auto', 'Full', 'Recover', 'APP', 'Driver']
  # active_method -> Enum['Restart']

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {

    # After system restart,
    # you can use `rest::firmware::sp::result` to query the firmware upgrade progress.
    # Check examples/firmware_sp_result_get.pp to get a overview.

    # Tips: Only V5 servers used with BIOS version later than 0.39 support this function.
    # transfered(upload) firmware files
    rest::firmware::inband::upgrade { $hostname:
      ibmc_host         => $hostname,
      ibmc_username     => $data['username'],
      ibmc_password     => $data['password'],
      firmware_file_uri => $firmware_file_uri,
      signal_file_uri   => $signal_file_uri,
      mode              => 'Recover', # optional
      active_method     => 'Restart', # optional
    } -> rest::firmware::sp::set { "${hostname}-set-sp":
      # transfered firmware files takes effect upon next system restart when SP Service start is enabled
      # Enable SP service start
      ibmc_host                    => $hostname,
      ibmc_username                => $data['username'],
      ibmc_password                => $data['password'],
      start_enabled                => true,
      system_restart_delay_seconds => 60,
    } -> rest::bmc::power::ctrl { "${hostname}-restart":
      # restart system to take effect
      ibmc_host     =>  $hostname,
      ibmc_username =>  $data['username'],
      ibmc_password =>  $data['password'],
      reset_type    =>  'ForceRestart',   # {On,ForceOff,GracefulShutdown,ForceRestart,Nmi,ForcePowerCycle}
    }
  }
}

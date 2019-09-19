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

  # Tips: This function is under license control. It can be used only with a license.
  # After system restart,
  # you can use `rest::firmware::sp::result` to query the firmware upgrade progress.
  # Check examples/firmware_sp_result_get.pp to get a overview.

  # config file path should be a local system file
  # it does not support network protocol file like nfs, cifs etc.
  $config_file_path = '/data/nfs/os_deploy_config_file_path.json'

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {
    rest::system::deploy::config { $hostname:
      ibmc_host                  => $hostname,
      ibmc_username              => $data['username'],
      ibmc_password              => $data['password'],
      os_deploy_config_file_path => $config_file_path,
    } -> rest::bmc::vmm::connect { "$hostname-vmm-connect":
      # connect virtual media to OS image
      ibmc_host     => $hostname,
      ibmc_username => $data['username'],
      ibmc_password => $data['password'],
      image_uri     => 'nfs://10.10.10.2/images/ubuntu.iso',
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
      reset_type    =>  'ForceRestart',     # {On,ForceOff,GracefulShutdown,ForceRestart,Nmi,ForcePowerCycle}
    }
  }
}

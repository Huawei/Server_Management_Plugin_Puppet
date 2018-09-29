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


  # alarm_severity -> Enum["Critical", "Major", "Minor", "Normal"]

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {
    rest::bmc::smtp::set { "$hostname":
      ibmc_host              => "$hostname",
      ibmc_username          => "${data['username']}",
      ibmc_password          => "${data['password']}",
      enabled                => true,
      server_addr            => "10.0.0.1",
      tls_enabled            => true,
      anon_enabled           => false,
      sender_addr            => "smtp@test.com",
      sender_password        => "${data['smtp-sender-pwd']}",
      sender_username        => "${data['smtp-sender-username']}",
      email_subject          => "Server Alert",
      email_subject_contains => [
        "HostName",
        "BoardSN",
        "ProductAssetTag",
      ],
      alarm_severity         => "Normal",
      receipt1               => {
        'enabled'       => true,
        'email_address' => 'example1@test.com',
        'description'   => 'example1'
      },
      receipt2               => {
        'enabled'       => true,
        'email_address' => 'example2@test.com',
        'description'   => 'example2'
      },
      receipt3               => {
        'enabled'       => false,
      },
      receipt4               => {
        'enabled'       => false,
      }
    }
  }
}

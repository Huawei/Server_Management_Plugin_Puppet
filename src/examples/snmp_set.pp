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

  # v3_auth_protocol -> Enum["MD5", "SHA1"]
  # v3_priv_protocol -> Enum["DES", "AES"]
  # trap_mode -> Enum["OID", "EventCode", "PreciseAlarm"]
  # trap_server_identity -> Enum["BoardSN", "ProductAssetTag", "HostName"]
  # trap_version -> Enum["V1", "V2C", "V3"]
  # trap_alarm_severity -> Enum["Critical", "Major", "Minor", "Normal"]

  # interate all hosts and get bios
  $hosts.each | String $hostname, Hash $data | {
    rest::bmc::snmp::set { "$hostname":
      ibmc_host             => "$hostname",
      ibmc_username         => "${data['username']}",
      ibmc_password         => "${data['password']}",
      v1_enabled            => true,
      v2_enabled            => true,
      long_password_enabled => false,
      rw_community_enabled  => true,
      rw_community          => "${data['read-write-community']}",
      ro_community          => "${data['read-only-community']}",
      v3_auth_protocol      => "MD5",
      v3_priv_protocol      => "AES",
      trap_enabled          => true,
      trap_version          => "V2C",
      trap_v3_user          => "root",
      trap_mode             => "OID",
      trap_server_identity  => "HostName",
      trap_community        => "${data['trap-community']}",
      trap_alarm_severity   => "Normal",
      trap_server1          => {
        "enabled" => true,
        "port"    => 101,
        "address" => "10.0.0.1",
      },
      trap_server2          => {
        "enabled" => true,
        "port"    => 102,
        "address" => "10.0.0.2",
      },
      trap_server3          => {
        "enabled" => false,
      },
      trap_server4          => {
        "enabled" => false,
      }
    }
  }
}

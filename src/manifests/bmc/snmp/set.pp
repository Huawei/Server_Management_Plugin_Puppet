# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bmc::snmp::set (
  String $ibmc_username                                        = 'username',
  String $ibmc_password                                        = 'password',
  String $ibmc_host                                            = '127.0.0.1',
  String $ibmc_port                                            = '443',
  Optional[Boolean] $v1_enabled                                = undef,
  Optional[Boolean] $v2_enabled                                = undef,
  Optional[Boolean] $long_password_enabled                     = undef,
  Optional[Boolean] $rw_community_enabled                      = undef,
  Optional[String[1, 32]] $rw_community                        = undef,
  Optional[String[1, 32]] $ro_community                        = undef,
  Optional[Rest::SnmpV3AuthProtocol] $v3_auth_protocol         = undef,
  Optional[Rest::SnmpV3PrivProtocol] $v3_priv_protocol         = undef,
  Optional[Boolean] $trap_enabled                              = undef,
  Optional[Rest::SnmpTrapVersion] $trap_version                = undef,
  Optional[String] $trap_v3_user                               = undef,
  Optional[Rest::SnmpTrapMode] $trap_mode                      = undef,
  Optional[Rest::SnmpTrapServerIdentity] $trap_server_identity = undef,
  Optional[String] $trap_community                             = undef,
  Optional[Rest::SnmpTrapAlarmSeverity] $trap_alarm_severity   = undef,
  Optional[Rest::SnmpTrapServer] $trap_server1                 = undef,
  Optional[Rest::SnmpTrapServer] $trap_server2                 = undef,
  Optional[Rest::SnmpTrapServer] $trap_server3                 = undef,
  Optional[Rest::SnmpTrapServer] $trap_server4                 = undef,
) {


  # init rest
  include ::rest

  # if defined($http_port) {
  #   $run_command = "$run_command --http-port $http_port"
  # }

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-V1'   => $v1_enabled ? {
      undef   => undef,
      default => bool2str($v1_enabled, 'True', 'False'),
    },
    '-V2'   => $v2_enabled ? {
      undef   => undef,
      default => bool2str($v2_enabled, 'True', 'False'),
    },
    '-LP'   => $long_password_enabled ? {
      undef   => undef,
      default => bool2str($long_password_enabled, 'True', 'False'),
    },
    '-RWE'  => $rw_community_enabled ? {
      undef   => undef,
      default => bool2str($rw_community_enabled, 'True', 'False'),
    },
    '-ROC'  => $ro_community,
    '-RWC'  => $rw_community,
    '-V3AP' => $v3_auth_protocol,
    '-V3EP' => $v3_priv_protocol,
    '-TS'   => $trap_enabled ? {
      undef   => undef,
      default => bool2str($trap_enabled, 'True', 'False'),
    },
    '-TV'   => $trap_version,
    '-TU'   => $trap_v3_user,
    '-TM'   => $trap_mode,
    '-TSI'  => $trap_server_identity,
    '-TC'   => $trap_community,
    '-TAS'  => $trap_alarm_severity,
  }

  $ts1 = $trap_server1 ? {
    undef   => {},
    default => {
      '-TS1-Enabled' => $trap_server1["enabled"] ? {
        undef   => undef,
        default => bool2str($trap_server1["enabled"], 'True', 'False'),
      },
      '-TS1-Port'    => $trap_server1["port"],
      '-TS1-Addr'    => $trap_server1["address"],
    }
  }

  $ts2 = $trap_server2 ? {
    undef   => {},
    default => {
      '-TS2-Enabled' => $trap_server2["enabled"] ? {
        undef   => undef,
        default => bool2str($trap_server2["enabled"], 'True', 'False'),
      },
      '-TS2-Port'    => $trap_server2["port"],
      '-TS2-Addr'    => $trap_server2["address"],
    }
  }

  $ts3 = $trap_server3 ? {
    undef   => {},
    default => {
      '-TS3-Enabled' => $trap_server3["enabled"] ? {
        undef   => undef,
        default => bool2str($trap_server3["enabled"], 'True', 'False'),
      },
      '-TS3-Port'    => $trap_server3["port"],
      '-TS3-Addr'    => $trap_server3["address"],
    }
  }

  $ts4 = $trap_server4 ? {
    undef   => {},
    default => {
      '-TS4-Enabled' => $trap_server4["enabled"] ? {
        undef   => undef,
        default => bool2str($trap_server4["enabled"], 'True', 'False'),
      },
      '-TS4-Port'    => $trap_server4["port"],
      '-TS4-Addr'    => $trap_server4["address"],
    }
  }

  $joined = join(join_keys_to_values(delete_undef_values($params + $ts1 + $ts2 + $ts3 + $ts4), "' '"), "' '")
  $command = "setsnmp '${joined}'"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}

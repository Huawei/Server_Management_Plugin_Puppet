# A description of what this class does
#
# @summary A short summary of the purpose of this class
#
# @example
#   include rest::service
define rest::bmc::smtp::set (
  String $ibmc_username                                                    = 'username',
  String $ibmc_password                                                    = 'password',
  String $ibmc_host                                                        = '127.0.0.1',
  String $ibmc_port                                                        = '443',
  Optional[Boolean] $enabled                                               = undef,
  Optional[String] $server_addr                                            = undef,
  Optional[Boolean] $tls_enabled                                           = undef,
  Optional[Boolean] $anon_enabled                                          = undef,
  Optional[String[1, 255]] $sender_addr                                    = undef,
  Optional[String[1, 50]] $sender_password                                 = undef,
  Optional[String[1, 64]] $sender_username                                 = undef,
  Optional[String[0, 255]] $email_subject                                  = undef,
  Optional[Array[Rest::SmtpSubjectContains, 0, 3]] $email_subject_contains = undef,
  Optional[Rest::SmtpAlarmSeverity] $alarm_severity                        = undef,
  Optional[Rest::SmtpReceipt] $receipt1                                    = undef,
  Optional[Rest::SmtpReceipt] $receipt2                                    = undef,
  Optional[Rest::SmtpReceipt] $receipt3                                    = undef,
  Optional[Rest::SmtpReceipt] $receipt4                                    = undef,
) {

  # init rest
  include ::rest

  # if defined($http_port) {
  #   $run_command = "$run_command --http-port $http_port"
  # }

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"

  $params = {
    '-S'      => $enabled ? {
      undef   => undef,
      default => bool2str($enabled, 'True', 'False')
    },
    '-SERVER' => $server_addr,
    '-TLS'    => $tls_enabled ? {
      undef   => undef,
      default => bool2str($tls_enabled, 'True', 'False')
    },
    '-ANON'   => $anon_enabled ? {
      undef   => undef,
      default => bool2str($anon_enabled, 'True', 'False')
    },
    '-SA'     => $sender_addr ? {
      undef   => undef,
      default => $sender_addr,
    },
    '-SP'     => $sender_password ? {
      undef   => undef,
      default => $sender_password,
    },
    '-SU'     => $sender_username ? {
      undef   => undef,
      default => $sender_username,
    },
    '-ES'     => $email_subject ? {
      undef   => undef,
      default => $email_subject,
    },
    '-AS'     => $alarm_severity,
  }

  $r1 = $receipt1 ? {
    undef   => {},
    default => {
      '-R1-Enabled' => $receipt1["enabled"] ? {
        undef   => undef,
        default => bool2str($receipt1["enabled"], 'True', 'False'),
      },
      '-R1-Addr'    => $receipt1["email_address"],
      '-R1-Desc'    => $receipt1["description"],
    }
  }

  $r2 = $receipt2 ? {
    undef   => {},
    default => {
      '-R2-Enabled' => $receipt2["enabled"] ? {
        undef   => undef,
        default => bool2str($receipt2["enabled"], 'True', 'False'),
      },
      '-R2-Addr'    => $receipt2["email_address"],
      '-R2-Desc'    => $receipt2["description"],
    }
  }

  $r3 = $receipt3 ? {
    undef   => {},
    default => {
      '-R3-Enabled' => $receipt3["enabled"] ? {
        undef   => undef,
        default => bool2str($receipt3["enabled"], 'True', 'False'),
      },
      '-R3-Addr'    => $receipt3["email_address"],
      '-R3-Desc'    => $receipt3["description"],
    }
  }

  $r4 = $receipt4 ? {
    undef   => {},
    default => {
      '-R4-Enabled' => $receipt4["enabled"] ? {
        undef   => undef,
        default => bool2str($receipt4["enabled"], 'True', 'False'),
      },
      '-R4-Addr'    => $receipt4["email_address"],
      '-R4-Desc'    => $receipt4["description"],
    }
  }

  $esc_join = join($email_subject_contains, ' ')
  $esc = empty($email_subject_contains) ? {
    true    => '',
    default =>  "-ESC ${esc_join}",
  }

  $joined = join(join_keys_to_values(delete_undef_values($params + $r1 + $r2 + $r3 + $r4), "' '"), "' '")
  $command = "setsmtp '${joined}' ${esc}"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}

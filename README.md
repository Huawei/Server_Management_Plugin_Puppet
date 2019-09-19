# rest

#### Table of Contents

1. [Description](#description)
1. [Setup - The basics of getting started with rest](#setup)
    * [What rest affects](#what-rest-affects)
    * [Setup requirements](#setup-requirements)
    * [Beginning with rest](#beginning-with-rest)
1. [Usage - Configuration options and additional functionality](#usage)
1. [Limitations - OS compatibility, etc.](#limitations)
1. [Development - Guide for contributing to the module](#development)

## Description

The Rest module is used to manage Huawei Servers with iBMC. This module provides
some Puppet resource types and samples manifests for various features of the Huawei iBMC.

## Setup

### What rest affects

The Rest module implements all puppet resource types with `Exec` module which execute python scripts(Rest-Linux) 
and those python scripts will access iBMC using Redfish API.

The Rest module will do:
* Install `Rest-Linux`(scripts folder) to `/etc/puppet/modules/rest/files`
* Install `stdlib>=5.0.0` module

### Setup Requirements 

* Puppet Master/Agent version >= 5.0.0
* Puppet Agent OS family should be `redhat`
* Python 2.7 should be in ENV path in Puppet Agent

### Beginning with rest

```bash
puppet module install serverplugin-rest
```

Check [Puppet Labs: Installing Modules](https://docs.puppetlabs.com/puppet/latest/reference/modules_installing.html) for more information.

## Usage

These Puppet resources are defined as part of `Rest` module:

* [`rest::bios::boot::get`](#restbiosbootget)
* [`rest::bios::boot::order`](#restbiosbootorder)
* [`rest::bios::boot::override`](#restbiosbootoverride)
* [`rest::bios::get`](#restbiosget)
* [`rest::bios::restore`](#restbiosrestore)
* [`rest::bios::set`](#restbiosset)
* [`rest::bmc::ethernet::dns`](#restbmcethernetdns)
* [`rest::bmc::ethernet::get`](#restbmcethernetget)
* [`rest::bmc::ethernet::ipv4`](#restbmcethernetipv4)
* [`rest::bmc::ethernet::ipv6`](#restbmcethernetipv6)
* [`rest::bmc::ethernet::ipversion`](#restbmcethernetipversion)
* [`rest::bmc::ethernet::vlan`](#restbmcethernetvlan)
* [`rest::bmc::license::delete`](#restbmclicensedelete)
* [`rest::bmc::license::export`](#restbmclicenseexport)
* [`rest::bmc::license::get`](#restbmclicenseget)
* [`rest::bmc::license::install`](#restbmclicenseinstall)
* [`rest::bmc::ntp::get`](#restbmcntpget)
* [`rest::bmc::ntp::set`](#restbmcntpset)
* [`rest::bmc::power::ctrl`](#restbmcpowerctrl)
* [`rest::bmc::power::restart`](#restbmcpowerrestart)
* [`rest::bmc::service::get`](#restbmcserviceget)
* [`rest::bmc::service::set`](#restbmcserviceset)
* [`rest::bmc::smtp::get`](#restbmcsmtpget)
* [`rest::bmc::smtp::set`](#restbmcsmtpset)
* [`rest::bmc::snmp::get`](#restbmcsnmpget)
* [`rest::bmc::snmp::set`](#restbmcsnmpset)
* [`rest::bmc::vmm::connect`](#restbmcvmmconnect)
* [`rest::bmc::vmm::disconnect`](#restbmcvmmdisconnect)
* [`rest::chassis::led::set`](#restchassisledset)
* [`rest::firmware::inband::upgrade`](#restfirmwareinbandupgrade)
* [`rest::firmware::inband::version`](#restfirmwareinbandversion)
* [`rest::firmware::outband::upgrade`](#restfirmwareoutbandupgrade)
* [`rest::firmware::outband::version`](#restfirmwareoutbandversion)
* [`rest::firmware::sp::result`](#restfirmwarespresult)
* [`rest::firmware::sp::set`](#restfirmwarespset)
* [`rest::firmware::sp::upgrade`](#restfirmwarespupgrade)
* [`rest::firmware::sp::version`](#restfirmwarespversion)
* [`rest::system::assettag::set`](#restsystemassettagset)
* [`rest::system::cpu::health`](#restsystemcpuhealth)
* [`rest::system::cpu`](#restsystemcpu)
* [`rest::system::deploy::config`](#restsystemdeployconfig)
* [`rest::system::drive::health`](#restsystemdrivehealth)
* [`rest::system::drive`](#restsystemdrive)
* [`rest::system::eth::get`](#restsystemethget)
* [`rest::system::fan::health`](#restsystemfanhealth)
* [`rest::system::get`](#restsystemget)
* [`rest::system::memory::health`](#restsystemmemoryhealth)
* [`rest::system::memory`](#restsystemmemory)
* [`rest::system::network_adapter::health`](#restsystemnetwork_adapterhealth)
* [`rest::system::network_adapter`](#restsystemnetwork_adapter)
* [`rest::system::power_supply::health`](#restsystempower_supplyhealth)
* [`rest::system::raid::health`](#restsystemraidhealth)
* [`rest::system::raid`](#restsystemraid)
* [`rest::user::add`](#restuseradd)
* [`rest::user::delete`](#restuserdelete)
* [`rest::user::get`](#restuserget)
* [`rest::user::set`](#restuserset)


### Common Attributes

All Rest resource type share those attributes:

| Attribute      | Description                              |
|----------------|------------------------------------------|
| ibmc_username  | iBMC login username                       |
| $ibmc_password | iBMC login password                       |
| $ibmc_host     | iBMC API access host, default `127.0.0.1` |
| $ibmc_port     | iBMC API access port, default `443`       |

Rest module resource types can visit iBMC API anywhere, resource type is free to run on anywhere.

### `rest::bios::boot::get`

Get boot settings.

**Attributes**

No additional attributes

**Examples Manifest**

[boot_get.pp](./examples/boot_get.pp)


### `rest::bios::boot::order`

Set boot order.

**Additional Attributes**

| Attribute | Type          | Description         |
|-----------|---------------|---------------------|
| sequence  | Array[String] | boot order sequence |

**Examples Manifest**

[boot_order.pp](./examples/boot_order.pp)

### `rest::bios::boot::override`

Set boot source override.

**Additional Attributes**

| Attribute | Type    | Description                |
|-----------|---------|----------------------------|
| target    | Enum    | boot source                |
| enabled   | Boolean | boot source override times |

**Examples Manifest**

[boot_override.pp](./examples/boot_override.pp)

### rest::bios::get

Get BIOS attribute.

**Additional Attributes**

| Attribute | Type   | Description                  |
|-----------|--------|------------------------------|
| attribute | String | indicates the BIOS attribute |

**Examples Manifest**

[bios_get.pp](./examples/bios_get.pp)

### rest::bios::restore

Restore BIOS attribute.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[bios_restore.pp](./examples/bios_restore.pp)


### rest::bios::set

Set BIOS attribute.

**Additional Attributes**

| Attribute | Type   | Description     |
|-----------|--------|-----------------|
| attribute | String | attribute name  |
| value     | String | attribute value |

**Examples Manifest**

[bios_set.pp](./examples/bios_set.pp)

### rest::bmc::ethernet::dns

Set iBMC ethernet DNS.

**Additional Attributes**

| Attribute        | Type   | Description                    |
|------------------|--------|--------------------------------|
| hostname         | String | iBMC hostname                   |
| domain           | String | iBMC domain name                |
| address_origin   | Enum   | How to allocate DNS address    |
| preferred_server | String | preferred DNS server address   |
| alternate_server | String | alternative DNS server address |

**Examples Manifest**

[ethernet_dns_set.pp](./examples/ethernet_dns_set.pp)

### rest::bmc::ethernet::get

Get iBMC ethernet interface information.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[ethernet_get.pp](./examples/ethernet_get.pp)

### rest::bmc::ethernet::ipv4

Set iBMC ethernet IPv4 address.

**Additional Attributes**

| Attribute      | Type   | Description                                  |
|----------------|--------|----------------------------------------------|
| ip             | String | IPv4 address                                 |
| gateway        | String | gateway IP address                           |
| mask           | String | subnet mask                                  |
| address_origin | Enum   | How to allocate IP. It can be Static or DHCP |

**Examples Manifest**

[ethernet_ipv4_set.pp](./examples/ethernet_ipv4_set.pp)

### rest::bmc::ethernet::ipv6

Set iBMC ethernet IPv6 address.

**Additional Attributes**

| Attribute      | Type    | Description                                                     |
|----------------|---------|-----------------------------------------------------------------|
| ip             | String  | IPv6 address                                                    |
| gateway        | String  | gateway IP address                                              |
| prefix_length  | integer | IPv6 address prefix length                                      |
| address_origin | Enum    | How to allocate IP. It can be Static, DHCPv6, LinkLocal, SLAAC. |

**Examples Manifest**

[ethernet_ipv6_set.pp](./examples/ethernet_ipv6_set.pp)

### rest::bmc::ethernet::ipversion

Set iBMC ethernet IP version.

**Additional Attributes**

| Attribute | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| value     | String | IP version. It can be IPv4AndIPv6, IPv4, IPv6. |

**Examples Manifest**

[ethernet_ipversion_set.pp](./examples/ethernet_ipversion_set.pp)

### rest::bmc::ethernet::vlan

Set iBMC ethernet VLAN.

**Additional Attributes**

| Attribute | Type    | Description              |
|-----------|---------|--------------------------|
| enabled   | Boolean | whether VLAN is enabled. |
| vlan_id   | Integer | VLAN id (1-4094).        |

**Examples Manifest**

[ethernet_vlan_set.pp](./examples/ethernet_vlan_set.pp)

### rest::bmc::license::delete

Delete iBMC license.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[license_delete.pp](./examples/license_delete.pp)

### rest::bmc::license::export

Export iBMC license.

**Additional Attributes**

| Attribute | Type   | Description                           |
|-----------|--------|---------------------------------------|
| export_to | String | the file path of export license file. |

**Examples Manifest**

[license_export.pp](./examples/license_export.pp)

### rest::bmc::license::get

Get iBMC license infomation.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[license_get.pp](./examples/license_get.pp)

### rest::bmc::license::install

Install iBMC license.

**Additional Attributes**

| Attribute | Type   | Description                                                  |
|-----------|--------|--------------------------------------------------------------|
| source    | Enum   | License source.                                              |
| type      | Enum   | Methods of installing the license file. It can be Text, URI. |
| content   | String | License content.                                             |

**Examples Manifest**

[license_install.pp](./examples/license_install.pp)

### rest::bmc::ntp::get

Get NTP settings.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[ntp_get.pp](./examples/ntp_get.pp)

### rest::bmc::ntp::set

Setup NTP.

**Additional Attributes**

| Attribute        | Type    | Description                                                         |
|------------------|---------|---------------------------------------------------------------------|
| enabled          | Boolean | whether NTP service enabled or not                                  |
| addr_origin      | Enum    | Ntp Address Origin                                                  |
| preferred_server | String  | preferred NTP server address                                        |
| alternate_server | String  | alternative NTP server address                                      |
| auth_enabled     | Boolean | whether auth enabled                                                |
| min_interval     | Integer | minimum NTP synchronization interval. the value ranges from 3 to 17 |
| max_interval     | Integer | maximum NTP synchronization interval. the value ranges from 3 to 17 |

**Examples Manifest**

[ntp_set.pp](./examples/ntp_set.pp)

### rest::bmc::power::ctrl

Power Ctrl

**Additional Attributes**

| Attribute  | Type | Description      |
|------------|------|------------------|
| reset_type | Enum | Power Reset Type |

**Examples Manifest**

[sys_power_ctrl.pp](./examples/sys_power_ctrl.pp)

### rest::bmc::power::restart

iBMC Power Restart.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[bmc_power_restart.pp](./examples/bmc_power_restart.pp)

### rest::bmc::service::get

Get service information

**Additional Attributes**

no additional attributes

**Examples Manifest**

[service_get.pp](./examples/service_get.pp)

### rest::bmc::service::set

Update service settings

**Additional Attributes**

| Attribute       | Type    | Description                                                       |
|-----------------|---------|-------------------------------------------------------------------|
| protocol        | Enum    | indicates the Service to update                                   |
| enabled         | Boolean | indicates if the protocol property State is enabled or disabled   |
| port            | Integer | indicates the protocol property port range is 1 to 65535          |
| notify_ttl      | Integer | indicates the protocol SSDP property, NotifyTTL range is 1 to 255 |
| notify_scope    | Enum    | indicates the protocol SSDP property NotifyIPv6Scope              |
| notify_interval | Integer | indicates the notify multicast interval seconds                   |

**Examples Manifest**

[service_set.pp](./examples/service_set.pp)

### rest::bmc::smtp::get

Get SMTP settings

**Additional Attributes**

no additional attributes

**Examples Manifest**

[smtp_get.pp](./examples/smtp_get.pp)

### rest::bmc::smtp::set

Update SMTP settings

**Additional Attributes**

| Attribute              | Type                 | Description                                               |
|------------------------|----------------------|-----------------------------------------------------------|
| enabled                | Boolean              | indicates the SMTP state is enabled or disabled           |
| server_addr            | String               | indicates if SMTP server address                          |
| tls_enabled            | Enum                 | indicates if SMTP server support TLS or not               |
| anon_enabled           | Enum                 | indicates if SMTP server support anon                     |
| sender_addr            | String               | indicates the SMTP sender address                         |
| sender_password        | String               | indicates the SMTP sender password                        |
| sender_username        | String               | indicates the SMTP sender username                        |
| email_subject          | String               | indicates the SMTP sent email subject                     |
| email_subject_contains | Array\[Enum\]        | indicates the SMTP sent email subject additional contents |
| alarm_severity         | Enum                 | indicates the alarm severity to send email                |
| receipt1               | Struct\[TrapServer\] | indicates the SMTP receipt 1                              |
| receipt2               | Struct\[TrapServer\] | indicates the SMTP receipt 2                              |
| receipt3               | Struct\[TrapServer\] | indicates the SMTP receipt 3                              |
| receipt4               | Struct\[TrapServer\] | indicates the SMTP receipt 4                              |

**Examples Manifest**

[smtp_set.pp](./examples/smtp_set.pp)

### rest::bmc::snmp::get

Get SNMP settings

**Additional Attributes**

no additional attributes

**Examples Manifest**

[snmp_get.pp](./examples/snmp_get.pp)

### rest::bmc::snmp::set

Update SNMP settings

**Additional Attributes**

| Attribute             | Type                 | Description                                             |
|-----------------------|----------------------|---------------------------------------------------------|
| v1_enabled            | Boolean              | indicates Whether SNMPv1 is enabled                     |
| v2_enabled            | Boolean              | indicates Whether SNMPv2 is enabled                     |
| long_password_enabled | Boolean              | indicates Whether long passwords are enabled            |
| rw_community_enabled  | Boolean              | indicates Whether read-write community name are enabled |
| rw_community          | String               | indicates the Read-Write community name                 |
| ro_community          | String               | indicates the Read-only community name                  |
| v3_auth_protocol      | Enum                 | indicates the SNMPv3 authentication algorithm           |
| v3_priv_protocol      | Enum                 | indicates the SNMPv3 encryption algorithm               |
| trap_enabled          | Boolean              | indicates Whether trap is enabled                       |
| trap_v3_user          | String               | indicates the SNMPv3 user name                          |
| trap_version          | Enum                 | indicates the trap version                              |
| trap_mode             | Enum                 | indicates the trap mode                                 |
| trap_server_identity  | Enum                 | indicates the trap Host identifier                      |
| trap_community        | String               | indicates the Community name                            |
| trap_alarm_severity   | Enum                 | indicates the Severity level of the alarm to be sent    |
| trap_server1          | Struct\[TrapServer\] | indicates the trap server 1                             |
| trap_server2          | Struct\[TrapServer\] | indicates the trap server 2                             |
| trap_server3          | Struct\[TrapServer\] | indicates the trap server 3                             |
| trap_server4          | Struct\[TrapServer\] | indicates the trap server 4                             |

**Examples Manifest**

[snmp_set.pp](./examples/snmp_set.pp)

### rest::bmc::vmm::connect

Connect to virtual media.

**Additional Attributes**

| Attribute | Type   | Description                   |
|-----------|--------|-------------------------------|
| image_uri | String | VRI of the virtualmedia image |

**Examples Manifest**

[vmm_connect.pp](./examples/vmm_connect.pp)

### rest::bmc::vmm::disconnect

Disconnect virtual media.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[vmm_disconnect.pp](./examples/vmm_disconnect.pp)

### rest::chassis::led::set

Set chassis indicator LED status.

**Additional Attributes**

| Attribute | Type | Description                                                       |
|-----------|------|-------------------------------------------------------------------|
| state     | Enum | indicates the state of chassis LED, it can be Lit, Off, Blinking. |

**Examples Manifest**

[indicator_led_set.pp](./examples/indicator_led_set.pp)

### rest::firmware::inband::upgrade

Upgrade inband firmware.

**Additional Attributes**

| Attribute         | Type   | Description                                                             |
|-------------------|--------|-------------------------------------------------------------------------|
| firmware_file_uri | String | indicates the firmware file url.                                        |
| signal_file_uri   | String | indicates the signal file url of the firmware file.                     |
| mode              | Enum   | indicates the upgrade mode, it can be Auto, Full, Recover, APP, Driver. |
| active_method     | Enum   | indicates the firmware active method, it can be Restart.                |

**Examples Manifest**

[firmware_inband_upgrade.pp](./examples/firmware_inband_upgrade.pp)

### rest::firmware::inband::version

Get inband firmware version.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[firmware_inband_version_get.pp](./examples/firmware_inband_version_get.pp)

### rest::firmware::outband::upgrade

Upgrade outband firmware.

**Additional Attributes**

| Attribute         | Type   | Description                      |
|-------------------|--------|----------------------------------|
| firmware_file_uri | String | indicates the firmware file url. |

**Examples Manifest**

[firmware_outband_upgrade.pp](./examples/firmware_outband_upgrade.pp)

### rest::firmware::outband::version

Get outband firmware version.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[firmware_outband_version_get.pp](./examples/firmware_outband_version_get.pp)

### rest::firmware::sp::result

Get Smart Provisioning result.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[firmware_sp_result_get.pp](./examples/firmware_sp_result_get.pp)

### rest::firmware::sp::set

Upgrade Smart Provisioning service.

**Additional Attributes**

| Attribute                    | Type    | Description                                                  |
|------------------------------|---------|--------------------------------------------------------------|
| start_enabled                | boolean | indicates whether SP start is enabled.                       |
| system_restart_delay_seconds | integer | indicates maximum seconds allowed for the restart of the OS. |
| timeout                      | integer | indicates maximum time (300~86400) allowed for SP deployment.|
| finished                     | boolean | indicates Status of the transaction deployed.                |

**Examples Manifest**

[sp_set.pp](./examples/sp_set.pp)

### rest::firmware::sp::upgrade

Upgrade Smart Provisioning service.

**Additional Attributes**

| Attribute         | Type   | Description                                                             |
|-------------------|--------|-------------------------------------------------------------------------|
| firmware_file_uri | String | indicates the firmware file url.                                        |
| mode              | Enum   | indicates the upgrade mode, it can be Auto, Full, Recover, APP, Driver. |
| active_method     | Enum   | indicates the firmware active method, it can be Restart.                |

**Examples Manifest**

[firmware_sp_upgrade.pp](./examples/firmware_sp_upgrade.pp)

### rest::firmware::sp::version

Get Smart Provisioning service version.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[firmware_sp_version_get.pp](./examples/firmware_sp_version_get.pp)

### rest::system::assettag::set

Update iBMC asset tag.

**Additional Attributes**

| Attribute | Type   | Description              |
|-----------|--------|--------------------------|
| value     | String | indicates the asset tag. |

**Examples Manifest**

[assettag_set.pp](./examples/assettag_set.pp)

### rest::system::cpu

Get CPU List

**Additional Attributes**

no additional attributes

**Examples Manifest**

[cpu_get.pp](./examples/cpu_get.pp)

### rest::system::cpu::health

Get CPU health infomation

**Additional Attributes**

no additional attributes

**Examples Manifest**

[cpu_health_get.pp](./examples/cpu_health_get.pp)

### rest::system::deploy::config

Update system OS deploy configuration.

**Additional Attributes**

| Attribute                  | Type   | Description                                                        |
|----------------------------|--------|--------------------------------------------------------------------|
| os_deploy_config_file_path | String | indicates the file path of OS deploy configuration JSON file path. |

**Examples Manifest**

[os_deploy_config.pp](./examples/os_deploy_config.pp)

### rest::system::drive

Get physical drive list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[drive_get.pp](./examples/drive_get.pp)

### rest::system::drive::health

Get physical drive health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[drive_health_get.pp](./examples/drive_health_get.pp)

### rest::system::eth::get

Get system ethernet list.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[system_eth_get.pp](./examples/system_eth_get.pp)

### rest::system::fan::health

Get fan health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[fan_health_get.pp](./examples/fan_health_get.pp)

### rest::system::get

Get system infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[system_get.pp](./examples/system_get.pp)

### rest::system::memory

Get memory list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[memory_get.pp](./examples/memory_get.pp)

### rest::system::memory::health

Get memory health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[memory_health_get.pp](./examples/memory_health_get.pp)

### rest::system::network_adapter::health

Get system network adaptor health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[network_adapter_health_get.pp](./examples/network_adapter_health_get.pp)

### rest::system::network_adapter

Get system network adaptor infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[network_adapter_get.pp](./examples/network_adapter_get.pp)

### rest::system::power_supply::health

Get power supply health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[power_supply_health_get.pp](./examples/power_supply_health_get.pp)

### rest::system::raid

Get RAID controller list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[raid_get.pp](./examples/raid_get.pp)

### rest::system::raid::health

Get RAID health infomation.

**Additional Attributes**

no additional attributes

**Examples Manifest**

[raid_health_get.pp](./examples/raid_health_get.pp)

### rest::user::add

Add new user

**Additional Attributes**

| Attribute | Type   | Description                               |
|-----------|--------|-------------------------------------------|
| username  | String | indicates the new created user's username |
| password  | String | indicates the new created user's password |
| role      | Enum   | indicates the new created user's role     |

**Examples Manifest**

[user_add.pp](./examples/user_add.pp)

### rest::user::delete
Add new user

**Additional Attributes**

| Attribute | Type   | Description                      |
|-----------|--------|----------------------------------|
| username  | String | indicates the user to be deleted |

**Examples Manifest**

[user_delete.pp](./examples/user_delete.pp)

### rest::user::get

Get user list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[user_get.pp](./examples/user_get.pp)

### rest::user::set

Update user attributes

**Additional Attributes**

| Attribute   | Type    | Description                         |
|-------------|---------|-------------------------------------|
| username    | String  | indicates the user to be updated    |
| newusername | String  | indicates new name for user         |
| newpassword | String  | indicates new password for the user |
| newrole     | Enum    | indicates new role for user         |
| enabled     | Boolean | indicates if the user is enabled    |
| locked      | Boolean | indicates if the user is locked     |

**Examples Manifest**

[user_set.pp](./examples/user_set.pp)


## Limitations

This is where you list OS compatibility, version compatibility, etc. If there
are Known Issues, you might want to include them under their own heading here.

## Development

Feel free to fork repo and send PR.

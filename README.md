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
some Puppet resource types and samples manifests for various features of the Huawei BMC.

## Setup

### What rest affects

The Rest module implements all puppet resource types with `Exec` module which execute python scripts(Rest-Linux) 
and those python scripts will access BMC using Redfish API.

The Rest module will do:
* Install `Rest-Linux`(scripts folder) to `/etc/puppet/modules/rest/files`
* Install `stdlib>=4.20.0` module

### Setup Requirements 

* Puppet Master version >= 5.0.0
* Puppet Agent OS family should be `Debian` or `redhat`

### Beginning with rest

```SourceCode
puppet module install huawei-rest
```

Check [Puppet Labs: Installing Modules](https://docs.puppetlabs.com/puppet/latest/reference/modules_installing.html) for more information.

## Usage

These Puppet resources are defined as part of `Rest` module:

* [`rest::bios::boot::get`](#restbiosget)
* [`rest::bios::boot::order`](#restbiosrestore)
* [`rest::bios::boot::override`](#restbiosset)
* [`rest::bios::get`](#restbmcpowerrestart)
* [`rest::bios::restore`](#restbiosbootget)
* [`rest::bios::set`](#restbiosbootorder)
* [`rest::bmc::ethernet::get`](#restbiosbootoverride)
* [`rest::bmc::ntp::get`](#restsystemcpu)
* [`rest::bmc::ntp::set`](#restsystemdisk)
* [`rest::bmc::power::ctrl`](#restbmcethernetget)
* [`rest::bmc::power::restart`](#restsystemmemory)
* [`rest::bmc::service::get`](#restbmcntpget)
* [`rest::bmc::service::set`](#restbmcntpset)
* [`rest::bmc::smtp::get`](#restsystemraid)
* [`rest::bmc::smtp::set`](#restbmcserviceget)
* [`rest::bmc::snmp::get`](#restbmcserviceset)
* [`rest::bmc::snmp::set`](#restbmcsmtpget)
* [`rest::system::cpu`](#restbmcsmtpset)
* [`rest::system::disk`](#restbmcsnmpget)
* [`rest::system::memory`](#restbmcsnmpset)
* [`rest::system::raid`](#restbmcpowerctrl)
* [`rest::user::add`](#restuseradd)
* [`rest::user::delete`](#restuserdelete)
* [`rest::user::get`](#restuserget)
* [`rest::user::set`](#restuserset)


### Common Attributes

All Rest resource type share those attributes:

| Attribute   | Description                                         |
|-------------|-----------------------------------------------------|
| ibmc_username | BMC login username |
| $ibmc_password | BMC login password |
| $ibmc_host | BMC API access host, default `127.0.0.1` |
| $ibmc_port | BMC API access port, default `443` |

Rest module resource types can visit BMC API anywhere, resource type is free to run on anywhere.

### /rest::bios::boot::get

Get boot settings.

**Attributes**

No additional attributes

**Examples Manifest**

[boot_get.pp](./examples/boot_get.pp)


### rest::bios::boot::order

Set boot order.

**Additional Attributes**

| Attribute | Type          | Description         |
|-----------|---------------|---------------------|
| sequence  | Array[String] | boot order sequence |

**Examples Manifest**

[boot_order.pp](./examples/boot_order.pp)

### rest::bios::boot::override

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

| Attribute | Type    | Description                |
|-----------|---------|----------------------------|
| attribute | String  | indicates the BIOS attribute |

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

### rest::bmc::ethernet::get

Get BMC ethernet interface information.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[ethernet_get.pp](./examples/ethernet_get.pp)

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

BMC Power Restart.

**Additional Attributes**

No additional attributes

**Examples Manifest**

[bmc_power_restart.pp](./examples/bmc_power_restart.pp)

### rest::bmc::service::get

Get service information

**Additional Attributes**

| Attribute | Type | Description                                                     |
|-----------|------|-----------------------------------------------------------------|
| protocol  | Enum | Service Protocol. (Optional, if not provided, get all services.) |

**Examples Manifest**

[service_get.pp](./examples/service_get.pp)

### rest::bmc::service::set

Update service settings

**Additional Attributes**

| Attribute        | Type    | Description                                                       |
|------------------|---------|-------------------------------------------------------------------|
| protocol         | Enum    | indicates the Service to update                                   |
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

| Attribute              | Type          | Description                                               |
|------------------------|---------------|-----------------------------------------------------------|
| enabled                | Boolean       | indicates the SMTP state is enabled or disabled           |
| server_addr            | String        | indicates if SMTP server address                          |
| tls_enabled            | Enum          | indicates if SMTP server support TLS or not               |
| anon_enabled           | Enum          | indicates if SMTP server support anon                     |
| sender_addr            | String        | indicates the SMTP sender address                         |
| sender_password        | String        | indicates the SMTP sender password                        |
| sender_username        | String        | indicates the SMTP sender username                        |
| email_subject          | String        | indicates the SMTP sent email subject                     |
| email_subject_contains | Array\[Enum\] | indicates the SMTP sent email subject additional contents |
| alarm_severity         | Enum          | indicates the alarm severity to send email                |
| receipt1           | Struct\[Receipt\] | indicates the receipt address 1            |
| receipt2           | Struct\[Receipt\] | indicates the receipt address 2            |
| receipt3           | Struct\[Receipt\] | indicates the receipt address 3            |
| receipt4           | Struct\[Receipt\] | indicates the receipt address 4            |

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
| trap_server1          | Struct\[TrapServer\] | indicates the trap server 1            |
| trap_server2          | Struct\[TrapServer\] | indicates the trap server 2            |
| trap_server3          | Struct\[TrapServer\] | indicates the trap server 3            |
| trap_server4          | Struct\[TrapServer\] | indicates the trap server 4            |


**Examples Manifest**

[snmp_set.pp](./examples/snmp_set.pp)


### rest::system::cpu

Get CPU List

**Additional Attributes**

no additional attributes

**Examples Manifest**

[cpu_get.pp](./examples/cpu_get.pp)

### rest::system::disk

Get physical disk list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[disk_get.pp](./examples/disk_get.pp)

### rest::system::memory

Get memory list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[memory_get.pp](./examples/memory_get.pp)

### rest::system::raid

Get RAID controller list

**Additional Attributes**

no additional attributes

**Examples Manifest**

[raid_get.pp](./examples/raid_get.pp)

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
Delete new user

**Additional Attributes**

| Attribute | Type   | Description                               |
|-----------|--------|-------------------------------------------|
| username  | String | indicates the user to be deleted          |

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

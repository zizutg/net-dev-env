WiFi Access Control

# Overview

This exercise provides basic understanding of configuring DHCP Service
and security control on Wi-Fi Router.

# Learning Objectives

- Understand DHCP server configuration

- Implement MAC filtering

- Implement Access Control List

# Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

# Environment 

This exercise requires working with a Wi-Fi Router/Access Point and your
laptop (or device). It would be greatly helpful if Wi-Fi Router is
connected to Wired LAN port for internet connectivity and access. At
times, without this connectivity, the configuration may not be completed
successfully.

# Description

In this exercise, TP Link dual band Wi-Fi Router is used to describe the
exercise for illustrative purposes. For any other Wi-Fi Access
Point/Router, screen layout or menu/options may be somewhat different in
GUI interface, but similar concepts would be applicable. The exercise
will describe setting up both Access Point functionality as well as
Wi-Fi Router functionality. It is assumed that you will be working with
factory reset Wi-Fi Router. Thus, it is recommended that the Wi-Fi
Router be reset to factory default before starting the setup.

## Configuring DHCP

When a device (laptop/phone etc.) connects to Wi-Fi Router, it needs to
get the IP address, subnet mask, default router, DNS server etc. so as
access internet successfully. The RFC 1918 provides the private address
ranges for public use, i.e., any one can use these IP addresses in their
local setup with requiring any permissions/approvals. This RFC provides
The three reserved ranges as below:

i.  10.0.0.0 - 10.255.255.255, with a subnet prefix of /8.

ii. 172.16.0.0 - 172.31.255.255 with a subnet prefix of /16. That is,
    there are 16 ranges that can be used. These 16 ranges are
    172.16.0.0/16, 172.17.0.0/16, ..., 172.31.0.0/16.

iii. (192.168.0.0 - 192.168.255.255, with a subnet prefix of /24. That
     is, there 256 ranges that can be used. These 256 ranges correspond
     to 192.168.0.0/24, 192.168.1.0/24, ..., 192.168.255.0.0/24.

Normally, for a home/office network where number of connecting devices
are less in numbers (e.g., less than 200), most setup use the 3^rd^
range i.e., 192.168.0.0-192.168.255.255.

### Configuration of IP Range

To configure your selected range in the Wi-Fi router, login to the
AP/router, select DHCP option, and enter the values in the DHCP server
settings. An example is shown in [Figure 1](#_Ref206338139).

![: DHCP server setting](media/image1.png){width="5.33794072615923in"
height="3.144594269466317in"}

The [Figure 1](#_Ref206338139) shows the range 192.168.0.0/24 being used
for DHCP Server and with default gateway as 192.168.0.1. General
convention is to use the first assignable IP address (or the last
assignable address) in range be used for default gateway. It is to be
noted the first address in the range 192.168.0.0 is used to denote
network number and last address 192.168.0.255 is used for broadcast
address and thus can't be used for assignment. The [Figure
1](#_Ref206338139) uses the start of DHCP range to be 192.168.0.100 and
end of DHCP Range to be 192.168.0.199.

In this DHCP server configuration, addresses 192.168.0.2-192.168.0.99 as
well as 192.168.0.200 -- 192.168.0.254 are not configured for DHCP
Server. As a general practice, full network range is not configured and
some address space is reserved. You should choose your start and end
addresses for DHCP server configuration.

Another parameter that needs to be configured is lease time. The DHCP
server assigns the IP Address for a limited period determined by lease
time. After expiry of lease time, the device needs to renew the IP
Address. Typically, in home or small office setup, this value is kept at
1 to 2 days, whereas in public places e.g., library, airports etc., the
lease time is defined to be 1 to 2 hrs. This is because in the public
places, a user is expected to use the internet connectivity for shorter
duration.

Another parameter that must be configured is DNS server. These are
typically provided by your internet service provider. Enter those values
in these fields. If not known, then you can specify open DNS servers
such as 8.8.8.8 (by Google) and 1.1.1.1 (by Cloudfare).

Save the settings and this will be effective immediately. In case you
have changed the range, it is likely that you will be disconnected and
need to be connected again as you will get a new IP address from DHCP
Server.

### Configuring Reserved Addresses

For some of the fixed device in home/office setup, it is preferred that
these devices be assigned a fixed IP address. Either these can be
manually assigned to the device or configured in the DHCP Server to
always assign the same address. Use the **Address Reservation** option
in AP/Router setting and enter the MAC address of the device and
associated reserved IP address. An example of such a setup is shown in
[Figure 2](#_Ref206340536). This reserved IP address is also used when
you would like to put security control for different devices in the
Wi-Fi Router.

![: Reserving IP addresses in DHCP
setting](media/image2.png){width="5.445857392825896in"
height="2.413980752405949in"}

## Configuring Security Controls

A Wi-Fi router provides different choices for security control access.
At the base level, most AP/Router provides MAC filtering, Access Control
Lists etc.

### MAC Filtering

This option, if provided, requires you to enter the MAC addresses of
devices which should be always given (or denied) full access to network
users or internet. For example, if a internet enable TV is to be given
full access, its MAC address should be entered in such a list and it
should be given full access. Similarly, if few devices or hosts (e.g., a
server in the local network) needs to be provided unrestricted access,
their MAC addresses should be entered here.

Further, if some devices should not be given access from internet (e.g.,
printer, thermostat, security access devices), there MAC address should
be configured and access should be denied.

Thus, primarily which needs to be given (or denied) Internet access,
enter their MAC addresses accordingly.

### Access Control Lists

Often, you would like to define rules limiting the access of some
devices to certain internet sites and these devices should not be given
full internet access. For example, printer should be able to access its
manufacturer website for driver/software update. Then, these devices
should be first added into Reserved IP Addresses and then added to
Access control List specifying which targets are allowed for access and
during what time. You need to be careful when adding rules to ACL. ACL
also has a default policy of deny or allow. Choose it as per your need.
Use default deny if you are pessimistic and want to explicitly identify
and permit known users for internet access. Choose default Allow, if you
are optimistic and generally want to allow everyone except selected few
who should be denied internet access. These ACL rules can become
complicated especially if a large number of such rules are defined and
thus defined them judiciously.

### Other Security Controls

Some WiFi routes provides explicit parental control. This option is
generally used for children, K-12 schools, where you would like to
provided internet access during specified hours. If such a situation
applies, then define these rules accordingly.

### Bandwidth Control

At times, especially in a small office setup with limited internet
bandwidth, you would like to put bandwidth control for users so that
some unscrupulous users do not consume the entire bandwidth. One
example, is guest network access. [Figure 3](#_Ref206341881) provides an
example configuration of bandwidth control.

![[]{#_Ref206341881 .anchor}Figure 3: Bandwidth access
control](media/image3.png){width="5.490358705161855in"
height="4.147684820647419in"}

Define the bandwidth control policies as per your requirements and
implement the same by configuring the values accordingly. However, it
should be noted that such configuration often results in disgruntled
users and may lead to political issues. So, use such controls in a
judicious manner.

# Summary

> In this exercise, we have studied and learnt the following

a.  DHCP Server configuration

b.  MAC filtering

c.  Access Control Lists for security control

🡨end of Lab-CN-Wk14-S4🡪

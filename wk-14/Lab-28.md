WiFi Connectivity and Authentication

# Overview

This exercise provides basic understanding of WiFi Connectivity in
home/office network.

# Learning Objectives

- Understand WiFi AP/Router configuration

- Understand SSId management

- Configure WiFi Authentication.

# Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

# Environment 

This exercise requires working with a Wifi Router/Access Point and your
laptop (or device). It would be greatly helpful if WiFi Router is
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

## Initial Setup

### Powering up Wi-Fi Router/AP

Power on the AP/Router, and connect its internet port to office LAN wall
jack using RJ45 cable.

Make a note of the factory default setting i.e., its SSID and Password,
which can be typically found at the backside label of the device. After
power on of the Wi-Fi Router, wait till its status light indicators show
that it is connected correctly.

### Connecting to AP/Router for Configuration

On your laptop, select the Wi-Fi Network (e.g., TP-Link_EB3D_5G) as
broadcast by AP/Router and connect to it. Once Wifi is connected, open a
browser on your laptop, and enter the IP address of WiFi Router (as
given in quick start guide) which would typically be 192.168.x.1, where
x would 0,1, 2 or 3. This will open a set up page for Wi-Fi Router.
Since this device is starting from factory default setting, it may ask
to reset the password to a new value. Create a password of your choice
and then access the setup GUI for setting up the AP/Router.

### Band Selection

Most Access Points work in dual band i.e., 2.4GHz and 5GHz. Find the
menu item for radio/dual band and enable both. Configure extra options
if available for these bands as follows

i.  2.4GHz Frequency Band

    a.  This band supports 802.11b, 802.11g and 802.11n mode. Those most
        modern devices are configured to use 802.11n mode, it is
        recommended to enable all three of these modes.

    b.  This frequency band supports 11 channels and rather than fixing
        any particular channel, configure it in Auto Mode i.e., let AP
        determine the best channel available in the location where it is
        installed.

    c.  Further, set the channel width to Auto mode instead of 20MHz or
        40MHz. The latter gives more bandwidth, but may also cause more
        interference with neighboring devices when more number of
        devices are connected to it.

    d.  Enable broadcast of SSID. If this is not enabled, then this AP
        will not be discoved by user device (e.g., laptop, phone etc.)

ii. 5GHz Frequency band

    a.  This frequency band supports 802.11a, 802.11n and 802.11ac mode.
        Most current devices today supports 802.11ac, but it is
        recommended to configure it with mixed mode using all 3 options.

    b.  Choose the channel in Auto mode for best operations.

    c.  Choose Channel width in Auto mode for best operations.

## Configuring Authentication

### Authentication

The access point typically provides following 3 types of wireless
authentication

i.  No authentication (disable authentication)

> This implies that no authentication i.e., any user who can see the
> SSID from the AP/Router, can connect to it. It is strongly recommended
> this authentication method is not used in office/home. This option may
> however be useful in a public place e.g., library, park, etc.

ii. WPA/WPA2/WPA3 Personal

    a.  This is the preferred authentication method to be used for
        home/office setup where all users connecting to WiFi AP/Router
        know and trust each other. In this exercise, select this option.

    b.  From the given Encryption option, use AES if available, else
        TKIP. AES provides better encryption security.

    c.  Specify the password and remember the same. This will be used by
        all users connecting to AP/Router. If all users don't know each
        other, this can be a security risk.

    d.  The drawback of this option is that if any one user leaves the
        group, this password needs to be changed and informed to all
        other users.

iii. WPA/WPA2 Enterprise.

     a.  This option is to be selected in a larger office environment,
         where the organization maintains a separate authentication
         server, e.g., Active Directory (AD) server or Radius Server. If
         so, enter the IP Address of that server and related
         information. We will not use this option.

iv. Guest Network Access.

    a.  If Wi-Fi AP/Router provides guest network access separately,
        then enable it and configure it. Define a separate SSID and
        password for the guest, and isolate it from accessing local
        network. This will provide security to local users and provide
        access to visiting guests to your home/office.

    b.  If AP/Router provides bandwidth control, enable the same and
        define the limit for incoming and outgoing traffic. This ensures
        that guest does not consume the entire internet bandwidth.

### WPS Access

> Most current routers provide Wi-Fi Protected Setup (WPS) for
> connecting a device quickly using a PIN. The device must support WPS
> Connectivity. To enable this support, configure the WPS option, and
> enter 8-digit pin value. The WPS standard defines the PIN to be 8
> digits.
>
> To connect a new device using PIN, prese the WPS button on Wi-Fi
> router, and connect the device within 2 minutes. On the device, user
> need to enter the specified PIN and device will be connected using WPN
> in a quicker way.

# Summary

> In this exercise, we have studied and learnt the following

a.  Configuring Wi-Fi Bands (2.4GHz and/or 5GHz) and channel parameters

b.  Configuring Authentication methods (WPA-PSK vs WPA Enterprise)

c.  Configuring SSID and enabling its broadcast.

d.  Enabling WPS for authentication.

🡨end of Lab-CN-Wk14-S3🡪

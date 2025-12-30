# Lab 02 - Linux User and Groups

This exercise provides basic understanding of users in a Linux system
and grouping of users.

## Learning Objectives

-   Understand basics of Linux users.
-   Understand basics of Linux groups

## Learning Resources

1.  Understanding password hashing

    -   https://www.cyberciti.biz/faq/understanding-etcshadow-file/

## Environment 

Access to a Linux system created in Lab 01, either via remote desktop or SSH.

Note: If you closed the previous docker container you need:
- Pull and run the image 
  - Or, Build and run the Docker Image: might take time
- Use these credentials to access the system
  - `ssh student@localhost:33900`
  - `password: dps_repo`
- unminimize the current image 

***Consult Lab 01 for details***

## Description


### Creating a user

User management activities requires **root** privileges. Use all such commands with `sudo` privilege.

Create a normal user with home directory creation and login shell as
bash, and assign it a password

- `student:~$ sudo useradd -m -s /bin/bash testuser1`

  - This creates a user but password has not been set and thus this user can't access the system. Verify this by checking the entries in */etc/passwd* and */etc/shadow* files.

- `student:~$ grep testuser1 /etc/passwd`
    >*testuser1:x:1008:1009::/home/testuser2:/bin/bash*

- `student:~$ sudo grep testuser1 /etc/shadow`
    > *testuser1:!:19976:0:99999:7:::*

Setup a password for this user to be able to login

- `student:~$ sudo passwd testuser1`
    >*New password:*<br>
    >*Retype new password:*<br>
    >*passwd: password updated successfully*<br>

This will create a password for this user /etc/shadow file and user
should be able to login.

- `student:~$ sudo grep testuser1 /etc/shadow`
    >*tuser1:\$y\$j9T\$mFx41HpSIc/3F49PwV6hf\$RI<br>WNJmn3q3dUeSPS4J6eRW4HnMFrYDe90BqxXtnj./:19976:0:99999:7:::*

Change the attributes of this created user e.g. assign a name for
identification information purposes and verify this name in /etc/passwd
file.

- `student:~$ sudo usermod -c "General Test User 1" testuser1`
- `student:~$ grep testuser1 /etc/passwd`
    >*testuser1:x:1007:1008:General Test User 1:/home/testuser1:/bin/bash*<br>


### Using sudo command

For normal user account without sudo privileges, sudo command does not
work. From the testuser1 terminal, try the following commands

***Open another terminal and login as via SSH as the testuser1 with the password.***


- `testuser1:~$ sudo whoami`
    > *[sudo] password for student:*<br>
    > *testuser1 is not in the sudoers file. This incident will be reported.*<br>
    > *testuser1:~$*<br>

For sudo privileged user account e.g. student, sudo command works
fine. For first time invocation, enter the password of your privileged
account. From the original terminal, where you logged in as student

- `student:~$ sudo whoami`
    >*[sudo] password for student:*<br>
    >*root*<br>
    >*student:~$*

Access the bash shell with root privileges

- `student:~$ sudo bash`
    >*root\@ubuntu-linux-22-04-desktop:/home/student\#*<br>

You have all the root accesses. To exit from this

- `root\@ubuntu-linux-22-04-desktop:/home/student# exit`


### Creating a user with sudo privileges

Follow the above process to first create a normal user and then using
the usermod command, add this created user to sudo group.

- `student:~$ sudo useradd -m -s /bin/bash testuser2`
- `student:~$ sudo passwd testuser2`
    >*New password:*<br>
    >*Retype new password:*<br>
    >*passwd: password updated successfully*<br>

It is a recommended practice that users should change the password upon
first login. Force the user to change the password upon first login.

- `student:~$ sudo passwd -e testuser2`
    >*passwd: password expiry information changed.*<br>

- `student:~$ sudo usermod -aG sudo testuser2`

Verify that this user is added to *sudo* group

- `student:~$ grep testuser2 /etc/group`
    >*sudo:x:27:rprustagi,student,testuser2*<br>
    >*testuser2:x:1009:*<br>

- ***Open another terminal and log in as testuser2***
    >*You are required to change your password immediately (administrator enforced).*<br>
    >*Changing password for testuser2.*<br>
    >*Current password:*<br>
    >*New password:*<br>
    >*Retype new password:*<br>

***Study useradd, usermod in more details with man utility***

### Understand Linux Users

  Identify current logged in user
- `student:~$ whoami`
    >*student*

Identify userid and groupid for any user

- `student:~$ id`

    >*uid=1005(student) gid=1006(student) groups=1006(student)*<br>

- `student:~$ id testuser1`
  
    >*uid=1001(testuser1) gid=1001(testuser1) groups=1001(testuser1)*


Other commands that are useful in actual machines but might be hard to test on docker container

- Identify all users currently logged in 
  - `student:~$ who -a`
- Alternatively, another command to find information about all users, and their running processes
  - `student:~$ w`


### Removing a user 

To remove a user from the system, use userdel command.

The first command below simply removes the user from /etc/passwd but its
home directory will continue to exist. The second command will remove
the user as well as its home directory and all contents therein.

- `student:~$ sudo userdel testuser1`
- `student:~$ sudo userdel -r testuser2`

### Installing softwares/packages

First update the repositories and then install the desired packages.

- `student:~$ sudo apt update`

Get information about any installed packages e.g. apache2 webserver

- `student:~$ sudo apt show apache2`

    >*Package: apache2*<br>
    >*Version: 2.4.52-1ubuntu4.12*<br>
    >*Priority: optional*<br>
    >*Section: web*<br>
    >*Origin: Ubuntu*<br>
    >*...*<br>

To list all the packages installed on the system

- `student:~$ sudo apt list | more`
    >*WARNING: apt does not have a stable CLI interface. Use with caution in scripts.*
    >*Listing\...*<br>
    >*0ad-data-common/jammy 0.0.25b-1 all*<br>
    >*0ad-data/jammy 0.0.25b-1 all*<br>
    >*0ad/jammy 0.0.25b-2 arm64*<br>
    >*0install-core/jammy 2.16-2 arm64*<br>
    >*0install/jammy 2.16-2 arm64*<br>
    >*0xffff/jammy 0.9-1 arm64*<br>
    >*1oom/jammy 1.0-2 arm64*<br>
    >*2048-qt/jammy 0.1.6-2build1 arm64*<br>
    >*...*

Similarly, explore few other options with package installations software

- `student:~$ sudo apt-cache stats`
- `student:~$ sudo apt update --fix-missing`
- `student:~$ sudo apt upgrade`
- `student:~$ sudo apt dist-upgrade`

#### Install and removing packages

To install a package, simply use that package name to install, e.g. to
install ncat

- `student:~$ sudo apt install ncat`
    >*Reading package lists\... Done*<br>
    >*Building dependency tree\... Done*<br>
    >*Reading state information\... Done*<br>
    >*Calculating upgrade\... Done*<br>
    >*...*<br>
    >*Do you want to continue? [Y/n] y*<br>
    >*...*<br>
    >*Processing triggers for man-db (2.10.2-1) \...*<br>
    >*student:~$*<br>

Similarly, to remove a package, simply use that remove option with
package name. To remove outdated dependencies, use autoclean option.

- `student:~$ sudo apt remove ncat`
    >*Reading package lists\... Done*<br>
    >*Building dependency tree\... Done*<br>
    >*Reading state information\... Done*<br>
    >*...*<br>
    >*Do you want to continue? [Y/n] y*<br>
    >*...*<br>
    >*Processing triggers for man-db (2.10.2-1) \...*<br>
    >*student:~$*<br>

- `student:~$ sudo apt autoclean`
    >*Reading package lists\... Done*<br>
    >*Building dependency tree\... Done*<br>
    >*Reading state information\... Done*<br>

## Summary

In this exercise, we have learnt working witih creating users, changing
the password and managing software packages including installing and
removing these.

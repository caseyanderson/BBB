# installing debian onto the eMMC of BBB (rev B)
Casey Anderson, July 2014


I'm currently using this image: BBB-eMMC-flasher-debian-7.1-2013-10-08.img.xz (google it,as I apparently misplaced the url [note to self: find url]

## Part 1: writing image file to sd card (from mac osx)
sourced from [here](http://www.raspberrypi.org/documentation/installation/installing-images/mac.md)

*do the following in the terminal, anything in carrots (< to >) denotes user input*

1. `diskutil list`

2. `diskutil unmountDisk /dev/<disk# from diskutil>`

3. `sudo dd bs=1m if=/<location of file on cpu> of=/dev/<disk#>`

4. go get a cup of coffee

5. at the end, you should see something like this in the terminal:

```800+0 records in
800+0 records out
838860800 bytes transferred in 186.166372 secs (4505974 bytes/sec)```

6. `diskutil unmountDisk /dev/disk2`

7. `diskutil eject /dev/disk2`

/////////

## Part 2: flashing the image to the internal eMMC
*i.e. put the SD card in the BBB...*

1. power down your BBB, keep ethernet plugged in (why not)

2. put sd card into slot

3. hold the [user boot button](https://www.google.com/search?q=beaglebone+black+user+boot+button&espv=2&source=lnms&tbm=isch&sa=X&ei=Gfm5U9qMB8zjoAS2qIEY&ved=0CAcQ_AUoAg&biw=1039&bih=779&dpr=1) down, apply power

4. once all four LEDs are on, continue holding until it switches to two leds, then let go of user boot (the heartbeat should change to the bottom two leds being predominantly on, with the other two flashing periodically)

5. go get a cup of coffee
*note: sometimes this works, sometimes it doesnt (often times because one did not hold the user boot button down long enough).*

6. the flashing process is complete when all four LEDs stay on without interruption.

/////////

## Part 3a: log in via ssh over LAN
*i prefer working with BBBs over the network, so lets start with an explanation of how login wirelessly via ssh*

1. start with the BBB powered down and ethernet plugged in (make sure nothing else is plugged in for now)

2. apply power, wait for heartbeat

3. since we are doing this via wifi, use something to look for all registered IPs on your network (example: im doing this from mac osx, so im using LanScan, which is fine if you are not somewhere with millions of things on the network [like art center, for example]). you are looking for something that comes up with "Texas Instruments" as your vendor (this is certainly the easiest way to identify a BBB with LanScan)

4. in the terminal, log in to the root user for debian

```ssh root@<IP ADDRESS OF BBB>```

which will result in a prompt asking for your password. By default the password is `root`. we need to CHANGE THIS AS SOON AS POSSIBLE (and disable root access via ssh entirely, which will be discussed later). if all went to plan, you should see something like this upon successfully logging in:

```
Linux arm 3.8.13-bone28 #1 SMP Thu Sep 12 23:22:35 UTC 2013 armv7l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with AB
```

/////////

## Part 3b: log in via ssh over USB

/////////

## Part 4a: making a new user on our way to disabling root access via ssh

root should only be reserved for special cases, and we dont want to keep it as a generally available user on our system. lets start by making a new user
(sourced from [here]( http://www.debian-administration.org/article/2/Adding_new_users))

1. make a login: ```useradd <name of user>```

2. and then change the password ```passwd <name of user>```

3. now, lets make a home directory for that new user:

```
mkdir /home/<name of user>
chown <name of user>:users /home/<name of user>
```

this creates a directory with the same name as the login account beneath the ```/home``` directory - then changes it to be owned by the user.

4. lets add our new user to the list of sudoers with ```sudo visudo```

look for a line that reads something like the following:

```
#User privilege specification
root    ALL=(ALL:ALL) ALL
```

and add your new user under root like this:

```#User privilege specification
root    ALL=(ALL:ALL) ALL
<newuser>     ALL=(ALL:ALL) ALL
```

5. now type ```Ctrl-X``` (to close) and then ```Y``` and ```enter``` (to save)

6. reboot ```sudo reboot```

and you should now be able to login to your new user

//

## Part 4a: change the root password

su
(to become root if you logged into your new user)

passwd

Enter new UNIX password:
Retype new UNIX password:

(do that)

now root has a different password

//

the entire reason i was interested in distributed computing was imagining the kind of scalability i could get by developing one image, spreading it across many boards, and communicating with each of them differently. in order to do that effectively, we need to be able to identify which machine we are talking to. so, lets change the hostname of the cpu

1. sudo nano /etc/hostname
<new hostname>

2. Ctl-X, Y to save

3. sudo nano /etc/hosts
change
127.0.0.1 localhost
127.0.0.1 arm

to

127.0.0.1 localhost
127.0.0.1 <new hostname>

4. Ctl-X, Y to save

5. sudo reboot

6. login after reboot and you should see your changes take effect

(fyi, underscores are not allowed in hostnames...
in other words, if you tried to set

deb_1

as the host name, you will see this on login

root@(none)

)

//

static ip address

go into /etc/network/interfaces to look at your current settings

1. sudo nano /etc/network/interfaces

so, kind of depends what you want to do with this board. if you are going to be moving it around from place to place, it might be better to keep the settings where they are (i.e. the board will get a new IP address from whatever network it connects to). however, one of the problems with this: if there are a million devices on the network already, its going to be difficult to locate the board. in the past, i have added a script that launches on startup (with cron), which logs into one of my email addresses and emails the BBB's ip to another email address. there are some security issues with how im doing that currently, but i had okay results with that (the only drawback is that it sometimes takes a minute for a device to be assigned an ip, log into one email service, and email another one, and that can get annoying). ill cover how to do this in the near future, but if you know that you will be consistantly connecting to the same network, or will not be moving the board from location to location, then you could also simply opt for a static ip.

so, by default /etc/network/interfaces has the following set:

# The primary network interface
auto eth0
iface eth0 inet dhcp

1. comment out both of those (you can delete it, but its easier to comment it out on the offchance that you make a mistake and need to redo this file)
i.e. should look like this:

# The primary network interface
#auto eth0
#iface eth0 inet dhcp

2. now, down at the bottom, add something like this:

auto eth0
iface eth0 inet static
address 192.168.1.100
netmask 255.255.255.0
network 192.168.1.0
broadcast 192.168.1.255
gateway 192.168.1.1

with your own info in there. more specifically, you will need to change the following parameters:

address <youripaddress>
nemask <normally 255.255.255.0, but check to be sure>
network <yournetworkip>
broadcast <yourbroadcast>
gateway <your gateway>

a few different ways to find this info

1. in the same shell that you are wirelessly ssh-ing into the BBB, type ifconfig to see your current network settings. its a bit difficult to read some of these, and fortunately linux has some nice tools for such things

insert list of tools for such things here

to confirm, sudo reboot, log in again when your system is up. you should now see the exact same settings you entered previously.

//
one last setup issue and then we can start actually doing things

so, we have changed the root login, but peopel still know that there is probably a way to login as root if they can guess the password. lets fix it so that is impossible. in other words, we are going to set it so that no one is allowed to login as root at all. in order to be root, one will have to login as one of our users (and they would have to know that that user is there), and THEN switch to root. we want that kind of security just in case. also, for fun, i have switched the SSH login port so that it is even harder for someone else to login to this machine.

sudo nano /etc/ssh/sshd_config

change Port to something else
Port 2033 (i did 2233)

and disable root login
Permitrootlogin no

there seems to be some disagreement about whether changing the port number makes sense. its up to you, ultimately, but if you want to do it, that is how

//
updating and upgrading (plus other general debian setup stuff)
finally, actual linux stuff!

update server package list and upgrade packages

sudo apt-get update
sudo apt-get upgrade

set timezone:

sudo dpkg-reconfigure tzdata

do this twice. the first time you will set country and time zone (US, Pacific Ocean), the second time you will specify America and then, if you are in LA, Los Angeles. it will open an ancient looking gui window for you to interact with to do this stuff

to add usb support

sudo apt-get install usbmount

//
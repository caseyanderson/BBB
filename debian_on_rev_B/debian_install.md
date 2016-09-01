# installing debian onto the eMMC of BBB (rev B)
Casey Anderson, July 2014


I'm currently using this image: https://debian.beagleboard.org/images/bone-debian-8.3-lxqt-4gb-armhf-2016-01-24-4gb.img.xz

## Part 1: writing image file to sd card (from mac osx)
sourced from [here](http://www.raspberrypi.org/documentation/installation/installing-images/mac.md)

*do the following in the terminal, anything in carrots (< to >) denotes user input*

1. `diskutil list`

2. `diskutil unmountDisk /dev/<disk# from diskutil>`

3. `sudo dd bs=1m if=/<location of file on cpu> of=/dev/<disk#>`

4. go get a cup of coffee

5. at the end, you should see something like this in the terminal:

```
800+0 records in
800+0 records out
838860800 bytes transferred in 186.166372 secs (4505974 bytes/sec)
```

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
*i prefer working with BBBs over the network, so lets start with an explanation of wireless ssh login*

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

and add your new user under ```root``` like this:

```
#User privilege specification
root    ALL=(ALL:ALL) ALL
<newuser>     ALL=(ALL:ALL) ALL
```

5. now type ```Ctrl-X``` (to close) and then ```Y``` and ```enter``` (to save)

6. reboot ```sudo reboot```

and you should now be able to login to your new user

/////////

## Part 4b: change the root password

1. ```su``` to become root if you logged into your new user

2. then ```passwd```

3. enter new password twice

4. now root has a different password

/////////

## Part 4c: disable root login over ssh

1. go to ```/etc/ssh/sshd_config```

2. you should see something that looks likes:

```
Permitrootlogin yes
```

which you should simply change to no

3. save and exit

4. reboot

/////////

## Part 5.: change hostname of the cpu

1. ```sudo nano /etc/hostname```

2. enter ```<new hostname>```

3. ```Ctl-X```, ```Y``` to save

4. ```sudo nano /etc/hosts```

and change

```
127.0.0.1 localhost
127.0.0.1 arm
```

to
```
127.0.0.1 localhost
127.0.0.1 <new hostname>
```

4. ```Ctl-X```, ```Y``` to save

5. reboot

6. login after reboot and you should see your changes take effect (fyi, underscores are not allowed in hostnames...)

/////////

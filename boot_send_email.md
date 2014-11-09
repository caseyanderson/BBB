# BBB emails its own IP
*refers to [this](boot_send_ip.py) code*

1. choose a send (`me`) and receive (`you`) email address. the file needs access to the password for  `me` currently (NOTE TO SELF: find a better way to do this).

2. Enter `crontab -u <username> -e` in the terminal. This will allow you to schedule cron jobs for user `<username>`.

3. Enter `@reboot <path to boot_send_ip.py>` in the terminal. `cntl-X` and then `y` to save.

4. make `boot_send_ip.py` executable by entering `chmod +x <path to file>` in the terminal.

5. restart and the BBB should email its IP on boot.

Note: if you are not receiving the email on the `you` side, you have likely either forgot to make the `.py` file executable or need to add some amount of a wait (`time.sleep(xSeconds)`) somewhere in the script. The main issue here is generally the amount of time it takes for login to the `me` email address.

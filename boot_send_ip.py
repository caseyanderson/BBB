#!/usr/bin/python

"""
Find own ip address and email it.
sourced from code by http://edgyproduct.org/
"""

import socket
import datetime, time
import sys

failed = 1
while(failed):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        my_ip = s.getsockname()[0]
        s.close()
        failed = 0
    except SocketError:
        print sys.exc_info()[0]
    except:
        print error
    time.sleep(5)

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


msg = MIMEText("Beaglebone ip address: %s" % my_ip)


me = 'cta@caseyanderson.com'
you = 'casey.thomas.anderson@gmail.com'

msg['Subject'] = 'Beaglebone ip address at ' + str(datetime.datetime.now())
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('mail.caseyanderson.com')
s.login('cta@caseyanderson.com', '<password>')
s.sendmail(me, [you], msg.as_string())
s.quit()

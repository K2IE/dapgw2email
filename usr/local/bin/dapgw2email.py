#!/usr/bin/python3

# Author: K2IE
# Published under GPL v3.0

import time
import subprocess
import select
import sys
import smtplib
import datetime

dt1 = datetime.datetime.now(datetime.timezone.utc)
dt2 = dt1.strftime('%Y-%m-%d')

filename = "/var/log/pi-star/DAPNETGateway-" + dt2 + ".log"

ric = b'to ' + sys.argv[1].encode('utf-8') + b','

sender = sys.argv[3]
recipient = sys.argv[4]

myFrom    = "From: Pi-Star <" + sender + ">\n"
myTo      = "To: " + recipient + "\n"
Subject   = "Subject: DAP GW Pager Notification\n\n"

header    = myFrom + myTo + Subject 

f = subprocess.Popen(['tail','-F',filename],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

while True:
    if p.poll(1):
        p_line = f.stdout.readline()
        if ric in p_line:
           pos = p_line.find(b'Alphanumeric')
           message = p_line[pos+15: -2]
           smtpmsg = header + message.decode('utf-8')
#           print (message.decode('utf-8'))
#           print (header)
           try:
              smtpObj = smtplib.SMTP(sys.argv[2], 25)
              smtpObj.sendmail (sender, recipient, smtpmsg)
              smtpObj.quit
           except:
              exit ("Error: Check SMTP configuration.")
    time.sleep(1)

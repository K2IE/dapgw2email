#!/usr/bin/python3

# Author: K2IE
# Published under GPL v3.0

import time
import subprocess
import select
import sys
import smtplib
import datetime

def curr_utc_date():
   dt1 = datetime.datetime.now(datetime.timezone.utc)
   dt2 = dt1.strftime('%Y-%m-%d')
   return dt2

def init_log_tail():
   global p
   global f
   today = curr_utc_date()
   filename = "/var/log/pi-star/DAPNETGateway-" + today + ".log"
   f = subprocess.Popen(['tail','-F',filename],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   p = select.poll()
   p.register(f.stdout)
   return today

ric = b'to ' + sys.argv[1].encode('utf-8') + b','

sender = sys.argv[3]
recipient = sys.argv[4]

myFrom    = "From: Pi-Star <" + sender + ">\n"
myTo      = "To: " + recipient + "\n"
Subject   = "Subject: DAP GW Pager Notification\n\n"

header    = myFrom + myTo + Subject 

today = init_log_tail()

while True:
    # Check for new UTC date and switch logfiles
    if today != curr_utc_date():
       p.terminate()
       today = init_log_tail()
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

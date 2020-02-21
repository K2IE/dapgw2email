#!/usr/bin/python3

# Author: K2IE
# Published under GPL v3.0

import time
import subprocess
import select
import smtplib
import datetime
import os.path
import configparser
import logging

log = logging.getLogger('dapgw2email')

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

def ErrExit():
   log.error("Exiting")
   exit(0)

conffile = "/etc/dapgw2email.conf"
if not os.path.isfile(conffile):
   log.error(conffile + " not found")
   ErrExit()

config = configparser.ConfigParser()

try:
   config.read(conffile)
except:
   log.error("Check " + conffile + " for proper [dapgw2email] section heading")
   ErrExit()

try:
   ric = config.get('dapgw2email', 'RIC').encode('utf-8')
except:
   log.error("Check " + conffile + " for proper RIC value in [dapgw2email] section")
   ErrExit()

try:
   smtp = config.get('dapgw2email', 'SMTP')
except:
   log.error("Check " + conffile + " for proper SMTP value in [dapgw2email] section")
   ErrExit() 

try:
   sender = config.get('dapgw2email', 'SENDER')
except:
   log.error("Check " + conffile + " for proper SENDER value in [dapgw2email] section")
   ErrExit() 

try:
   recipient = config.get('dapgw2email', 'RECIPIENT')
except:
   log.error("Check " + conffile + " for proper RECIPIENT value in [dapgw2email] section")
   ErrExit() 

try:
   r1 = config.get('dapgw2email', 'R1').encode('utf-8')
except:
   pass

try:
   r2 = config.get('dapgw2email', 'R2').encode('utf-8')
except:
   pass

try:
   r3 = config.get('dapgw2email', 'R3').encode('utf-8')
except:
   pass

try:
   r4 = config.get('dapgw2email', 'R4').encode('utf-8')
except:
   pass

try:
   r5 = config.get('dapgw2email', 'R5').encode('utf-8')
except:
   pass

try:
   r6 = config.get('dapgw2email', 'R6').encode('utf-8')
except:
   pass

try:
   r7 = config.get('dapgw2email', 'R7').encode('utf-8')
except:
   pass

try:
   r8 = config.get('dapgw2email', 'R8').encode('utf-8')
except:
   pass

try:
   r9 = config.get('dapgw2email', 'R9').encode('utf-8')
except:
   pass

rlist = []
rlist.append(ric)
if 'r1' in locals():
   rlist.append(r1)
if 'r2' in locals():
   rlist.append(r2) 
if 'r3' in locals():
   rlist.append(r3) 
if 'r4' in locals():
   rlist.append(r4)
if 'r5' in locals():
   rlist.append(r5)
if 'r6' in locals():
   rlist.append(r6)
if 'r7' in locals():
   rlist.append(r7)
if 'r8' in locals():
   rlist.append(r8)
if 'r9' in locals():
   rlist.append(r9) 

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
        for rval in rlist:
           if rval in p_line:
              pos = p_line.find(b'Alphanumeric')
              message = p_line[pos+15: -2]
              smtpmsg = header + message.decode('utf-8')
              try:
                 smtpObj = smtplib.SMTP(smtp, 25)
                 smtpObj.sendmail (sender, recipient, smtpmsg)
                 smtpObj.quit
              except:
                 log.error("Error: Check SMTP configuration.")
                 ErrExit() 
              break
    time.sleep(1)

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
   log.warning("Opening log file")
   filename = "/var/log/pi-star/DAPNETGateway-" + today + ".log"
   f = subprocess.Popen(['tail','-F',filename],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   p = select.poll()
   p.register(f.stdout)
   log.warning("Log file open successful")
   return today

def ErrExit():
   log.error("Exiting")
   exit(0)

conffile = "/etc/dapgw2email.conf"
if not os.path.isfile(conffile):
   log.error(conffile + " not found")
   ErrExit()

config = configparser.ConfigParser()
config.read(conffile)

# Check whether config file exists and has [dapgw2email] stanza
if not config.has_section('dapgw2email'):
   log.error("Check " + conffile + " for proper [dapgw2email] section heading")
   ErrExit()

# Check for required options in the config file.  If not found, log error and
# exit.
try:
   ric = config.get('dapgw2email', 'RIC').encode('utf-8')
except configparser.NoOptionError:
   log.error("Check " + conffile + " for proper RIC value in [dapgw2email] section")
   ErrExit()

try:
   smtp = config.get('dapgw2email', 'SMTP')
except configparser.NoOptionError:
   log.error("Check " + conffile + " for proper SMTP value in [dapgw2email] section")
   ErrExit() 

try:
   sender = config.get('dapgw2email', 'SENDER')
except configparser.NoOptionError:
   log.error("Check " + conffile + " for proper SENDER value in [dapgw2email] section")
   ErrExit() 

try:
   recipient = config.get('dapgw2email', 'RECIPIENT')
except configparser.NoOptionError:
   log.error("Check " + conffile + " for proper RECIPIENT value in [dapgw2email] section")
   ErrExit() 

# Create list of optional rubrics (R1-R9 in conf file)
rubrics = ['R'+str(i) for i in range(1, 10)]

# Initialize list of RICs to include pager number
rlist = [ric]

# Loop through dict of optional rubric names and add the rubric value
# to rlist if it exists in the config file
for r in rubrics:
   try:
      rubric_value = config.get('dapgw2email', r).encode('utf-8')
      rlist.append(rubric_value)
   except configparser.NoOptionError:
      pass


myFrom    = "From: Pi-Star <" + sender + ">\n"
myTo      = "To: " + recipient + "\n"
Subject   = "Subject: DAP GW Page To "

header    = myFrom + myTo + Subject 

today = init_log_tail()

while True:
    # Check for new UTC date and switch logfiles
    if today != curr_utc_date():
       p.unregister(f.stdout)
       today = init_log_tail()
    if p.poll(1):
        p_line = f.stdout.readline()
        if b'Queueing' in p_line:
           for rval in rlist:
              if rval in p_line:
                 pos = p_line.find(b'Alphanumeric')
                 message = p_line[pos+15: -2]
                 smtpmsg = header + rval.decode('utf-8') + "\n\n" \
                    + message.decode('utf-8')
                 try:
                    smtpObj = smtplib.SMTP(smtp, 25)
                    smtpObj.sendmail (sender, recipient, smtpmsg)
                    smtpObj.quit
                 except:
                    log.error("Error: Check SMTP configuration.")
                    ErrExit() 
                 break
    time.sleep(1)

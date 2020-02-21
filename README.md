This python3 program is meant to be run on a working Pi-Star system.  It will
monitor incoming DAP GW traffic for messages sent to a specified RIC.  When
detected, it will trigger an email with the contents of the pager message.

This is a great way to play with POCSAG paging for amateur radio without
having to first invest in a pager.

Thanks to the DAPNET (Decentralized Amateur Paging Network) folks for providing
the backend that makes all this work.  Thanks to G4KLX for providing the
gateway software and to MW0MWZ for including it in his Pi-Star distribution.

For more information about amateur radio paging, see https://hampager.de.

Configuration needs to be done in the /etc/dapgw2email.conf file.  You may
specify one primary RIC and up to 9 Rubrics (or other RICs).

A systemd unit service file is included.

Here is the file structure for this project:

├── etc
│   └── dapgw2email.conf
├── lib
│   └── systemd
│       └── system
│           ├── dapgw2email.service
│           └── dapgw2email.timer
├── LICENSE
├── README
└── usr
    └── local
        └── bin
            └── dapgw2email.py

This software is offered under the terms of the GNU General Public License
v3.0.

Dan Srebnick (K2IE)
February 12, 2020

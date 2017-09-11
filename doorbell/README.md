# TofuDoorbell

A simple Python application for a Raspberry Pi to play an MP3 sample
when it detects that a door has been opened.

## Hardware

1. Raspberry Pi B+, 2, 3 etc.
2. Door mounted [reed switch.](https://www.amazon.com/gp/product/B00HR8CT8E)

## Software requirements

1. Raspbian
2. Python
3. python-pigpio
4. mplayer

```
$ sudo apt-get install python-pigpio mplayer
```

## Installation

Run the build.sh script under ./build to create an installable .deb 
repository. It's recommended to add a systemd unit configuration of the 
template:

```[Unit]
Description=Tofu Doorbell

[Service]
ExecStart=/usr/bin/python /opt/tofu-doorbell/tofu-doorbell.py
ExecStop=/usr/bin/pkill -f tofu-doorbell.py
WorkingDirectory=/opt/tofu-doorbell
Restart=always

[Install]
WantedBy=default.target
```

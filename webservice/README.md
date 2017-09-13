# Tofu WebService

A NodeJS application to provide a user with a web interface for managing locally stored audio clips.

![Tofu Webservice screenshot](./images/Tofu-webservice-screenshot-small.png?raw=true "Tofu Webservice screenshot")

## Installation

It's recommended to add a systemd unit configuration of the template:

```
Description=Tofu WebService

[Service]
ExecStart=/usr/bin/node /opt/tofu/ewbservice/tofu-webservice.js
ExecStop=/usr/bin/pkill -f tofu-webservice.js
WorkingDirectory=/opt/tofu/webservice
Restart=always

[Install]
WantedBy=default.target
```

---
title: IoT-HSM Installation
description: Learn how to install IoT-HSM on an Ubuntu server.
---
To get started with IoT-HSM, it is recommend to deploy a Long-Term Support (LTS) version of [Ubuntu Server](https://ubuntu.com/download/server). IoT-HSM has been tested on Ubuntu 24.04 or 25.10. Once Ubuntu is installed and updated, login to a terminal shell, and execute the following commands as the root user. You can access a root shell by entering `sudo su -` at the terminal.
```
apt update
apt -y install curl
curl -sL https://raw.githubusercontent.com/lspiehler/iot-hsm/master/scripts/setup_ubuntu.sh | bash -
```
After the script completes, it will be prompt to set a new password twice—this password will be used for the admin account on the IoT-HSM web interface. Once configured, open a browser and navigate to the IP address of the Ubuntu endpoint, prefixed with `https://`. For example: `https://192.168.1.5`.

See the [Create an HSM CA](create-hsm-ca.md) documentation to create a certificate authority for use with IoT-HSM.
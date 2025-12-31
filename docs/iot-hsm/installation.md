---
title: IoT-HSM Installation
description: Learn how to install IoT-HSM on an Ubuntu server.
---

## Virtual or Physical Machine
When installing IoT-HSM, it is recommend to deploy a Long-Term Support (LTS) version of [Ubuntu Server](https://ubuntu.com/download/server). IoT-HSM has been tested on Ubuntu 24.04 and 25.10. Once Ubuntu is installed and updated, login to a shell, and execute the following commands as the root user. You can become root by entering the command `sudo su -`.
```
apt update
apt -y install curl
curl -sL https://raw.githubusercontent.com/lspiehler/iot-hsm/master/scripts/setup_ubuntu.sh | bash -
```
After the script completes, it will prompt to set a new password twice. This password will be used for the admin account on the IoT-HSM web interface. Once configured, open a browser and navigate to the IP address of the Ubuntu endpoint, prefixed with `https://`. For example: `https://192.168.1.5`.

See the [Create an HSM CA](create-hsm-ca.md) documentation to create a certificate authority for use with IoT-HSM.

## Container Deployment
Below is an example command that can be used to deploy IoT-HSM as a container.
```
docker run -it -d --restart=always --name iot-hsm -e LISTENIP=0.0.0.0 -p 3000:3000 -v iot-hsm:/var/lib/softhsm/tokens -v /var/node/iot-hsm/state:/var/node/iot-hsm/state ghcr.io/lspiehler/iot-hsm:latest
```
IoT-HSM was designed to support all container platforms like those provided by GCP, Azure, and AWS. Advanced knowledge of those platforms may be required for successful deployment. Be sure to mount the appropriate volumes for persistent storage.

No authentication or TLS support is provided by the IoT-HSM containerized deployment. Additional containers (e.g., nginx or Traefik reverse proxies deployed as a sidecar) or cloud resources (load balancers, application gateways, etc) are required to provide these features if desired.

**Note:** Yubikeys are not supported on IoT-HSM container deployments at this time.

See the [Create an HSM CA](create-hsm-ca.md) documentation to create a certificate authority for use with IoT-HSM.
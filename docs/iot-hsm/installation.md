---
title: IoT-HSM Installation
description: Install IoT-HSM on Ubuntu Server or run it as a container, then connect it to PKIaaS.io to keep your CA private keys in hardware.
---

## Virtual or Physical Machine
When installing IoT-HSM, it is recommended to deploy a Long-Term Support (LTS) version of [Ubuntu Server](https://ubuntu.com/download/server). IoT-HSM has been tested on Ubuntu 24.04 and 26.04. Once Ubuntu is installed and updated, log in to a shell, and execute the following commands as the root user. You can become root by entering the command `sudo su -`.
```
apt update
apt -y install curl
curl -sL https://raw.githubusercontent.com/lspiehler/iot-hsm/master/scripts/setup_ubuntu.sh | bash -
```
The script installs the latest release of IoT-HSM (the one shown at [https://github.com/lspiehler/iot-hsm/releases/latest](https://github.com/lspiehler/iot-hsm/releases/latest)), not the newest code on `master`. If it can't look the release up, it stops before installing IoT-HSM.

Once IoT-HSM is installed, the script asks for a name for the appliance, which PKIaaS.io shows instead of the appliance's ID (for example on the IoT-HSM page). Press Enter to use the hostname (offered only when it is a valid name). Without a terminal, for example in automation, the appliance gets no name unless you set it before running the script: `curl -sL ... | AGENT_NAME="Rack 4 HSM" bash -`. Run that as root rather than through `sudo`, which drops `AGENT_NAME`. Run the script in the foreground: in the background it stops at the question. A name is 1 to 64 letters, digits, spaces and `. _ - ( ) # : / @`; one PKIaaS.io wouldn't accept is not saved. To change it later, edit `AGENT_NAME` in `/var/node/iot-hsm/.env` and run `sudo -u iothsm pm2 restart iot-hsm`.

After naming the appliance, the script turns on the firewall (ufw) if it is off. It first allows the TCP ports that sshd listens on, so that turning the firewall on doesn't cut off SSH, then ports 80 and 443 for the web interface (80 only redirects to HTTPS), and then turns ufw on. If ufw is already on, the script leaves its SSH rules as they are and only allows ports 80 and 443. If ufw is off and the script finds no port that sshd listens on, it adds the rules for ports 80 and 443 but leaves ufw off and prints how to turn it on. If you move SSH to another port later, allow the new port in ufw first, for example `ufw allow 2222/tcp`.

After the script completes, it will prompt to set a new password twice. This password will be used for the admin account on the IoT-HSM web interface. Once configured, open a browser and navigate to the IP address of the Ubuntu endpoint, prefixed with `https://`. For example: `https://192.168.1.5`.

See the [Create an HSM CA](create-hsm-ca.md) documentation to create a certificate authority for use with IoT-HSM.

## Container Deployment
Below is an example command that can be used to deploy IoT-HSM as a container.
```
docker run -it -d --restart=always --name iot-hsm -e LISTENIP=0.0.0.0 -p 3000:3000 -v iot-hsm:/var/lib/softhsm/tokens -v /var/node/iot-hsm/state:/var/node/iot-hsm/state ghcr.io/lspiehler/iot-hsm:latest
```
To name the appliance, add `-e AGENT_NAME="Rack 4 HSM"` with your own name. `AGENT_NAME` is the name PKIaaS.io shows for the appliance instead of its ID. A container's hostname is a random ID, so IoT-HSM never sends it; without `AGENT_NAME`, PKIaaS.io shows the ID.

IoT-HSM was designed to support all container platforms like those provided by GCP, Azure, and AWS. Advanced knowledge of those platforms may be required for successful deployment. Be sure to mount the appropriate volumes for persistent storage.

No authentication or TLS support is provided by the IoT-HSM containerized deployment. Additional containers (e.g., nginx or Traefik reverse proxies deployed as a sidecar) or cloud resources (load balancers, application gateways, etc.) are required to provide these features if desired.

**Note:** YubiKeys are not supported on IoT-HSM container deployments at this time.

See the [Create an HSM CA](create-hsm-ca.md) documentation to create a certificate authority for use with IoT-HSM.
---
title: Overview
description: Learn about IoT-HSM and how a YubiKey can be used as a hardware security module (HSM) to securely sign certificates.
---
See the [installation documentation](installation.md) to get started with IoT-HSM.
IoT-HSM is a lightweight application designed to enable a persistent connection between one or more YubiKeys and PKIaaS.io. Once deployed and provisioned for a Certificate Authority (CA), it securely forwards all signing requests for the CA from PKIaaS.io to the IoT-HSM, where the connected YubiKey handles the signing. To ensure robust security, all communications with the IoT-HSM are digitally signed with end-to-end encryption via S/MIME. Advantages of using IoT-HMS with YubiKeys include:

* IoT-HSM is an extremely affordable HSM solution (only the cost of the [YubiKey](https://www.yubico.com/product/yubikey-5-series/yubikey-5-nfc/){:target="_blank"})
* Private keys can be imported or generated on the YubiKey and never leave the device
* One or more YubiKeys can be managed by a single IoT-HSM appliance
* Multiple slots on a YubiKey can be provisioned with different private keys, allowing for multiple CAs to be managed by a single YubiKey
* Yubikey can effortlessly be moved to new hardware or an upgraded install of the IoT-HSM appliance
* Multiple IoT-HSM appliances can be used to provide redundancy and load balancing (requires duplicate private keys to be imported to the Yubikeys on each appliance)

**Note:** IoT-HSM also offers the ability to create a virtual HSM using SoftHSM2, which can be used for testing and development purposes but is not recommended for production use. To create a SoftHSM2 virtual HSM, click "Create SoftHSM2" on the IoT-HSM dashboard.

<iframe width="560" height="315" src="https://www.youtube.com/embed/z5EENNZS1X8?si=ODKocYeNWeNmdD3g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
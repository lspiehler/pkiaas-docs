---
title: Overview
description: Learn about IoT-HSM and the different supported HSMs that can be used with PKIaaS.io.
---
See the [installation documentation](installation.md) to get started with IoT-HSM.
IoT-HSM is a lightweight application designed to allow Google Cloud KMS keys and YubiKeys to be used to protect CA private keys on PKIaaS.io. Once deployed and provisioned for a Certificate Authority (CA), it securely forwards all signing requests for the CA from PKIaaS.io to the IoT-HSM, where the configured HSM handles the signing. To ensure robust security, all communications with the IoT-HSM are digitally signed with end-to-end encryption via S/MIME. Advantages of using IoT-HSM include:

* IoT-HSM is an extremely affordable HSM solution only the cost of the [YubiKey](https://www.yubico.com/product/yubikey-5-series/yubikey-5-nfc/){:target="_blank"} (approximately $50) or [Google Cloud KMS key](https://cloud.google.com/kms/pricing{:target="_blank"}) (approximately $1 - $3 per month depending on usage)
* Private keys can be imported or generated and never leave the device
* One or more HSMs can be managed by a single IoT-HSM appliance
* Multiple slots on a YubiKey can be provisioned with different private keys, allowing for multiple CAs to be managed by a single YubiKey
* Keys can effortlessly be moved to new hardware or an upgraded install of the IoT-HSM appliance
* Multiple IoT-HSM appliances can be used to provide redundancy and load balancing

**Note:** IoT-HSM also offers the ability to create a virtual HSM using SoftHSM2, which can be used for testing and development purposes but is not recommended for production use. To create a SoftHSM2 virtual HSM, click "Create SoftHSM2" on the IoT-HSM dashboard.

<iframe width="560" height="315" src="https://www.youtube.com/embed/z5EENNZS1X8?si=ODKocYeNWeNmdD3g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Next, see [Create an HSM CA](create-hsm-ca.md) to create a CA for use with IoT-HSM.
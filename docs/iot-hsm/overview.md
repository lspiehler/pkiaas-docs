# Overview

See the [installation documentation](installation.md) to get started with IoT-HSM.

## Overview
IoT-HSM is a lightweight application designed to enable a persistent connection between one or more YubiKeys and PKIaaS.io. Once deployed and provisioned for a Certificate Authority (CA), it securely forwards all signing requests for the CA from PKIaaS.io to the IoT-HSM, where the connected YubiKey handles the signing. To ensure robust security, all communications with the IoT-HSM are digitally signed with end-to-end encryption via S/MIME.

<iframe width="560" height="315" src="https://www.youtube.com/embed/z5EENNZS1X8?si=ODKocYeNWeNmdD3g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
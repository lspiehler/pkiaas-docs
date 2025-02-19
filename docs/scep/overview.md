---
title: SCEP Overview
description: Learn about using SCEP to automate the request and issuance of digital certificates from a certificate authority on PKIaaS.io.
---
SCEP (Simple Certificate Enrollment Protocol) is a long-established, open source protocol that automates the request and issuance of digital certificates from a certificate authority over HTTP. SCEP is often used by mobile device management (MDM) solutions to issue certificates to managed devices. It is also often used by network devices, such as routers and switches, to obtain certificates for secure communication.

## Enabling SCEP
PKIaaS.io supports SCEP for certificate enrollment, but it is not enabled by default. SCEP can be enabled and disabled on a per-template basis. To enable SCEP for a template log in to PKIaaS.io and navigate to **Certificate Templates -> Manage Templates**. Click on the template you wish to enable SCEP for, then click "Edit Template" and select the "SCEP" tab. From here, you can enable SCEP and configure the SCEP settings for the template.

## SCEP URL
The SCEP URL is unique to each template. To find the SCEP URL for a template, navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to use and select "Show Template Service URLs" from the menu. This is the URL that devices will use to communicate with PKIaaS.io to request a certificate from the template.

## SCEP Validation
When a device requests a certificate via SCEP, PKIaaS.io will validate the request before issuing the certificate. Multiple validation methods are supported. See the links below for more information on each.

1. [Static Passphrase](static-passphrase.md)
2. [Microsoft NDES Compatibility](microsoft-ndes-compatibility.md)
3. [Intune Integration](intune-integration.md)
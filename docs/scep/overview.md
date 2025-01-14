SCEP (Simple Certificate Enrollment Protocol) is a long-established, open source protocol that automates the request and issuance of digital certificates from a certificate authority over HTTP. SCEP is often used by mobile device management (MDM) solutions to issue certificates to managed devices. It is also often used by network devices, such as routers and switches, to obtain certificates for secure communication.

## Enabling SCEP
PKIaaS.io supports SCEP for certificate enrollment, but it is not enabled by default. SCEP can be enabled and disabled on a per-template basis. To enable SCEP for a template log in to PKIaaS.io and navigate to **Certificate Templates -> Manage Templates**. Click on the template you wish to enable SCEP for, then click "Edit Template" and select the "SCEP" tab. From here, you can enable SCEP and configure the SCEP settings for the template.

## SCEP URL
The SCEP URL is unique to each template. To find the SCEP URL for a template, navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to use and select "Show Template Service URLs" from the menu. This is the URL that devices will use to communicate with PKIaaS.io to request a certificate from the template.

## SCEP Validation
When a device requests a certificate via SCEP, PKIaaS.io will validate the request before issuing the certificate. Multiple validation methods are supported. See the links below for more information on each.

1. [Static Passphrase](static-passphrase)
2. [Microsoft NDES Compatibility](micrsoft-ndes-compatibility)
3. [Intune Integration](intune-integration)

## SCEP Security
SCEP access can be restricted to specific IP addresses. To restrict access to a specific IP address, navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to restrict access to and select the "SCEP" tab. Check the "Enable IP ACL" checkbox and enter the IP address you wish to allow SCEP requests from in the "Allowed IPs" field. Multiple IP addresses can be entered, separated by commas. Using the "Limit access to" drop down, you may choose whether to limit access to SCEP Requests, the Microsoft compatibility UI or both.
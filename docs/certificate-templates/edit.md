---
title: Edit Templates
description: Learn how to edit certificate templates on PKIaaS.io.
---
To edit the settings for a certificate template, login to PKIaaS.io and navigate to **Certificate Templates -> Manage Templates** in the navigation pane on the left of the page. Click on a template and select "Edit Template".

## Options

### General
* **Enabled** - enables/disables the template
* **Allow unsolicited certificate web requests** - enables/disables the "Public Certificate Request" URL for the template
* **Allow the use of a valid certificate to authorize an automatic renewal request** - enables/disables certificate renewal authorization using a previously issued certificate using the renewal options found on the CA's CPS page
    * **Automatically revoke old certificate** - revoke the old certificate used to authorize renewal
    * **Require certificate to be within** - don't allow renewal using a certificate to authorize renewal unless it is within the specified number of days of expiration
    * **Copy subject and SANs from original certificate during renewal** - use the same subject and subject alternative names from the old certificate used to authorize renewal
* **Signing Algorithm** - customize the hash algorithm used to sign certificates
* **Validity Period (Days)** - specify the default length of time the issued certificate will be valid—for manually issued certificates. This option can be overridden at the time of signing when the request is in **X509 Certificates -> Pending Requests**
* **Description** - provide a description for the template

### Subject
To honor the subject attributes requested within the CSR, use the **Supplied by the CSR** option. Otherwise, the subject attributes in the CSR will be overridden by the defaults defined here.

### Key Usage
Select the key usages and extended key usages to be enabled for certificates issued using this template. Custom comma-separated extended key usage OIDs can be entered into the **Custom EKU OIDs** field.

### Basic Constraints
The Basic Constraints extension in an X509 certificate defines whether the certificate is a Certificate Authority (CA) or an end-entity (non-CA) certificate. Set the **Certificate Authority** option to yes if the template will be used to sign subordinate CAs (intermediate CAs) certificate authorities. Path length defines the maximum number of subordinate CAs that can exist below this certificate in the certificate hierarchy.

### CRL / OCSP / AIA / CPS
* **Include AIA Extension in Certificate** - The Authority Information Access (AIA) attribute is an optional but commonly included extension in an X.509 certificate. It provides information about how to access important resources or services related to the certificate issuer. Use this option to enable or disable the AIA attribute in certificates issued using this template.
    * **Custom URL** - Allows customization of the URL where the issuing CA’s certificate (or chain) can be downloaded.
* **Include OCSP Extension in Certificate** - Enable or disable the OCSP Responder attribute within the AIA extension in certificates issued using this template.
* **Include CRL Extension in Certificate** - Enable or disable the CRL Distribution Point (CDP) attribute in certificates issued using this template.
* **Include CPS Extension in Certificate** - Enable or disable the Certificate Policies attribute in certificates issued using this template. This attribute contains the URL to the Certificate Practice Statement (CPS) and the policy identifier.
    * **Policy** - Disable, select a predefined policy identifier, or enter a custom OID.

### SCEP
Simple Certificate Enrollment Protocol is a protocol designed to simplify the process of managing and issuing digital certificates in a scalable and automated manner. It is commonly used in environments where devices like routers, printers, and mobile devices need to enroll for certificates to enable secure communications. The SCEP URL for the template can be found by navigating to **Certificate Templates -> Manage Templates**, next click on a template, and choose the **Show Template Service URLs** option. A modal will appear revealing the template service URLs including the SCEP URL.

* **Enable SCEP protocol** - Enable or disable SCEP for the template.
* **Enable SCEP Static Passphrase** - Enable or disable a static passphrase for SCEP services on the template. This may be required for SCEP processes that require the same passphrase to be used for multiple SCEP clients.
* **Enable Microsoft Intune/Endpoint Manager Integration** - Enable or disable Microsoft Intune SCEP integration for the template.
* **Strip Root from GetCACert Requests** - Exclude the root CA and return only the root in responses to SCEP GetCACert requests.
* **Enable Microsoft SCEP compatibility** - Enable or disable the Microsoft SCEP (NDES) compatibility. This option enabled PKIaaS.io to mimic the /CertSrv/mscep_admin/ URL on Microsoft NDES servers to generate "enrollment challenge passwords" for processes and workflows designed to work with this Microsoft NDES functionality. The URL for this page can be found by navigating to **Certificate Templates -> Manage Templates**, next click on a template, and choose the **SCEP Admin (Microsoft compatibility)** option to navigate to the URL in a new tab.
    * **Enable Microsoft SCEP basic auth** - Enable or disable basic HTTP authentication for the Microsoft SCEP compatibility page. A username and password must be provided if this option is selected.
* **Enable IP ACL** - Enable or disable the IP-based access control list (firewall functionality) for access to SCEP requests, the Microsoft compatibility page (if enabled) or both. Enter a list of IPs allowed to access the resources.

### CT Logs
For templates associated with root CAs or intermediate CAs that chain up to root CAs that require issued certificates to be submitted to certificate transparency logs, enter a comma-separated list of URLs where these certificates should be submitted here. The CT log must support logging for the CA associated with the template. This is something that must be coordinated with the owner of the CT log.
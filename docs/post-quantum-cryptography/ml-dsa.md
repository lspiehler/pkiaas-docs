---
title: ML-DSA
description: Learn how to create a quantum safe certificate authority (CA) using the ML-DSA post-quantum cryptographic algorithm with PKIaaS.io.
---
## Create a ML-DSA Certificate Authority
Login to [PKIaaS.io](https://pkiaas.io/auth/login), and navigate to **Certificate Authorities -> Create New CA**. From the **Key Type** dropdown, select "ML-DSA". In the **Parameter Set** drop down, "65" (security level 2) will be selected by default. A different parameter set may be selected if desired to customize the security level of the private key for the CA. See more information about ML-DSA security levels below. Refer to [Certificate Authorities Overview](../certificate-authorities/overview.md) for more information on the available options in the new CA form. After the form has been completed, click **Create New CA** to create the ML-DSA CA.

### Security Levels (Parameter Sets)
ML-DSA offers parameter sets that meet three security levels: ML-DSA-44, ML-DSA-65, and ML-DSA-87. ML-DSA-44 is intended to meet NIST's level 2 security category, ML-DSA-65 is intended to meet level 3, and ML-DSA-87 is intended to meet level 5. See [https://www.ietf.org/archive/id/draft-salter-lamps-cms-ml-dsa-00.html](https://www.ietf.org/archive/id/draft-salter-lamps-cms-ml-dsa-00.html#name-introduction) for more information.

* **Security Level 2 (ML-DSA-44)** - Attacks on algorithms in the level 2 category are intended to be at least as hard as performing a collision search on SHA256.
* **Security Level 3 (ML-DSA-65)** - Attacks on algorithms in the level 3 category are intended to be at least as hard as performing an exhaustive key search on AES192.
* **Security Level 5 (ML-DSA-87)** - Attacks on algorithms in the level 5 category are intended to be at least as hard as performing an exhaustive key search on AES256.

## Generate ML-DSA Private Keys and CSRs
In order to issue a quantum-safe ML-DSA certificate, a CSR must be generated with a ML-DSA private key. This can be done using tools like OpenSSL with the liboqs provider or online at [https://certificatetools.com/](https://certificatetools.com/) by selecting one of the "Generate ML-DSA-(44|65|87) Private Key (liboqs)" options from the **Private Key** dropdown.

**Note**: In production, it is recommended to generate the private key and CSR on a secure system that is not connected to the internet.

## Issue a ML-DSA Certificate
Navigate to **Certificate Templates -> Manage Templates**, and click on the desired template. From the menu select **Submit CSR**. Paste the contents of a base64 certificate signing request (CSR) generated with a ML-DSA private key and click **Submit**. Navigate to **X509 Certificates -> Pending Requests** to review and approve the request. Click on the pending request to view the details, optionally override requested attributes or validity, and click **Sign** to issue the certificate. Navigate to **X509 Certificates -> Issued Certificates** to view and download the issued certificate.
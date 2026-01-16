---
title: SLH-DSA (formerly SPHINCS+)
description: Learn how to create a quantum safe certificate authority (CA) using the (FIPS 205, formerly SPHINCS+) post-quantum cryptographic algorithm with PKIaaS.io.
---
## Create a SLH-DSA Certificate Authority
Login to [PKIaaS.io](https://www.pkiaas.io/auth/login), and navigate to **Certificate Authorities -> Create New CA**. From the **Key Type** dropdown, select "SLH-DSA". Select the desired parameter set from the **Parameter Set** drop down. See more information about SLH-DSA security levels below. Refer to [Certificate Authorities Overview](../certificate-authorities/overview.md) for more information on the available options in the new CA form. After the form has been completed, click **Create New CA** to create the SLH-DSA CA.

### Security Levels (Parameter Sets)
SLH-DSA offers 12 parameter sets that meet three security levels. SLH-DSA-SHA2-128s, SLH-DSA-SHA2-128f, SLH-DSA-SHAKE-128s and SLH-DSA-SHAKE-128f are intended to meet NIST's level 1 security level. SLH-DSA-SHA2-192s, SLH-DSA-SHA2-192f, SLH-DSA-SHAKE-192s and SLH-DSA-SHAKE-192f are intended to meet level 3. SLH-DSA-SHA2-256s, SLH-DSA-SHA2-256f, SLH-DSA-SHAKE-256s and SLH-DSA-SHAKE-256f are intended to meet level 5. See [https://www.ietf.org/archive/id/draft-ietf-lamps-x509-slhdsa-01.html](https://www.ietf.org/archive/id/draft-ietf-lamps-x509-slhdsa-01.html#name-introduction) for more information.

* **Security Level 1 (SLH-DSA-SHA2|SHAKE-128s|f)** - 128-bit AES equivalent and 3072-bit RSA equivalent
* **Security Level 3 (SLH-DSA-SHA2|SHAKE-192s|f)** - 192-bit AES equivalent and 7680-bit RSA equivalent
* **Security Level 5 (SLH-DSA-SHA2|SHAKE-256s|f)** - 256-bit AES equivalent and 15360-bit RSA equivalent

## Generate SLH-DSA Private Keys and CSRs
In order to issue an SLH-DSA certificate, a CSR must be generated with a SLH-DSA private key. This can be done using tools like OpenSSL (version 3.5 or higher) or online at [https://certificatetools.com/](https://certificatetools.com/) by selecting one of the SLH-DSA private key options from the **Private Key** dropdown.

**Note**: In production, it is recommended to generate the private key and CSR on a secure system that is not connected to the internet.

## Issue a SLH-DSA Certificate
Navigate to **Certificate Templates -> Manage Templates**, and click on the desired template. From the menu select **Submit CSR**. Paste the contents of a certificate signing request (CSR) generated with a SLH-DSA private key and click **Submit**. Navigate to **X509 Certificates -> Pending Requests** to review and approve the request. Click on the pending request to view the details, optionally override requested attributes or validity, and click **Sign** to issue the certificate. Navigate to **X509 Certificates -> Issued Certificates** to view and download the issued certificate.
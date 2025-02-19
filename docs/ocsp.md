---
title: Online Certificate Status Protocol (OCSP)
description: Learn about the Online Certificate Status Protocol (OCSP) service on PKIaaS.io.
---
## Overview
OCSP (Online Certificate Status Protocol) is a network protocol used in Public Key Infrastructure (PKI) to check the revocation status of digital certificates. It allows clients, like web browsers, to verify whether a certificate is still valid or has been revoked without requiring a full download of a Certificate Revocation List (CRL).

## OCSP Signing Certificate
By default, PKIaaS.io generates a certificate with the "OCSP Signing" extended key usage (EKU) attribute for each CA when the CA is created. The certificate will appear in **X509 Certificates -> Issued Certificates** with the common name "PKIaaS.io OCSP Responder". This certificate is used to sign OCSP responses for the CA. When the certificate expires or is manually revoked, a new OCSP signing certificate will be generated on demand during the next OCSP request.

## OCSP Responder URL
To find the OCSP responder URL along with many other service URLs, login to [PKIaaS.io](https://pkiaas.io/auth/login), and navigate to **Certificate Authorities -> Manage CAs**. Click on the desired CA, and Select "Show CA Service URLs". A valid OCSP request must be sent to the OCSP responder URL to receive a signed OCSP response. Tools like the [OCSP Checker](https://certificatetools.com/ocsp-checker) can be used to return the OCSP response for a certificate.

## OCSP in the AIA Extension
By default, the OCSP URL is also encoded in issued certificates in the Authority Information Access (AIA) extension. This can be changed within a certificate template by navigating to **Certificate Templates -> Manage Templates**, clicking on a template, and selecting "Edit Template". The OCSP URL can be removed from certificates issues using the template by unchecking "Include OCSP Extension in Certificate" in the **CRL / OCSP / AIA / CPS** section of the template settings.
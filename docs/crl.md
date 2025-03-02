---
title: Certificate Revocation List (CRL)
description: Learn about Certificate Revocation Lists (CRLs) and how to access them from PKIaaS.io.
---
## Overview
A CRL (Certificate Revocation List) is a list published by a Certificate Authority (CA) that contains the serial numbers of digital certificates that have been revoked before their scheduled expiration. This list is part of Public Key Infrastructure (PKI) and serves as a mechanism to help entities verify whether a certificate is still valid.

## CRL Generation
PKIaaS.io automatically generates CRLs on demand when a HTTP request is received to download the CRL. CRLs are cached and valid for a period of 30 days from the time of generation. When the CRL expires or another certificate is revoked, the cache is deleted, and a new CRL is generated on demand during the next HTTP request to download the CRL.

## CRL URL
To find the CRL URL along with many other service URLs, login to [PKIaaS.io](https://www.pkiaas.io/auth/login), and navigate to **Certificate Authorities -> Manage CAs**. Click on the desired CA, and Select "Show CA Service URLs". Click the CRL URL to download the CRL.

## CRL Distribution Point
By default, the CRL URL is also encoded in issued certificates in the CRL Distribution Points (CDP) extension. This can be changed within a certificate template by navigating to **Certificate Templates -> Manage Templates**, clicking on a template, and selecting "Edit Template". The CRL URL can be removed from certificates issues using the template by unchecking "Include CRL Extension in Certificate" in the **CRL / OCSP / AIA / CPS** section of the template settings.
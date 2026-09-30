---
title: Certificate Issuance Workflows Overview
description: Compare the manual and automated ways to issue certificates on PKIaaS.io, from signing a CSR in the admin UI to enrolling via ACME or SCEP.
---
PKIaaS.io supports multiple workflows for issuing certificates. See the links below for more information on each workflow:
## Manual Workflows
* [Sign a CSR from the Admin UI](sign-a-csr-from-the-admin-ui.md)

## Automated Workflows
* [Issue Certificates via ACME](../acme/overview.md)
* [Issue Certificates via SCEP](../scep/overview.md)

**Note**: All expired certificates are automatically removed from the system 30 days after expiration. This ensures the certificate management system remains performant and only retains valid, relevant certificates.
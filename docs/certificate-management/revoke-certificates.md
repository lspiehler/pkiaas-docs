---
title: Revoke Certificates
description: Learn how to revoke certificates on PKIaaS.io.
---
## Revoke a Certificate
To revoke a certificate, login to PKIaaS.io and navigate to **X509 Certificates -> Issued Certificates** in the navigation pane on the left of the page. Click on the certificate you'd like to revoke and select the "Revocation" tab in the modal. Choose an option from the "Revocation Reason" dropdown and click "Revoke".

## Unrevoke a Certificate
A certificate can only be unrevoked if it was revoked using the certificate hold revocation reason. To unrevoke a certificate, navigate to **X509 Certificates -> Issued Certificates** in the navigation pane on the left of the page. Click on the certificate you'd like to unrevoke and select the "Revocation" tab in the modal. If the certificate was revoked using the "certificateHold" revocation reason, an "Unrevoke" button will be available to undo the revocation.

**Note:** Any revocation reason other than "certificateHold" will result in a permanent revocation that cannot be undone.
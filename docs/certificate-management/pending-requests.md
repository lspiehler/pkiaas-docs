---
title: Pending Requests
description: Learn how to review and approve pending certificate requests on PKIaaS.io.
---
"Pending Requests" is a list of certificate requests that have been submitted but not yet signed. To view the list of pending requests, login to [PKIaaS.io](https://www.pkiaas.io/auth/login), and navigate to **X509 Certificates -> Pending Requests**. Click on the pending certificate request to view the details of the request. A modal will appear with the details of the request, including the CSR, the requested attributes, and the amount of time the certificate will be valid for, based on the template that was used to submit the request. At the bottom of the modal, you can approve or reject the request by clicking "Sign" or "Decline" respectively. If you approve the request, the certificate will be signed and the certificate will appear in the list of issued certificates by navigating to **X509 Certificates -> Issued Certificates**. See more information below for options to override the default validity period and attributes requested in the CSR.

## Override Requested Attributes

Before approving a pending certificate request, you have the option to override the attributes requested in the CSR before it is signed. To override the requested attributes, click on the "Requested Attributes" tab in the pending request approval modal and click "Override requested attributes". The form will become active, allowing the existing attributes to be removed and new attributes to be added. This can be useful for adding missing SANs or subject attributes to the certificate.

## Override Validity Period

Before approving a pending certificate request, you have the option to override the default validity period of the template that was used to submit the CSR. To override the validity period, click on the "Validity" tab in the pending request approval modal and click "Override validity time". The form will become active, allowing the validity period to be changed. Two options exist, allow the administrator to choose whether to set the validity period in days relative to the current time or select the start and end date and time of validity. The latter option can be used to ensure the certificate isn't valid until a specific date in the future.
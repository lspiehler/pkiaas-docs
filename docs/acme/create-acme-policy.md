---
title: Create an ACME Policy
description: Create an ACME policy on PKIaaS.io to bind ACME requests to a certificate template, and pre-approve domains to skip HTTP and DNS challenges.
---
An ACME policy associates ACME certificate requests with a specified certificate template and allows a comma-separated list of "pre-approved domains" to be supplied. Pre-approved domains will be automatically authorized and will not be required to do any ACME HTTP or DNS challenges. Wildcard domains are supported to pre-approve an entire root domain and all subdomains.

To create an ACME policy, log in to PKIaaS.io and navigate to **ACME -> Policies**. Click "Create", enter a unique name for the new ACME policy, select which template should be used when signing certificates requested using this policy, optionally enter any pre-approved domains, and click "Create Policy."

Next, see [Generate EAB Credentials](generate-eab-credentials.md).
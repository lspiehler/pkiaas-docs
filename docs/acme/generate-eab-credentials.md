---
title: Generate EAB Credentials
description: Learn how to generate external account binding (EAB) credentials for registering a new ACME account on PKIaaS.io.
---
An ACME policy must be created before EAB credentials can be generated. See [Create an ACME Policy](create-acme-policy.md) if this step hasn't been completed yet.

The use of EAB (external account binding) allows PKIaaS.io to associate ACME accounts with a specific user's PKIaaS.io account, CA, and ACME policy. To generate an EAB for registering a new ACME account, login to PKIaaS.io and navigate to **ACME -> Policies**. Click the gears in the "External Account Bindings" column of one of the ACME policies to navigate to the EAB management page for the policy and click "Create". Enter a unique name for the EAB. Enter the desired value for "Allowed Use Count". This value represents the number of times this EAB can be used to register unique ACME accounts. Lastly, enter the expiration date after which ACME new account registrations will no longer be authorized with this EAB and click "Create EAB".

When the new EAB is generated, a modal will appear providing the ACME directory URL, the EAB KID and HMAC Key, and some example commands to use the values provided to register a new ACME account using the certbot ACME client. These values can be used to register an ACME account with any ACME client that supports external account bindings. The KID and HMAC Key will only be displayed once, so be sure to copy them before closing the modal.

**Note:** After an ACME account is registered with an EAB, it is permanently associated with the policy the EAB was generated for. It is safe to delete an EAB after an ACME account had been registered with it.

Next, see [Register an ACME Account](register-acme-account.md).
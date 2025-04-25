---
title: Microsoft Intune Integration
description: Learn how to integrate PKIaaS.io with Microsoft Intune for SCEP certificate issuance.
---
PKIaaS.io natively supports SCEP integration with Microsoft Intune allowing certificates to be validated and issued to devices managed by Intune.

## Prerequisites
Before the Intune integration can be configured, communication must be authorized between PKIaaS.io and Intune. Follow Microsoft"s documentation to configure the necessary permissions and create an application registration in Azure AD. [https://learn.microsoft.com/en-us/mem/intune/protect/certificate-authority-add-scep-overview](https://learn.microsoft.com/en-us/mem/intune/protect/certificate-authority-add-scep-overview#authorize-communication-between-ca-and-intune){:target="_blank"}

## Enabling Intune Integration
To enable Intune integration, login to [PKIaaS.io](https://www.pkiaas.io/auth/login), and navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to enable Microsoft Intune integration for, then click "Edit Template" and select the "SCEP" tab. Check the "Enable Microsoft Intune/Endpoint Manager Integration" checkbox. A form will appear requiring the following information:

* **Tenant ID:** the tenant ID for your Azure tenant (refer to step 6 from the [Microsoft Intune documentation](https://learn.microsoft.com/en-us/mem/intune/protect/certificate-authority-add-scep-overview#authorize-communication-between-ca-and-intune){:target="_blank"})
* **Application (client) ID:** the application (client) ID for the application registration created previously in Azure AD (refer to step 4 from the [Microsoft Intune documentation](https://learn.microsoft.com/en-us/mem/intune/protect/certificate-authority-add-scep-overview#authorize-communication-between-ca-and-intune){:target="_blank"})
* **Client Secret:** the client secret for the application registration created previously in Azure AD (refer to step 5 from the [Microsoft Intune documentation](https://learn.microsoft.com/en-us/mem/intune/protect/certificate-authority-add-scep-overview#authorize-communication-between-ca-and-intune){:target="_blank"})

Finally, click "Save Template" to enable the integration.

## Create and assign SCEP certificate profiles in Intune
After the integration is enabled, the remainder of the configuration is done in Intune. Follow the steps in the [https://learn.microsoft.com/en-us/mem/intune/protect/certificates-profile-scep](https://learn.microsoft.com/en-us/mem/intune/protect/certificates-profile-scep){:target="_blank"} to create and assign SCEP certificate profiles in Intune. Be sure to have the template SCEP URL handy while configuring the SCEP certificate profile. See [SCEP Overview](overview.md/#scep-url) for help finding the URL for the template.
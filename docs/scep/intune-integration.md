---
title: Microsoft Intune Integration
description: Integrate PKIaaS.io with Microsoft Intune to validate and issue SCEP certificates to managed devices, with one-click setup or your own Microsoft Entra app registration.
---
PKIaaS.io natively supports SCEP integration with Microsoft Intune, allowing certificates to be validated and issued to devices managed by Intune. The integration can be connected automatically with one click, or configured with an app registration you create in Microsoft Entra ID.

## Enabling Intune Integration
To enable Intune integration, log in to [PKIaaS.io](https://www.pkiaas.io/auth/login), and navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to enable Microsoft Intune integration for, then click "Edit Template" and select the "SCEP" tab. Check the "Enable Microsoft Intune/Endpoint Manager Integration" checkbox, then connect automatically or use your own app registration.

### Connect Automatically (Recommended)
Click "Connect to Intune". You will be redirected to Microsoft to sign in as a Global Administrator or Privileged Role Administrator for your tenant and approve the PKIaaS.io Intune Connector. The connector requests two application permissions: **SCEP challenge validation** (Intune) and **Read all applications** (Microsoft Graph, used to locate your tenant's Intune SCEP validation service). After approving, you will be returned to the template, which will show that it is connected. No app registration or client secret is needed.

**Note:** Save any other changes to the template before clicking "Connect to Intune". Microsoft may take a few minutes to activate a new connection. If another template on the same certificate authority is already connected, click "Use tenant" to connect without approving again.

To disconnect, uncheck "Enable Microsoft Intune/Endpoint Manager Integration" and click "Save Template". Deleting the PKIaaS.io Intune Connector from **Enterprise applications** in Microsoft Entra ID disconnects every template using your tenant.

### Use Your Own App Registration
Click "Use my own app registration instead", then create an app registration by following Microsoft's instructions to [authorize communication between CA and Intune](https://learn.microsoft.com/en-us/intune/fundamentals/certificates/third-party-ca-scep#authorize-communication-between-ca-and-intune){:target="_blank"}. Enter the following information:

* **Tenant ID:** your tenant ID or primary domain (e.g. contoso.onmicrosoft.com)
* **Application (client) ID:** found on the app registration's Overview page
* **Client Secret:** the client secret value created under **Certificates & secrets**

Finally, click "Save Template" to enable the integration.

**Note:** Client secrets expire. When the secret expires, Intune validation will fail until a new client secret is saved on the template, or the template is connected automatically.

## Create and assign SCEP certificate profiles in Intune
After the integration is enabled, the remainder of the configuration is done in Intune. Follow the steps at [https://learn.microsoft.com/en-us/intune/device-configuration/certificates/scep-profiles](https://learn.microsoft.com/en-us/intune/device-configuration/certificates/scep-profiles){:target="_blank"} to create and assign SCEP certificate profiles in Intune. Be sure to have the template SCEP URL handy while configuring the SCEP certificate profile. See [SCEP Overview](overview.md#scep-url) for help finding the URL for the template.
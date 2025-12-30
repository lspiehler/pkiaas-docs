---
title: IoT-HSM Provisioning
description: Learn how to provision a certificate authority on PKIaaS.io to delegate signing operations to an HSM managed by IoT-HSM.
---
If you haven't yet deployed IoT-HSM, see the [installation documentation](installation.md) to get started.

### Create a CA with an HSM Key on PKIaaS.io
In order for a certificate authority on PKIaaS.io to delegate signing operations to an HSM managed by IoT-HSM, it must first be provisioned to do so. The first step in this process is to select the "HSM" option as the "Key Type" when creating a new certificate authority on the **Certificate Authorities -> Create new CA** page.

### Retrieve HSM Provisioning Certificate from PKIaaS.io
After clicking "Create New CA," the browser will navigate to a page showing the "HSM Provisioning Certificate." This will be used as a template to configure the new CA on the IoT-HSM appliance.

**Note:** If at any time you need to navigate back to this page, go to **Certificate Authorities -> Manage CAs**, click on the CA and select "Download HSM Provisioning Certificate" from the menu.

See the [configuration documentation](configuration.md) to configure IoT-HSM to sign requests for the new CA.
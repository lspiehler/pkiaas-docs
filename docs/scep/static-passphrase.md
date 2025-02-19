---
title: SCEP Static Passphrase
description: Learn how to enable and configure a static passphrase for SCEP certificate requests on PKIaaS.io.
---
PKIaaS.io supports the use of a static passphrase as a validation method for SCEP certificate requests, however, using a static password is generally considered a security risk due to its potential for unauthorized access if compromised. For this reason, we recommend using a more secure validation method, such as Microsoft NDES Compatibility or Intune Integration, whenever possible.

## Enable Static Passphrase
Within the SCEP tab of the template configuration, check the "Enable SCEP Static Passphrase" checkbox. Click the input that says "Click to Generate" to generate a passphrase. This passphrase will not be visible after the template is saved, so be sure to copy it to a secure location before saving.

**Note:** The passphrase can be updated in the future by clicking the "Click to Generate" input again. This will generate a new passphrase and invalidate the old one. If ever it is clicked by mistake, be sure to click "Cancel" in the template editor to keep the original passphrase.
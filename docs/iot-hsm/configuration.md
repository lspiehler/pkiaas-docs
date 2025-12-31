---
title: IoT-HSM Configuration
description: Learn how to provision a certificate authority on PKIaaS.io to delegate signing operations to an HSM managed by IoT-HSM.
---
If you haven't yet created an HSM CA and retrieved the provisioning certificate, see the [Create an HSM CA](create-hsm-ca.md) documentation before proceeding. Also, make sure your HSM is ready for use. See documentation for your HSM if it isn't showing up on the IoT-HSM dashboard.

* [Yubikey](yubikey.md)
* [Google Cloud KMS](google-cloud-kms.md)
* [SoftHSM2](softhsm2.md) (Not recommended for production use)

### Prepare the Private Key on the IoT-HSM
Login to the IoT-HSM. From the "HSM Options..." dropdown on one of the available HSMs, choose "Provision a New Slot." This will navigate to the provisioning wizard. Choose the slot to provision and a key option.

For Google Cloud KMS keys, no additional options are needed because keys are managed within Google Cloud.

The "Generate" option (recommended) will generate a new private key on the HSM slot using the "Key Type" option provided. The "Import" option allows an existing private key to be imported to the HSM slot. This option should only be used when the private key has been handled with extreme care and is ideal under circumstances when it is important to have a backup of the private key or if multiple IoT-HSMs will be provisioned with the same private key for redundancy.

### Import the HSM Provisioning Certificate to the IoT-HSM
#### Self-Signed Root CA
After preparing the private key, the next page in the provisioning wizard is where the "HSM Provisioning Certificate" generated in a previous step will be submitted. If a self-signed root CA is being generated, leave the first option selected, paste the provisioning certificate into the text area, and click submit.
#### Intermediate CA
If this CA will be an intermediate CA, select the option to generate a CSR, paste the provisioning certificate into the text area, and click submit. A modal will appear with a CSR that will need to be signed by the root CA issuing the certificate for this intermediate. Finally, select the last option in the dropdown and paste the certificate signed by the root using the provided CSR and click submit.
#### Import a Signed Certificate
Import a certificate after signing the CSR generated using the "Intermediate CA" option. This option may also be used after updating IoT-HSM or migrating to a new appliance and the original certificate needs to be re-associated with the key.

**Note:** If at any time you need to navigate back to this page, go to the IoT-HSM home page, select the slot being provisioned from the "Configured Slots..." drop down, and click "Complete Provisioning."

### Import the New Certificate from the IoT-HSM to PKIaaS.io

This is the final important step that will associate the newly provisioned HSM with the CA on PKIaaS.io.

Navigate to the IoT-HSM home page. Select the newly provisioned slot from the "Configured Slots..." drop down and click "View Certificate." Copy the certificate to the clipboard and on PKIaaS.io, navigate to **Certificate Authorities -> Manage CAs**, click on the CA being provisioned, and select "Import Signed Certificate." Paste the certificate copied from the IoT-HSM into the text area and click "Import Certificate."

A prompt will appear instructing to restart the IoT-HSM device. On the IoT-HSM home page, click "Reload" in the navigation bar at the top. Click "Import Certificate" again on the PKIaaS.io import signed CA page. If the imported certificate is an intermediate CA and PKIaaS.io is unable to download the certificate chain, a modal will appear prompting for the chain, including all intermediates and the root, to be supplied before the import can be completed.

### Provisioning Complete
When the steps have all be completed successfully, all signing requests for the provisioned CA will be delegated to the HSM on the IoT-HSM. Signing operations will fail if the IoT-HSM is not online with the HSM configured/inserted.

The number of successfully connected HSM slots will appear at the top right of the IoT-HSM home page. It may be necessary to refresh the page to see the updated status, as it may take a few moments to connect to PKIaaS.io. When a slot is selected from the "Configured Slots..." dropdown on one of the HSMs, the status will be displayed, indicating whether the slot is connected successfully.
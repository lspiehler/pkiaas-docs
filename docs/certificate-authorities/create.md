---
title: Create Certificate Authorities
description: Create a root or intermediate certificate authority on PKIaaS.io, including generating a CSR and importing the signed certificate to activate it.
---
## Create a Root CA
Users can create a root certificate authority by logging in to PKIaaS.io and navigating to **Certificate Authorities -> Create New CA**. Fill out the form with the appropriate options for the desired CA. See [certificate authority overview](overview.md) for documentation on all of the available options. When creating a root CA, it is necessary to leave the "CSR Only" option at the bottom of the form unchecked. Upon clicking "Create New CA," a new private key will be generated, and a self-signed, root certificate authority will be created and ready to issue certificates. See the [getting started](../getting-started.md#issue-a-certificate) guide for more documentation about issuing certificates.

## Create an Intermediate/Subordinate CA
To create an intermediate/subordinate certificate authority, ensure that the "CSR Only" option is selected on the **Certificate Authorities -> Create New CA** page when selecting the options for the desired CA. See [certificate authority overview](overview.md) for documentation on all of the available options. Upon clicking "Create New CA," a new private key will be generated, and a CSR will be created. The browser will be redirected to a page containing the CSR where it can be copied to the clipboard and signed by another certificate authority.

**Note:** If at any time you need to navigate back to the CSR page, go to **Certificate Authorities -> Manage CAs**, click on the CA and select "Download/Copy CSR" from the menu.

### Sign the CSR with a CA Outside PKIaaS.io
If a certificate authority not managed by PKIaaS.io will be used to sign the CSR, see the documentation for that CA on how to do so. The signed certificate must include a **Subject Key Identifier** extension, because every certificate PKIaaS.io issues identifies its CA by that key identifier. With OpenSSL, add this line to the extensions used to sign the CSR:

```
subjectKeyIdentifier = hash
```

When the certificate is imported (see the last step below), PKIaaS.io first signs a test certificate with it. If that fails, the certificate is not imported, a message explains what to change, and the CA's log has the details. The CA keeps its CSR, so a corrected certificate can be imported on the same page. If PKIaaS.io can't download the signing CA's certificate chain, a "Manually Import Trust Chain" dialog asks for the chain, including all intermediates and the root.

### Sign the CSR with a Root CA on PKIaaS.io
The following instructions detail how to sign the CSR with a CA managed by PKIaaS.io.

While logged into PKIaaS.io, select the signing root CA from the dropdown at the top of the page. This will switch the context of the admin page to the selected CA. If a template for creating certificate authorities has not already been created, navigate to **Certificate Templates -> Create Template**. Enter "Intermediate CA" as the template name and choose "Certificate Authority" as the starter template. The browser will be directed to a page where the template can optionally be customized. Click "Save" to finish creating the new template.

The browser should now be at the **Certificate Templates -> Manage Template** page. Click on the "Intermediate CA" template and select "Submit CSR" from the menu. Paste the CSR copied to the clipboard in a previous step and click submit. See the note above for instructions to navigate back to the CSR if needed.

The submitted CSR must now be approved in order to be signed. Navigate to **X509/Certificates -> Pending Requests**. Click on the pending certificate request for the new intermediate CA. A modal will appear where some certificate attributes can optionally be overridden. Click "Sign" to sign the submitted CSR and issue the certificate.

Finally, navigate to **X509/Certificates -> Issued Certificates**. Click on the newly issued certificate and copy it to the clipboard. This certificate must be imported to finish creating the new intermediate CA. Navigate to **Certificate Authorities -> Manage CAs**, click on the new intermediate CA and choose "Import Signed Certificate" from the menu. Paste the signed certificate into the text area and click "Import Certificate." The intermediate CA is now ready to issue certificates. Select it from the dropdown at the top of the page to begin using it.
# Getting Started

## Login
Getting started with PKIaaS.io is easy! All you need to do is click "Manage PKI" at the top right of the main page and choose the login you'd like to use.

## Create a Certificate Authority
All the certificates you'll create need to be signed by a certificate authority, so the first step is to create one. Navigating to any other page of the site before you've created a CA will redirect you back to a page forcing you to create one. If you're logging in for the first time, and you haven't created a CA before, you'll be asked to choose between a managed CA and a CA backed by an HSM. If you're new to PKI or you'd just like to take PKIaaS.io for a test drive, it would be best to choose the managed option to get going more quickly. Read more about these options [here](certificate-authorities/overview.md).

### CA Configuration Options
If you're still learning about PKI, feel free to use the default options and just update the name when creating your first CA. This is the easiest option to start issuing certificates and getting a feel for the site. When you're done choosing options, click "Create New CA". You'll then be redirected to the "Manage CAs" page and your new CA will appear in the drop down at the top of the page.

### Switch CAs
If you create more than one CA, you'll have the option of switching between them by selecting the one you'd like to manage from the dropdown at the top of the PKI management page to the right of the navigation pane. All other pages on the site will show only the resources—templates, certificates, services, etc.—within the context of the selected CA.

## Using Your New CA
Select the CA you want to work with from the dropdown at the top to the right of the navigation pane. This dropdown changes the scope of the site to manage the active CA. All actions performed—signing certificates, creating templates, creating ACME policies, etc.—will be done within the context of the selected CA.

## Certificate Templates

### Manage Templates
Certificate templates can be managed by navigating to **Certificate Templates -> Manage Templates** in the navigation pane on the left of the page. Certificate templates are used to enforce compliance of predefined standards for issuing certificates with your CA. These standards include key usages, subject attributes, basic constraints, and other certificate attributes. The use of templates is important to prevent accidental mis-issuance and to ensure that issued certificates are compliant with your security practices. All certificate signing on PKIaaS.io will be associated with a template.

### Create New Templates
By default, a "Web Server" template is automatically built for every CA that is created. This template has a good out-of-the-box configuration for issuing TLS/SSL certificates for web servers, but new, custom certificate templates can be created by navigating to **Certificate Templates -> Create Template**. Enter a name for the template and choose default settings by selecting an option from the "Starter Template" dropdown. Click "Create Template" to proceed to the configuration page, where the template options can be customized. See more information on the available options [here](certificate-templates/edit.md).  Once satisfied with the settings, click "Save" to finalize the changes and return to the template management page.

## Issue a Certificate
In the navigation page on the left, navigate to **Certificate Templates -> Manage Templates** and click on the template you'd like to use. From the menu, you can choose either, "Public Certificate Request", "Submit CSR", or "Create Pre-Approved Request." These options support various workflows for issuing certificates.

### Public Certificate Request
If your workflow involves receiving certificate requests from users, the "Public Certificate Request" option allows you to send an email to users inviting them to easily submit a certificate request. It also shows the public URL that can be shared for others to submit a certificate request. This option allows users to submit a CSR or fill out a form containing the desired subject attributes and SANs. The latter option can be helpful for users that are not familiar with x509 certificates and includes an option to generate a private key automatically in the browser when the user claims their certificate after it is approved. To review and approve these requests, navigate to **X509 Certificates -> Pending Requests**.

### Submit CSR
The "Submit CSR" option provides an input field to paste the contents of a certificate signing request. To review and approve these requests, navigate to **X509 Certificates -> Pending Requests**.

### Create Pre-Approved Request
The "Create Pre-Approved Request" feature enables a PKI administrator to pre-configure all the settings typically chosen during the approval process for a pending certificate request. The administrator can either redeem the certificate immediately or send an email to the user, inviting them to claim it. In the certificate claim workflow, the user can set a password to protect the PKCS#12 file, and a 2048-bit RSA private key will be generated in the browser. Alternatively, a CSR can be submitted, however, the subject attributes and SANs specified in it will be overridden by the pre-approved attributes in the signed certificate.

## Approve Pending Certificate Requests
Certificates requested using the "Public Certificate Request" or "Submit CSR" options require approval. The requests pending approval can be found by navigating to **X509 Certificates -> Pending Requests**. Here you will find options to Approve, Sign, Decline, or Re-Send emails for various types of certificate requests. Not all options are available for all types of certificate request workflows. These options can be performed in bulk, or the requests can be selected individually where additional options are provided to override subject attributes, subject alternative names (SANs), and to customize the validity time of the certificate instead of taking the template default.
# Getting Started

## Login
Getting started with PKIaaS.io is easy! All you need to do is click "Manage PKI" at the top right of the main page and choose the login you'd like to use.

## Create a Certificate Authority
All of the certificates you'll create need to be signed by a certificate authority, so the first step is to create one. Navigating to any other page of the site before you've create a CA will redirect you back to a page forcing you to create one. If you're logging in for the first time, and you haven't created a CA before, you'll be asked to choose between a managed CA and a CA by an HSM. If you're new to PKI or you'd just like to take PKIaaS.io for a test drive, it would be best to choose the managed option to get going more quickly. Read more about these options [here](/certificate-authorities/overview/).

### CA Configuration Options
If you're still learning about PKI, feel free to use the default options and just update the name when creating your first CA. This is the easiest option to start issuing certificates and getting a feel for the site. When you're done choosing options, click "Create New CA". You'll then be redirected to the "Manage CAs" page and your new CA will appear in the drop down at the top of the page.

### Switch CAs
If you create more than one CA, you'll have the option of switching between them by selecting the one you'd like to manage from the dropdown at the top of the PKI management page to the right of the navigation pane. All other pages on the site will show only the resources—templates, certificates, services, etc—within the context of the selected CA.

## Using Your New CA
Select the CA you want to work with from the dropdown at the top to the right of the navigation pane. This dropdown changes the scope of the site to manage the active CA. All actions performed—signing certificates, creating templates, creating ACME policies, etc—will be done within the context of the selected CA.

## Manage Templates
Certificate templates can be created and managed by navigating to "Certificate Templates" in the navigation pane on the left of the page. Certificate templates are used to enforce compliance of certain standards for issuing certificates from your CA. These standards include key usages, subject attributes, basic constraints, and other certificate attributes. These use of templates is important to prevent accidental misissuance and to ensure that issued certificates are complant with your security practices. All certificate signing on PKIaaS.io will be associated with a template.

## Issue a Certificate
In the navigation page on the left, navigate to **Certificate Templates -> Manage Templates** and click on the template you'd like to use. From the menu, you can choose either, "Public Certificate Request", "Submit CSR", or "Create Pre-Approved Request." These options support various workflows for issuing certificates.

### Public Certificate Request
If your role is primarily to manage your PKI, and your workflow involves receiving certificate requests from users, this option allows you to send an email to users inviting them to easily submit a certificate request. It also shows the public URL that can be shared for others to submit a certificate request. This option allows users to submit a CSR or fill out a form containing the desired subject attributes and SANs. The latter option can be helpful for users that are not familiar with x509 certificates and includes an option to generate a private key automatically in the browser when they claim their certificate after it is approved.
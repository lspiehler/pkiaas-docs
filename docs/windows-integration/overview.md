---
title: Windows Integration Overview
description: Learn how to integrate PKIaaS.io with Windows for certificate issuance and automatic renewal.
---
PKIaaS.io supports Microsoft Certificate Enrollment Policy Web Service and Certificate Enrollment Web Service, also known as CEP and CES, to enable certificate issuance and automatic renewal for Windows devices. This integration allows Windows clients to request certificates from PKIaaS.io seamlessly using the native Windows certificate enrollment features. For more information about CEP and CES, see the Microsoft documentation below:

* [Certificate Enrollment Web Services in Active Directory Certificate Services](https://learn.microsoft.com/en-us/archive/technet-wiki/7734.certificate-enrollment-web-services-in-active-directory-certificate-services)
* [MS-WCEP (CEP) Protocol Documentation](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wcep)
* [MS-WSTEP (CES) Protocol Documentation](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wstep)
* [Client Configuration for Key-Based Renewal](https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/certificate-enrollment-certificate-key-based-renewal#configure-the-client-computer)

CEP is used to provide certificate enrollment policy information to Windows clients, allowing them to understand which templates are available for certificate requests. CES is used to handle the actual certificate enrollment requests from Windows clients, including the issuance and renewal of certificates. CES is particularly useful for automatic certificate renewal, as it allows Windows clients to renew certificates without user intervention.

## Authentication
PKIaaS.io supports Username/Password and X.509 Certificate authentication methods on Windows clients for both Certificate Enrollment Policy Web Service (CEP) and Certificate Enrollment Web Service (CES). X.509 Certificate authentication with the CES service can only be used for certificate renewal. Username and password must be used for new certificate enrollment.

The username and password for CEP and CES can be defined in the CA edit and template edit pages, respectively, in their respective tabs. The username and password can be unique for each service or the option "Use CEP Credentials" can be selected within the template configuration to use the same credentials as CEP. The username and password may also be unique for each template, allowing for granular control over which templates can be used by users.

## Enabling Windows Integration
CEP can be enabled by navigating to **Certificate Authorities -> Manage CAs** in the navigation pane on the left side of the page. Click on the CA you want to enable CEP on, and select **Edit CA**. Navigate to the **CEP** tab and select the "Enable Microsoft Certificate Enrollment Policy Web Service (CEP)" checkbox. A mandatory username and password field will appear, allowing you to set the credentials for the CEP service. Click "Save" to apply the changes.

CES can be enabled by navigating to **Certificate Templates -> Manage Templates** in the navigation pane on the left side of the page. Click on the template you want to enable CES on, and select **Edit Template**. Navigate to the **CES** tab and select the "Enable Microsoft Certificate Enrollment Web Service (CES)" checkbox. This option is not available unless CEP has been enabled on the CA the template is associated with. Additional fields will appear, allowing the CES service to be configured. The username and password can be set to the same credentials as CEP by selecting the "Use CEP Credentials" checkbox, or they can be set to unique values. The username and password cannot be left blank if the "Use CEP Credentials" option is not selected. Click "Save" to apply the changes.

CES must be manually enabled on each template that will be used for certificate issuance on Windows clients. All CES enabled templates will appear on windows clients when requesting certificates, however, unique usernames and passwords can be set for each template to control access to certificate issuance by each template.

## Template Types
CES enabled "Computer" templates will appear on windows clients when requesting machine certificates, and CES enabled "User" templates will appear on windows clients when requesting user certificates. Be sure to create the appropriate template type for the intended use case. The template type can be set when creating a new template or editing an existing template by navigating to the **CES** tab within the template edit page. The "Template Type" dropdown allows you to select either "Computer" or "User" as the template type.

## Cryptography Options
The cryptography options for CES enabled templates can be configured by navigating to the **CES** tab within the template edit page. The "Cryptography" dropdown allows you to select the cryptographic algorithms that will be available for use when requesting certificates with the template. The "Minimum Key Size" dropdown allows you to set the minimum key size that will be enforced when requesting certificates. The minimum key size dropdown may not be present, depending on the selected cryptographic algorithms. A list of Cryptographic Storage Providers can be selected to limit the available CSPs for use when requesting certificates with the template. Only the selected CSPs will be available for use when requesting certificates with the template. If none are selected, all CSPs will be available.

## Additional Options
The "Allow the private key to be exported" checkbox allows the private key to be exported from the certificate. This is useful for scenarios where the private key needs to be backed up or used on multiple devices.

The "Enable strong private key protection" checkbox enables strong private key protection, which requires the user to enter a password to access the private key. This is useful for scenarios where the private key needs to be protected from unauthorized access.
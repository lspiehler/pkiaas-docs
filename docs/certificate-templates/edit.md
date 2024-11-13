To edit the settings for a certificate template, navigate to **Certificate Templates -> Manage Templates** in the navigation pane on the left of the page. Click on a template and select "Edit Template".

## Options

### General
* **Enabled** - enables/disables the template
* **Allow unsolicited certificate web requests** - enables/disables the "Public Certificate Request" URL for the template
* **Allow the use of a valid certificate to authorize an automatic renewal request** - enables/disables certificate renewal authorization using a previously issued certificate using the renewal options found on the CA's CPS page
    * **Automatically revoke old certificate** - revoke the old certificate used to authorize renewal
    * **Require certificate to be within** - don't allow renewal using a certificate to authorize renewal unless it is within the specified number of days of expiration
    * **Copy subject and SANs from original certificate during renewal** - use the same subject and subject alternative names from the old certificate used to authorize renewal
* **Signing Algorithm** - customize the hash algorithm used to sign certificates
* **Validity Period (Days)** - specify the default length of time the issued certificate will be valid—for manually issued certificates. This option can be overridden at the time of signing when the request is in **X509 Certificates -> Pending Requests**
* **Description** - provide a description for the template

### Subject
To honor the subject attributes requested within the CSR, use the **Supplied by the CSR** option. Otherwise, the subject attributes in the CSR will be overidden by the defaults defined here.

### Key Usage
Select the key usages and extended key usages to be enabled for certificates issued using this template. Custom comma-separated extended key usage OIDs can be entered into the **Custom EKU OIDs** field.

### Basic Constraints
Basic Constraints are a critical extension in an X509 certificate, defining whether the certificate is a Certificate Authority (CA) or an end-entity (non-CA) certificate. Set the **Certificate Authority** option to yes if the template will be used to sign subordinate CAs (intermediate CAs) certificate authorities. Path length defines the maximum number of subordinate CAs that can exist below this certificate in the certificate hierarchy.

### CRL / OCSP / AIA / CPS
* **Include AIA Extension in Certificate** - The Authority Information Access (AIA) attribute is an optional but commonly included extension in an X.509 certificate. It provides information about how to access important resources or services related to the certificate issuer. Use this option to enable or disable the AIA attribute in certificates issued using this template.
    * **Custom URL** - Allows customization of the URL where the issuing CA’s certificate (or chain) can be downloaded.
* **Include OCSP Extension in Certificate** - Enable or disable the OCSP Responder attribute within the AIA extension in certificates issued using this template.
* **Include CRL Extension in Certificate** - Enable or disable the CRL Distribution Point (CDP) attribute in certificates issued using this template.
* **Include CPS Extension in Certificate** - Enable or disable the Certificate Policies attribute in certificates issued using this template. This attribute contains the URL to the Certificate Practice Statement (CPS) and the policy identifier.
    * **Policy** - Disable, select a predefined policy identifier, or enter a custom OID.

### SCEP
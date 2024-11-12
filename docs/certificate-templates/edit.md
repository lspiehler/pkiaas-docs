To edit the settings for a certificate template, navigate to **Certificate Templates -> Manage Templates** in the navigation pane on the left of the page. Click on a template and select "Edit Template".

## General
* **Enabled** - enables/disables the template
* **Allow unsolicited certificate web requests** - enables/disables the "Public Certificate Request" URL for the template
* **Allow the use of a valid certificate to authorize an automatic renewal request** - enables/disables certificate renewal authorization using a previously issued certificate using the renewal options found on the CA's CPS page
    * **Automatically revoke old certificate** - revoke the old certificate used to authorize renewal
    * **Require certificate to be within** - don't allow renewal using a certificate to authorize renewal unless it is within the specified number of days of expiration
    * **Copy subject and SANs from original certificate during renewal** - use the same subject and subject alternative names from the old certificate used to authorize renewal
* **Signing Algorithm** - customize the hash algorithm used to sign certificates
* **Validity Period (Days)** - specify the default length of time the issued certificate will be valid—for manually issued certificates. This option can be overridden at the time of signing when the request is in **X509 Certificates -> Pending Requests**
* **Description** - provide a description for the template

## Subject
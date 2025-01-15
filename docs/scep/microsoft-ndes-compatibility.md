PKIaaS.io offers Microsoft NDES compatibility to support third-party applications and processes built to work with Microsoft NDES. The feature can be enabled on a per-template basis and can be used to generate one-time challenge passwords for certificate requests from the template. The challenge passwords expire after 60 minutes.

## Enable Microsoft NDES Compatibility
To enable Microsoft NDES compatibility for a template, navigate to **Certificate Templates -> Manage Templates**, click on the template you wish to enable Microsoft NDES compatibility for, then click "Edit Template" and select the "SCEP" tab. Check the "Enable Microsoft SCEP Compatibility" checkbox and save the template.

## Microsoft NDES Compatibility URL
After enabling Microsoft NDES compatibility, the URL to access the Microsoft compatible UI can be found by navigating to **Certificate Templates -> Manage Templates**, clicking on a template, and selecting "SCEP Admin (Microsoft Compatibility)" from the menu. This URL is unique to each template and can be used to generate one-time passcodes for certificate requests from the template.

## Authentication
Access to the Microsoft NDES Compatibility URL is automatically authenticated using the same credentials used to log in to PKIaaS.io if there is an active session. In order to access the URL without an active session—this may be required by third-party applications designed to integrate with Microsoft NDES—basic authentication can be enabled by checking the "Enable Microsoft Basic Authentication" checkbox in the "SCEP" tab of the template configuration. Enter a username and password to use for basic authentication and save the template.

## Restrict Access
To restrict access to the Microsoft NDES Compatibility URL to specific IP addresses, see [SCEP Security](security.md).
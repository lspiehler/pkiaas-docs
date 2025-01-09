## Overview
Timestamping is the process of adding a trusted and verifiable time and date to a piece of digital data. This establishes proof that the data existed or was signed at a specific moment in time and has not been altered since. It ensures that signed data remains verifiable and trustworthy long after the initial signing event, even after the signing certificate has expired.

## Timestamping Service
PKIaaS.io provides a timestamping service that allows users to request a trusted timestamp for code signing, PDF document signing, etc. Both the RFC 3161 and Authenticode timestamping protocols are supported. The timestamping service URL is unique to each CA and can be found by logging into [PKIaaS.io](https://pkiaas.io/auth/login) and navigating to **Certificate Authorities -> Manage CAs**. Click on the desired CA, and select "Show CA Service URLs".

## More Information
See the links below for more information about various tools for timestamping documents and code.

* [https://www.digicert.com/kb/code-signing/digicert-certificate-utility-to-sign-code.htm](https://www.digicert.com/kb/code-signing/digicert-certificate-utility-to-sign-code.htm)
* [https://globaltrust.eu/en/adobe-acrobat-reader-dc-use-certificate-timestamp-server/](https://globaltrust.eu/en/adobe-acrobat-reader-dc-use-certificate-timestamp-server/)
* [https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool?redirectedfrom=MSDN#timestamp-command-options)
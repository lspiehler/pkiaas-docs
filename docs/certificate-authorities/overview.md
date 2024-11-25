# Certificate Authorities

## Overview
A certificate authority (CA) serves as the cornerstone of everything on PKIaaS.io. Tasks like working with templates, issuing certificates, and managing ACME policies all operate within the scope of a CA. As such, the first step upon signing into PKIaaS.io is creating a CA. Users will be automatically redirected to a setup page and prompted to create a CA before accessing other features on the site.

Users can choose between creating a managed CA or one backed by an HSM. With a managed CA, the private key is securely stored using AES-256 encryption, offering a streamlined setup without additional configuration. Alternatively, the HSM-backed option integrates with a [PKIaaS.io IoT-HSM](https://pkiaas.io/iot-hsm), enabling key management via a YubiKey 5. In this setup, all signing operations are routed to the IoT-HSM, where they are processed by the YubiKey. For detailed guidance on creating a CA with IoT-HSM, refer to the [IoT-HSM documentation](../iot-hsm/overview.md).

## Options

### Subject Attributes
When creating a certificate authority (CA), users are provided with a range of flexible options to tailor their setup. The first six fields customize the subject attributes of the CA, with only the "Certificate Authority Name" (common name) being mandatory.

### Private Key
Next, users can configure the private key settings. Various types of private key types are supported including RSA, ECC, and CRYSTALS-dilithium. Here, users can also opt to use HSM (as previously mentioned) or import an existing private key.

### Hash Algorithm, Validity, and Path Length
Further customization options include selecting the signature hash algorithm, specifying the path length, and setting the certificate authority's validity period. The signature algorithm chosen here determines how the CA's certificate is self-signed. Depending on the private key used, additional signature options may become available for signing certificates within the certificate templates after the CA is established. For more details on "Path Length," refer to RFC5280, which explains the "basic constraints" x509v3 attributes.

### Key Usage
It is not recommended to make changes to the default "Key Usage" and "Extended Key Usage" options. Making changes could result in issues with your certificate authority.

### Intermediate CA
Finally, the "CSR Only" option is designed for cases where the CA being created will function as an intermediate or subordinate certificate authority rather than a root CA. This option generates a Certificate Signing Request (CSR) that must be signed by another CA. The signing can be performed by an external CA (such as Microsoft or EJBCA) or another PKIaaS.io CA. Once the signed certificate is obtained, it must be imported before the CA can be activated and used.
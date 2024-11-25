# IoT-HSM

If you haven't yet deployed IoT-HSM, see the [installation documentation](installation.md) to get started.

## Provisioning

In order for a certificate authority on PKIaaS.io to delegate signing operations to a YubiKey managed by IoT-HSM, it must first be provisioned to do so. The first step in this process is to select the "HSM" option as the "Key Type" when creating a new certificate authority on the **Certificate Authorities -> Create new CA** page.
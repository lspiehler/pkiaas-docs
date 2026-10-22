---
title: "Certificate Authorities in the pkiaas CLI"
description: "List your certificate authorities with the pkiaas CLI, show their details, export their certificates and chains, and choose the CA to work in."
---
## Choose Your CA
Commands that work in a certificate authority use the active CA unless you tell them otherwise. When you log in, the active CA is the one you last worked in on the website, and `pkiaas login` shows it:

```text
Active CA: Example Root CA (a1B2c3D4e5)
Change it with: pkiaas ca set <NAME|ID> (pkiaas ca list shows your CAs)
```

- **List your CAs:** `pkiaas ca list` shows the CAs you own and those you were invited to, with their names and IDs. The active one is marked with `*`.
- **Change the active CA:** `pkiaas ca set "Example Issuing CA"`, with a name or ID from the list.
- **Show a CA's details:** `pkiaas ca show` shows the active CA: its key, its certificate (serial, thumbprint, validity), how many of the certificates it issued are still valid, and the URLs of its public services (certificate, chain, CRL, OCSP, time stamping, the CPS page and Windows enrollment).
- **Export a CA's certificate:** `pkiaas ca export --out ca.pem` saves the CA's certificate as PEM. Add `--chain` for the CA's certificate followed by the certificates that issued it, which is what servers and `pkiaas pkcs12 create --chain-file` need. A root CA's certificate alone is what clients add to their trust store. See [Export](certificates.md#export) for standard output and DER.

The active CA is kept on your computer, for each server, until you log out. Changing it doesn't change the CA you work in on the website, and switching CA on the website doesn't change the CLI's.

To work in another CA for one command without changing the active one, add `--ca` with its name or ID, for example `pkiaas ca show --ca "Example Issuing CA"`. In a script or CI job, set `PKIAAS_CA` instead. `--ca` comes first, then `PKIAAS_CA`, then the active CA.

Names work in any case. Two of your CAs can have the same name: a name that more than one of them has fails with `ca_ambiguous`, and the error lists their IDs, so give the ID instead. In scripts and CI jobs, use the ID: it never changes, while a CA can be renamed. `pkiaas ca set` keeps the ID too, so renaming the active CA doesn't change it.

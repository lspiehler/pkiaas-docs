---
title: "Certificates in the pkiaas CLI"
description: "Find the certificates your CA issued with the pkiaas CLI, show their details, export them with their chain or CSR as PEM or DER."
---
## Find Your Certificates
`pkiaas cert list` lists the certificates your CA issued, newest first, also expired and revoked ones:

```text
Certificates issued by Example Root CA (a1B2c3D4e5)
SERIAL                                    NAME             STATUS                   EXPIRES     TEMPLATE
25ab765c7238b3d28d2bab03271f5fa8f2fccf86  www.example.com  valid                    2027-10-18  Web Server
0d0e0f1a2b3c4d5e6f708192a3b4c5d6e7f80910  old.example.com  revoked (keyCompromise)  2027-01-05  Web Server
2 certificates
```

- **Search** by common name with `--search www.example.com`, in any case.
- **Sort** with `--sort` (name, revocationReason, template, validFrom, validTo, keyType or keySize) and `--order asc` or `desc`, e.g. `--sort validTo` for the next to expire.
- **How many:** it lists 50 by default; `--limit` shows up to 1000. When there are more, it says how many and suggests narrowing the list.

The serial names the certificate in its CA. `pkiaas cert show <SERIAL>` shows its details: its status (valid, expired, or revoked with the reason and date), template, validity, key, signature algorithm, thumbprint, and whether the CSR it was issued from is stored. Add `--text` to see every field and extension as `openssl x509 -text` shows them, such as its subject alternative names. Serials can be given with or without colons, in any case.

## Export
`pkiaas cert export <SERIAL>` exports a certificate, and `pkiaas ca export` the CA's. They work as OpenSSL does:

- **Standard output or a file:** without `--out`, the certificate goes to standard output, so you can read it or pipe it into another command. With `--out FILE`, it's saved to the file, which is never replaced unless you add `--force`.
- **PEM or DER:** `--format pem` (the default) or `--format der`, as OpenSSL's `-outform`. DER is the binary form (`.cer`) that Windows and Java also take.
- **The chain:** `--chain` adds the certificates that issued it, up to the root, which is what a server sends. It needs PEM.
- **The CSR:** `pkiaas cert export <SERIAL> --csr` exports the certificate signing request the certificate was issued from, when it's stored. A CSR sent by SCEP contains the enrollment's challenge password, so keep it as private as the password.

```sh
pkiaas cert export 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 --chain --out fullchain.pem
pkiaas cert export 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 --format der --out www.cer
pkiaas cert export 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 | openssl x509 -noout -subject -enddate
```

`pkiaas ca cert`, the name of `ca export` in the first version, still works for now.

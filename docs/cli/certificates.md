---
title: "Certificates in the pkiaas CLI"
description: "Find the certificates your CA issued with the pkiaas CLI by name, subject, SAN, serial, status or expiry, show their details, export them with their chain or CSR as PEM or DER, and revoke them or put them on hold."
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

- **Search** with `--search TEXT`. It finds the text, in any case, in the common name, in any subject value (organization, organizational unit, email address and so on) or in any subject alternative name. A serial or thumbprint in hex finds that certificate too, with or without colons or spaces between the bytes (at least 8 digits).
- **Filter** to narrow the list. A certificate is listed when every filter you give holds:
    - `--match FIELD:VALUE`: one subject attribute or SAN type has exactly this value, in any case. `*` matches any text. FIELD is a subject attribute by its OpenSSL name (`CN`, `O`, `OU`, `C`, `ST`, `L`, `emailAddress`, `serialNumber`…, or long names such as `organizationName`) or a SAN type (`DNS`, `IP`, `URI`, `email`, `RID`, `dirName`, `otherName`). Repeat it for more, up to 10.
    - `--status valid,expired,revoked`: one or more statuses.
    - `--expires-within DAYS`: expires within this many days and hasn't expired yet. Revoked certificates are included, so add `--status valid` to find the certificates to renew.
    - `--template NAME|ID`: issued with this template, enabled or not.
    - `--key-type TYPE,...`: the key algorithm as the list's `keyType` shows it, e.g. `rsaEncryption`, `id-ecPublicKey`, `ML-DSA-65`.
    - `--reason R,...`: revoked with one of these reasons, e.g. `keyCompromise`, `superseded`, `certificateHold`.
- **Sort** with `--sort` (name, revocationReason, template, validFrom, validTo, keyType or keySize) and `--order asc` or `desc`, e.g. `--sort validTo` for the next to expire.
- **How many:** it lists 50 by default; `--limit` shows up to 1000. When there are more, it says how many and suggests narrowing the list.

```sh
pkiaas cert list --match 'dns:*.example.com' --match o:Contoso
pkiaas cert list --status valid --expires-within 30 --sort validTo
pkiaas cert list --search 25:ab:76:5c:72:38:b3:d2
pkiaas cert list --status revoked --reason keyCompromise --json
```

`--match 'dns:*.example.com'` finds names under example.com and the wildcard name `*.example.com` itself; quote it so the shell doesn't expand the `*`.

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

## Revoke a Certificate
Revoke a certificate by its serial, with a reason:

```sh
pkiaas cert revoke 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 --reason keyCompromise
```

The CA's next CRL and OCSP responses list the certificate as revoked, and clients that check revocation stop accepting it. The reasons are RFC 5280's: `unspecified`, `keyCompromise` (its private key leaked or may have), `cACompromise`, `affiliationChanged`, `superseded` (replaced by a new certificate), `cessationOfOperation` (no longer used) and `certificateHold`. `pkiaas cert show <SERIAL>` shows a certificate's reason and date.

- **Confirmation:** on a terminal, `cert revoke` names the certificate and the reason and asks you to confirm. In scripts and for AI agents, where there is no terminal, add `--yes` once you're sure; without it the command fails and changes nothing.
- **Final reasons:** every reason other than `certificateHold` is final. The revocation can't be undone, and its reason can't be changed (error `revocation_final`).
- **Certificate hold:** `certificateHold` suspends a certificate for now. Take it off hold with `pkiaas cert unrevoke <SERIAL>`, and the certificate is valid again. Or make the revocation final by revoking it again with another reason. The revocation date stays the time it was put on hold.
- **Safe to repeat:** revoking a certificate again with the same reason, or unrevoking one that isn't revoked, changes nothing and succeeds.
- **Subscription:** revoking and unrevoking need a subscription, yours or the CA owner's. Without one, they fail with `subscription_required`.

```sh
pkiaas cert revoke 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 --reason certificateHold --yes
pkiaas cert unrevoke 25ab765c7238b3d28d2bab03271f5fa8f2fccf86
```

To revoke from the website instead, see [Revoke Certificates](../certificate-management/revoke-certificates.md).

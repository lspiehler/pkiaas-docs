---
title: "Certificate Authorities in the pkiaas CLI"
description: "Create certificate authorities with the pkiaas CLI, including CAs whose key is on an IoT HSM, list them, show their details, import their signed certificates, export their certificates, chains, CSRs, provisioning certificates and CPS, change their settings, delete them, and choose the CA to work in."
---
## Choose Your CA
Commands that work in a certificate authority use the active CA unless you tell them otherwise. When you log in, the active CA is the one you last worked in on the website, and `pkiaas login` shows it:

```text
Active CA: Example Root CA (a1B2c3D4e5)
Change it with: pkiaas ca set <NAME|ID> (pkiaas ca list shows your CAs)
```

- **List your CAs:** `pkiaas ca list` shows the CAs you own and those you were invited to, with their names and IDs. The active one is marked with `*`.
- **Change the active CA:** `pkiaas ca set "Example Issuing CA"`, with a name or ID from the list.
- **Show a CA's details:** `pkiaas ca show` shows the active CA: its key, its certificate (serial, thumbprint, validity), how many of the certificates it issued are still valid, the URLs of its public services (certificate, chain, CRL, OCSP, time stamping, the CPS page and Windows enrollment), and its settings.
- **Export a CA's certificate:** `pkiaas ca export --out ca.pem` saves the CA's certificate as PEM. Add `--chain` for the CA's certificate followed by the certificates that issued it, which is what servers and `pkiaas pkcs12 create --chain-file` need. A root CA's certificate alone is what clients add to their trust store. See [Export](certificates.md#export) for standard output and DER.

The active CA is kept on your computer, for each server, until you log out. Changing it doesn't change the CA you work in on the website, and switching CA on the website doesn't change the CLI's.

To work in another CA for one command without changing the active one, add `--ca` with its name or ID, for example `pkiaas ca show --ca "Example Issuing CA"`. In a script or CI job, set `PKIAAS_CA` instead. `--ca` comes first, then `PKIAAS_CA`, then the active CA.

Names work in any case. Two of your CAs can have the same name: a name that more than one of them has fails with `ca_ambiguous`, and the error lists their IDs, so give the ID instead. In scripts and CI jobs, use the ID: it never changes, while a CA can be renamed. `pkiaas ca set` keeps the ID too, so renaming the active CA doesn't change it.

## Create a CA
`pkiaas ca create --name "Example Root CA"` creates a certificate authority owned by you, as the website's [Create a Managed CA](../certificate-authorities/create.md) form does. PKIaaS.io makes the CA's key, which never leaves the platform, and self-signs its certificate. The new CA also gets its OCSP certificate and a copy of the "Web Server" template, so it can issue certificates at once. The command shows the new CA as `pkiaas ca show` does; it doesn't become the active CA unless you add `--set`.

- **What its certificate holds:** `--subject "O=Example,OU=IT,C=US"` adds the other subject fields (C, ST, L, O and OU), `--key-type` chooses the key (e.g. `ec-p384` or the post-quantum `ml-dsa-65`), `--days` sets how long it is valid (3650 by default), and `--path-length 0` lets it issue only end-entity certificates. `--key-usage` and `--extended-key-usage` add usages; a CA usually needs none.
- **A CA another CA signs:** with `--csr-only`, the CA waits for its signed certificate. Export its CSR with `pkiaas ca export --csr --out ca.csr`, have the other CA sign it, then import the signed certificate with `pkiaas ca import` (see [Import a Signed Certificate](#import-a-signed-certificate)).
- **A CA whose key is on your HSM:** with `--iot-hsm`, the key is made on your HSM by the IoT-HSM agent, not on the platform (see [Create a CA on an IoT HSM](#create-a-ca-on-an-iot-hsm)).
- **Safe to repeat:** give `--idempotency-key` with any text, e.g. a UUID. Running the same command again with the same key within 24 hours returns the CA it created instead of a second one.

You can create 20 CAs an hour. SHA-1 (`--signature-algorithm sha1`) is for testing only and asks for confirmation.

For a CA that isn't signed yet, the result says what to do next. With `--json`, `nextStep` holds the command that exports what the CA waits on: its CSR (`--csr-only`) or its provisioning certificate (`--iot-hsm`). It is null for a signed CA.

## Create a CA on an IoT HSM
`pkiaas ca create --iot-hsm` creates a CA whose private key is made and kept on your own HSM by the [IoT-HSM](../iot-hsm/overview.md) agent, as choosing "HSM" as the key type on the website's Create new CA page does. `--key-type` and `--csr-only` don't go with it.

```sh
pkiaas ca create --name "Example HSM Root CA" --subject "O=Example,C=US" --iot-hsm
```

```text
Created the CA Example HSM Root CA (a1B2c3D4e5) (IoT-HSM, waiting for the HSM's certificate)
...
Export its provisioning certificate for the IoT-HSM agent's provisioning wizard with: pkiaas ca export --provisioning-certificate --ca a1B2c3D4e5 --out provisioning.crt
```

- **What the platform makes:** only the CA's provisioning certificate: a certificate with the CA's subject and extensions, self-signed with a throwaway key. It contacts no HSM and makes no OCSP certificate, which needs the HSM. It does copy the "Web Server" template to the CA.
- **Checked first:** the platform signs test certificates with the CA's subject and extensions, never with an HSM. If they can't be signed, for example because of the `--key-usage`, `--extended-key-usage` or `--path-length` given, the CA is removed and the command fails with `ca_settings_unusable` (exit code 1). Change the settings the message names and run it again; each try counts toward the 20 CAs an hour.
- **Until it's provisioned:** the CA waits for the HSM's certificate (`signed` is false and `hsm` is true in `pkiaas ca show --json`) and can't issue certificates.

Then provision the HSM:

1. Export the provisioning certificate: run the command in the result (`nextStep` with `--json`), for example `pkiaas ca export --provisioning-certificate --ca "Example HSM Root CA" --out provisioning.crt`. `--format der` saves it as DER instead of PEM.
2. Give the file to the IoT-HSM agent's provisioning wizard, which takes it as the template for the HSM's own certificate (see [IoT-HSM Configuration](../iot-hsm/configuration.md)).
3. Import the HSM's certificate on the website ("Import Signed Certificate" on the Manage CAs page), as [IoT-HSM Configuration](../iot-hsm/configuration.md) describes. `pkiaas ca import` doesn't take it yet: for a CA whose key is on an IoT HSM it fails with `ca_on_hsm`.

The HSM's certificate is imported twice, with an agent restart between. After the first import and until the second, `--provisioning-certificate` exports the HSM's certificate instead. Once the CA is signed, it has no provisioning certificate to export and the command fails with `conflict` (exit code 5). A CA whose key is on the platform has none either (`ca_not_hsm`, exit code 5), and an IoT HSM CA has no CSR (`ca export --csr` fails with `ca_on_hsm`, exit code 5).

## Import a Signed Certificate
`pkiaas ca import` imports the certificate another CA signed for a CA made with `--csr-only`, as the website's Import Signed Certificate page does. Once it's imported, the CA is signed and can issue certificates.

```sh
pkiaas ca export --csr --ca "Example Issuing CA" --out ca.csr
# have the signing CA sign ca.csr, then:
pkiaas ca import --ca "Example Issuing CA" --cert signed.pem --chain-file chain.pem
```

```text
Imported the signed certificate of CA Example Issuing CA (a1B2c3D4e5): the CA is signed and can issue certificates.
```

- **The files:** `--cert` is the signed certificate as PEM, DER or PKCS#7, or `-` for standard input. If it holds more than one certificate, the first is the CA's and the others are its chain, so a full chain file works on its own. `--chain-file` holds the certificates that issued it, up to the root.
- **Missing issuers:** an issuer that neither file holds is fetched by the server from the address in the certificate it issued (Authority Information Access, "CA Issuers"). If it can't be fetched, the command fails with `chain_not_found` (exit code 1): give the signing CA's certificate and those above it, up to the root, with `--chain-file`.
- **Checked before anything changes:** the certificate must be a CA certificate (basicConstraints CA:TRUE) for the CA's key, valid now, and usable to sign certificates, and its chain must lead to a self-signed root. A certificate that isn't fails with `ca_certificate_refused` (exit code 1), and the message says what to change; usually the signing CA has to sign the CSR again. If the server can't run the check right now, the command fails with `ca_check_unavailable` (exit code 1): run it again in a minute.
- **What changes:** the certificate becomes the CA's, with its chain; the CA gets its OCSP certificate; the CA's name becomes the certificate's common name; and the CA's log records the import, or why the certificate was refused.
- **Safe to repeat:** running the command again with the same certificate changes nothing on a signed CA. If an import stopped after the certificate was stored (`ca_import_unfinished`, exit code 1), running it again finishes it. If another import of the same CA ran at the same time (`ca_import_conflict`, exit code 5), check the CA with `pkiaas ca show`. A signed CA's certificate is never replaced (`conflict`).
- **Who can:** importing needs the modify privilege in the CA. You can import 20 CA certificates an hour, refused ones included; beyond that the command fails with `http_429` and says when to try again.

With `--json`, the result is the CA as `pkiaas ca show --json` shows it, with `signed` true.

## Change a CA's Settings
`pkiaas ca update` changes the settings of the active CA (or the one `--ca` names), as the website's [Edit CA](../certificate-authorities/edit.md) page does. Only the settings whose flags you give change, and you need the modify privilege in the CA. `pkiaas ca show` lists the settings as they are now.

The CA's certification practice statement (CPS) is the text of its public page. To change it, export it, edit the file, and send it back:

```sh
pkiaas ca export --cps > cps.md
pkiaas ca update --cps-file cps.md
```

The CPS you send is Markdown. A CPS written in the website's old HTML editor is replaced by it, so convert it on the website first if you want to keep its formatting. The other settings:

- **The policy identifier:** `--policy-oid 1.3.6.1.4.1.99999.1` sets the certificate policy OID the CA puts, next to the address of its CPS page, in certificates from templates with policies. `--policy-oid none` removes it.
- **Windows enrollment (CEP/CES):** `pkiaas ca update --cep on --cep-username enroll --cep-password-env CEP_PASSWORD` turns it on with the user name and password Windows clients enroll with. The password comes from an environment variable or, with `--cep-password-file`, from a file, never from the command line. `--cep off` turns it off.
- **Service certificates:** `--service-key-type ec-p384 --service-signature-algorithm sha384` sets the key of the CA's OCSP and time-stamping certificates. They get it when they are next made: when they expire (yearly) or are revoked.

Add `--dry-run` to see what would change, each setting old → new, without saving anything. Running the same command again changes nothing more, and if someone changed the CA at the same time, nothing is saved and the command asks you to run it again.

## Read the logs
`pkiaas log list` lists what the platform logged for your CAs, as the website's Logs page does: SCEP, CEP/CES and ACME requests, certificate approvals, revocations and the errors they met. Use it to find out why something failed, such as a device's enrollment. It lists the latest lines of all your CAs, not only the active one, in time order: the oldest first and the newest last, just above the prompt. Each line shows the time in your computer's time zone, the level, the CA's name in brackets, the client's IP address and the message:

```
2026-10-28T21:56:53-05:00 INFO    [Example Issuing CA] 203.0.113.7 Received SCEP request for template Web Server
```

- **One CA:** `--ca "Example Issuing CA"` (any case, or its ID); repeat it for more.
- **Warnings and errors:** `--level warning` keeps warnings and the more severe lines.
- **A time range:** `--since 24h` keeps the last day; `--since` and `--until` also take a date or a time, such as `2026-10-24T08:00:00-05:00`.
- **Search:** `--search 203.0.113.7` keeps the lines with that text in the message or the IP address, such as a device's name, a serial number or an error.

When there are more lines than it lists (50 by default, `--limit` up to 1000), it says how many and how to narrow them. `TZ=UTC pkiaas log list` shows the times in UTC; `--json` always has them in UTC.

## Delete a CA
`pkiaas ca delete "Example Test CA"` deletes a CA you own, with every certificate it issued, its pending requests, templates, ACME policies and log lines. OCSP, the CRL, SCEP, ACME and Windows enrollment stop answering for it, so clients can no longer check its certificates, and the users it is shared with lose it. For a CA whose key is on your HSM, the HSM keeps the key. **It can't be undone.**

The CA must be named, by its name or ID; the command never deletes the active CA by default. It first shows what the delete takes with it, then asks you to type the CA's name: only the exact name deletes it.

- **Preview only:** `--dry-run` shows what the delete would take with it and deletes nothing.
- **In scripts:** without a terminal, add `--yes` to delete without typing the name, for example for a test CA a CI job created.

You can also delete a CA on the website: see [Delete Certificate Authorities](../certificate-authorities/delete.md).

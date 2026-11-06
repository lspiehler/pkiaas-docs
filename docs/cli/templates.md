---
title: "Certificate Templates in the pkiaas CLI"
description: "Show and change a CA's certificate templates with the pkiaas CLI, try a change on a throwaway certificate before saving it, set the SCEP passphrase, and list, show and restore a template's revisions."
---
## Overview
A template says what the certificates it issues hold: validity, signing algorithm, subject, key usages and other extensions, and whether SCEP may use it. See [Certificate Templates](../certificate-templates/overview.md) for what each setting does.

The `pkiaas template` commands work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). A template is named by its name (any case) or its ID, which `pkiaas template list` shows (see [Request Certificates](requests.md)). If two templates have that name, the command fails with `template_ambiguous`: give the ID then. Templates are made and deleted on the website (see [Create Templates](../certificate-templates/create.md)).

## Show a Template
`pkiaas template show "Web Server"` shows everything the template sets, as the website's Edit Template page has it:

```text
Template Web Server (BmOeDZAh2L) of Example Issuing CA (a1B2c3D4e5), revision 1

General
  Enabled: yes
  Public requests: yes
  Automatic renewal: on, revoke the old certificate, within 15 days of expiry
  Copy subject and SANs from the original certificate: yes
  Signing algorithm: sha256
  Validity: 365 days
Subject: from the request
Key usage (critical): digitalSignature, keyEncipherment
Extended key usage: serverAuth, clientAuth
Basic constraints (critical): not a CA
CRL / OCSP / AIA / CPS
  AIA CA issuers: on
  OCSP: on
  CRL distribution point: on
  Certificate policies: on, no template policy
  Certificates get: 2.5.29.32.0
SCEP: off
CES: changed on the website
CT logs: none
Request rules: none
Last saved 2026-11-06 23:25 UTC
```

Secrets are never shown: only whether a SCEP passphrase is set. With `--json`, you get the template as the API has it, which `pkiaas template update --file` takes back (see below).

## Change a Template
`pkiaas template update "Web Server"` changes only the settings whose flags you give:

- `--enabled on|off`: only enabled templates take requests.
- `--public-requests on|off`: anyone may request a certificate on the CA's public page; approval still applies.
- `--validity-days 90`: how many days certificates are valid.
- `--signing-algorithm sha384`: the signature hash. Depending on the CA's key type, it may be ignored.
- `--policy-oid 1.3.6.1.4.1.99999.1` adds the template's own certificate policy; `--policy-oid none` removes it.
- `--scep on|off`: SCEP enrollment with this template.

Run it with `--dry-run` first. The server checks the change and signs a throwaway certificate with it, both ways PKIaaS.io signs certificates, without touching your CA's key. It shows each setting old → new and saves nothing:

```text
$ pkiaas template update "Web Server" --validity-days 90 --dry-run
Dry run: would update template Web Server (BmOeDZAh2L) of Example Issuing CA (a1B2c3D4e5); nothing was saved.
  Validity: 365 days → 90 days
Signing trial: passed (OpenSSL and native signing)
```

Without `--dry-run`, the change is saved as a new revision:

```text
$ pkiaas template update "Web Server" --validity-days 90
Updated template Web Server (BmOeDZAh2L) of Example Issuing CA (a1B2c3D4e5): validity. Now revision 2.
```

- **Settings that can't be signed:** if the throwaway certificate can't be signed, or doesn't get what the settings ask for, the command fails with `http_400`, naming the setting, and nothing is saved.
- **Changed in between:** if someone changed the template after the command read it, nothing is saved and the command fails with `template_changed` (exit code 5). Run it again: it reads the template again and applies only its own flags.
- **Several settings at once:** save `pkiaas template show "Web Server" --json > web-server.json`, edit the file, and send it back with `pkiaas template update "Web Server" --file web-server.json`. `--file -` reads it from standard input. The file's read-only fields (such as `id`, `revision` and `scep.staticPassphraseSet`) are ignored. If the template changed since the file was written, the command fails with `template_changed`: write the file again and redo the edit.
- **Safe to repeat:** running the same command again changes nothing more.

Key usages, the subject, Intune, Microsoft basic authentication and CES are changed on the website (see [Edit Templates](../certificate-templates/edit.md)), or with `--file`.

## The SCEP Passphrase
The [static challenge passphrase](../scep/static-passphrase.md) is a secret, so it never goes on the command line:

- `--scep-passphrase new --out scep-passphrase.txt` makes a new one (24 letters and digits) and writes it to the file, readable only by you. `--force` replaces the file if it exists. Without `--out`, it is shown only in a terminal, never sent into a pipe or a `--json` result.
- `--scep-passphrase-env NAME` takes your own from the environment variable NAME, and `--scep-passphrase-file FILE` from a file.
- `--scep-passphrase none` removes it.

Your own passphrase has 16 to 128 printable characters; some older SCEP devices accept only letters and digits. The passphrase is set after the settings are saved and adds no revision.

## Revisions
Every change of a template's settings is saved as a revision, whether it was made on the website, with the CLI or with the API. Certificates name the revision that issued them. Secrets (the SCEP passphrase, Intune, Microsoft basic authentication) add no revisions.

`pkiaas template revision list "Web Server"` lists them, newest first, with who saved each and what changed:

```text
Revisions of template Web Server (BmOeDZAh2L) of Example Issuing CA (a1B2c3D4e5)
REVISION  SAVED (UTC)       BY                 CHANGED
2         2026-11-06 23:25  admin@example.com  validity
1         2026-11-06 23:25  -                  as created
2 revisions
```

History starts with the settings as they were when PKIaaS.io began keeping it. It lists 50 revisions by default; `--limit` shows up to 1000.

`pkiaas template revision show "Web Server" 1` shows the settings of revision 1, as `pkiaas template show` does.

`pkiaas template revision restore "Web Server" 1` saves the settings of revision 1 as a new revision, marked as restored from 1; history is never rewritten. Run it with `--dry-run` first to see what would change:

```text
$ pkiaas template revision restore "Web Server" 1 --dry-run
Dry run: would restore revision 1 of template Web Server (BmOeDZAh2L) of Example Issuing CA (a1B2c3D4e5) as revision 3; nothing was saved.
  Validity: 90 days → 365 days
Stays as it is: the SCEP passphrase, Intune, Microsoft basic auth and CES.
Signing trial: passed (OpenSSL and native signing)
```

- **Signed first:** the restored settings are tried on a throwaway certificate, as `pkiaas template update` does. A revision that can't be signed today (for example because the CA's policy changed since) is refused with `http_400`, and nothing is saved.
- **Changed in between:** if someone changed the template after the command read it, nothing is saved and the command fails with `template_changed`: run it again.
- **Wrong number:** a revision the template doesn't have fails with `revision_not_found` (exit code 4). `pkiaas template revision list` shows the numbers.
- **Permissions:** restoring needs the modify privilege in the template's CA.

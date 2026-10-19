---
title: "pkiaas Command-Line Tool"
description: "Install the pkiaas CLI on Linux, macOS or Windows, log in, find and export your certificates, and create keys, CSRs and PKCS#12 files on your own computer. Built for AI agents as well as people."
---
## Overview
`pkiaas` is the PKIaaS.io command-line tool. It runs on Linux, macOS and Windows, and is built to be used by AI agents (Claude Code, Codex, Copilot and others) as well as by people. Today it can:

- create private keys of every type PKIaaS.io supports, including the post-quantum [ML-DSA](../post-quantum-cryptography/ml-dsa.md) and [SLH-DSA](../post-quantum-cryptography/slh-dsa.md) types;
- create certificate signing requests (CSRs) to have signed by your certificate authority;
- combine a key, its certificate and the CA chain into a PKCS#12 (.pfx/.p12) file;
- log in to your PKIaaS.io account;
- list your certificate authorities, show their details, export their certificates and chains, and choose the one to work in;
- list the certificates a CA issued, show their details and status, and export them, with their chain or the CSR they were issued from, as PEM or DER.

Keys, CSRs and PKCS#12 files are made on your computer, and private keys never leave it. Commands for requesting, signing and revoking certificates and for managing your certificate authorities are coming.

## Install
On Linux and macOS:

```sh
curl -fsSL https://pkiaas.io/cli/install.sh | sh
```

On Windows, in PowerShell:

```powershell
irm https://pkiaas.io/cli/install.ps1 | iex
```

The script downloads the binary for your system, checks its SHA-256 checksum and installs it for your user only. It never uses sudo. On Linux and macOS it goes in `~/.local/bin` (`/usr/local/bin` when run as root), and on Windows in `%LOCALAPPDATA%\Programs\pkiaas`, which is added to your PATH. Set `PKIAAS_INSTALL_DIR` to choose another folder. Run the same command again to update; `pkiaas` tells you when a newer version is available.

Check the installation with:

```sh
pkiaas version
```

## Log In
Creating keys, CSRs and PKCS#12 files doesn't need a login. Commands that work with your account do:

```sh
pkiaas login
```

Your browser opens. Sign in to PKIaaS.io if you aren't already, check the details on the page and click **Allow**. The CLI then shows your active certificate authority (see [Choose Your CA](#choose-your-ca)). The CLI's login is kept in your system's keyring, or where there is none, in a file only you can read. It lasts 30 days from its last use and 90 days at most. PKIaaS.io emails you about each new login.

- **No browser on this computer** (over SSH or in a container): run `pkiaas login --device`. It shows an address and a code to enter in a browser on any other device. Only enter a code that comes from a `pkiaas` command you ran yourself.
- **Check your login:** `pkiaas whoami`.
- **Log out:** `pkiaas logout`. `pkiaas logout --all` signs out every CLI login of your account, on every computer. Use it if a login may have leaked. You can also see and revoke CLI logins on the website.
- **CI and scripts:** set `PKIAAS_TOKEN` from your CI system's secret store instead of logging in.

## Choose Your CA
Commands that work in a certificate authority use the active CA unless you tell them otherwise. When you log in, the active CA is the one you last worked in on the website, and `pkiaas login` shows it:

```text
Active CA: Example Root CA (a1B2c3D4e5)
Change it with: pkiaas ca set <ID> (pkiaas ca list shows your CAs)
```

- **List your CAs:** `pkiaas ca list` shows the CAs you own and those you were invited to, with their IDs. The active one is marked with `*`.
- **Change the active CA:** `pkiaas ca set <ID>`, with an ID from the list.
- **Show a CA's details:** `pkiaas ca show` shows the active CA: its key, its certificate (serial, thumbprint, validity), how many of the certificates it issued are still valid, and the URLs of its public services (certificate, chain, CRL, OCSP, time stamping, the CPS page and Windows enrollment).
- **Export a CA's certificate:** `pkiaas ca export --out ca.pem` saves the CA's certificate as PEM. Add `--chain` for the CA's certificate followed by the certificates that issued it, which is what servers and `pkiaas pkcs12 create --chain` need. A root CA's certificate alone is what clients add to their trust store. See [Export](#export) for standard output and DER.

The active CA is kept on your computer, for each server, until you log out. Changing it doesn't change the CA you work in on the website, and switching CA on the website doesn't change the CLI's.

To work in another CA for one command without changing the active one, add `--ca <ID>`, for example `pkiaas ca show --ca a1B2c3D4e5`. In a script or CI job, set `PKIAAS_CA=<ID>` instead. `--ca` comes first, then `PKIAAS_CA`, then the active CA.

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

## Create a Key, a CSR and a PKCS#12 File
Create a key. You're asked for a passphrase to encrypt it with:

```sh
pkiaas key create --type ec-p256 --out server.key
```

`pkiaas key types` lists the key types. The default is RSA 2048, which every client accepts.

Create a CSR for the key. The common name is also added as a DNS subject alternative name unless you give `--san`:

```sh
pkiaas csr create --key server.key --cn www.example.com --san www.example.com --san example.com --out server.csr
```

Sign the CSR with your certificate authority, as in [Sign a CSR from the Admin UI](../certificate-issuance-workflows/sign-a-csr-from-the-admin-ui.md). Then find the signed certificate's serial and export it, with your CA's chain:

```sh
pkiaas cert list --search www.example.com
pkiaas cert export <SERIAL> --out server.pem
pkiaas ca export --chain --out ca.pem
```

Then combine them with the key for Windows, Java or a load balancer:

```sh
pkiaas pkcs12 create --key server.key --cert server.pem --chain ca.pem --out server.pfx
```

The file is protected with AES-256, which Windows 10 1709 and later, macOS, Java 12 and later and OpenSSL 1.1.1 and later read. Add `--legacy` for older systems.

Passphrases are never given on the command line. Without a terminal to prompt on (in scripts, for example), give them with `--passphrase-env NAME` (an environment variable) or `--passphrase-file PATH` (the first line of a file, or `-` for standard input). Files are never overwritten unless you add `--force`.

## Use with AI Agents
Ask your agent to run `pkiaas help agents` first. It explains how to run `pkiaas` without prompts, how to keep passphrases and tokens out of the agent's transcript, how to get you to approve the login, and what to do about each error. The same guide is on the [AI agent](agents.md) page.

Every command accepts `--json`: it then prints its result, or an error with a stable code and a hint, as JSON. `pkiaas help --json` describes every command, flag and result field as JSON, so agents can look commands up rather than guess.

Logging in always needs you, because you approve it in your browser. When your agent asks, run `pkiaas login` yourself; in Claude Code you can type `! pkiaas login`.

## Reference
The [command reference](reference.md) lists every command, flag and JSON result field. `pkiaas <command> --help` shows the same help in your terminal.

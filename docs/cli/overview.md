---
title: "pkiaas Command-Line Tool"
description: "Install the pkiaas CLI on Linux, macOS or Windows, log in, and create keys, CSRs and PKCS#12 files on your own computer. Built for AI agents as well as people."
---
## Overview
`pkiaas` is the PKIaaS.io command-line tool. It runs on Linux, macOS and Windows, and is built to be used by AI agents (Claude Code, Codex, Copilot and others) as well as by people. Today it can:

- create private keys of every type PKIaaS.io supports, including the post-quantum [ML-DSA](../post-quantum-cryptography/ml-dsa.md) and [SLH-DSA](../post-quantum-cryptography/slh-dsa.md) types;
- create certificate signing requests (CSRs) to have signed by your certificate authority;
- combine a key, its certificate and the CA chain into a PKCS#12 (.pfx/.p12) file;
- log in to your PKIaaS.io account.

Keys, CSRs and PKCS#12 files are made on your computer, and private keys never leave it. Commands for managing your certificate authorities and certificates are coming.

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

Your browser opens. Sign in to PKIaaS.io if you aren't already, check the details on the page and click **Allow**. The CLI's login is kept in your system's keyring, or where there is none, in a file only you can read. It lasts 30 days from its last use and 90 days at most. PKIaaS.io emails you about each new login.

- **No browser on this computer** (over SSH or in a container): run `pkiaas login --device`. It shows an address and a code to enter in a browser on any other device. Only enter a code that comes from a `pkiaas` command you ran yourself.
- **Check your login:** `pkiaas whoami`.
- **Log out:** `pkiaas logout`. `pkiaas logout --all` signs out every CLI login of your account, on every computer. Use it if a login may have leaked. You can also see and revoke CLI logins on the website.
- **CI and scripts:** set `PKIAAS_TOKEN` from your CI system's secret store instead of logging in.

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

Sign the CSR with your certificate authority, as in [Sign a CSR from the Admin UI](../certificate-issuance-workflows/sign-a-csr-from-the-admin-ui.md), and save the signed certificate in PEM form as `server.pem`. Save your CA's certificate as `ca.pem` too (**Certificate Authorities -> Manage CAs**, then **Download certificate**). The chain must be PEM for now. Then combine them with the key for Windows, Java or a load balancer:

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

---
title: "Keys, CSRs and PKCS#12 Files in the pkiaas CLI"
description: "Create private keys, certificate signing requests and PKCS#12 files on your own computer with the pkiaas CLI, from files or standard input and output."
---
## Runs on Your Computer
`pkiaas key`, `pkiaas csr` and `pkiaas pkcs12` run only on your computer and never contact PKIaaS.io, so your keys and passphrases stay with you. They're a convenience: OpenSSL or any other tool works just as well.

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
pkiaas pkcs12 create --key server.key --cert server.pem --chain-file ca.pem --out server.pfx
```

The file is protected with AES-256, which Windows 10 1709 and later, macOS, Java 12 and later and OpenSSL 1.1.1 and later read. Add `--legacy` for older systems. `--cert` may also hold the whole chain, such as a file from `pkiaas cert export --chain`: the certificate that matches the key is used, and the others are added as its chain. `--chain`, the name of `--chain-file` in the first versions, still works for now.

Passphrases are never given on the command line. Without a terminal to prompt on (in scripts, for example), give them with `--passphrase-env NAME` (an environment variable) or `--passphrase-file PATH` (the first line of a file, or `-` for standard input). Files are never overwritten unless you add `--force`.

### Standard Input and Output
Like [Export](certificates.md#export), these commands work as OpenSSL does:

- **Standard output or a file:** without `--out`, or with `--out -`, `key create`, `csr create` and `pkcs12 create` write to standard output. There is no result then, so `--json` needs `--out FILE`. Keys and PKCS#12 files are secrets: prefer `--out` for them, because output on screen can end up in logs and transcripts.
- **PEM or DER:** `key create` and `csr create` take `--format pem` (the default) or `--format der`, as OpenSSL's `-outform`. A PKCS#12 file is always DER.
- **Standard input:** `--key`, `--cert` and `--chain-file` can be `-` to read standard input. PEM or DER is recognized from the content, and `--cert` and `--chain-file` also read PKCS#7 (.p7b). Only one input or passphrase per command can come from standard input. Passphrases can't be prompted for then, so give them with `--passphrase-env`, `--key-passphrase-env` or a passphrase file.

```sh
pkiaas csr create --key server.key --cn www.example.com | openssl req -noout -text
pkiaas cert export <SERIAL> --chain | pkiaas pkcs12 create --cert - --key server.key --key-passphrase-env KEY_PASSPHRASE --passphrase-env PFX_PASSPHRASE --out server.pfx
```

**Windows PowerShell 5.1:** `>` and `|` re-encode output as UTF-16, which breaks keys, certificates and PKCS#12 files. Always use `--out FILE` there, and give file names rather than `-`. PowerShell 7.4 and later keep the bytes. A file re-encoded this way fails with a message saying so.

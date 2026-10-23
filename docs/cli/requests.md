---
title: "Request Certificates with the pkiaas CLI"
description: "Request a certificate from your CA with the pkiaas CLI: list the CA's templates, send a CSR, have the certificate issued and saved in the same command, and repeat a request safely with an idempotency key."
---
## Find a Template
A template says what the certificates it issues hold, such as their validity and key usages. `pkiaas template list` lists the templates of your CA by name, enabled or not:

```text
Templates of Example Root CA (a1B2c3D4e5)
ID          NAME        ENABLED
tmploff001  Retired     no
tmplweb001  Web Server  yes
2 templates
```

Commands take a template by its name, in any case, or by its ID. Only enabled templates take requests. Templates are made and changed on the website (see [Create Templates](../certificate-templates/create.md)). It lists 50 templates by default; `--limit` shows up to 1000.

## Request a Certificate
`pkiaas request create` sends a certificate signing request (CSR) to your CA with one of its templates, as **Submit CSR** on the website does:

```sh
pkiaas request create --csr www.csr --template "Web Server"
```

```text
Requested a certificate for www.example.com from Example Root CA (a1B2c3D4e5) with the template Web Server (request Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a).
It waits for a member of the CA to approve it: pkiaas request approve Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a
```

- **The CSR:** `--csr` is a PEM or DER file, for example from [`pkiaas csr create`](keys-csrs-pkcs12.md), or `-` to read standard input. Only the CSR is sent, never anything else in the file. The server checks its signature: a CSR that can't be read, or was changed after it was signed, fails with `invalid_csr`.
- **The template:** `--template` takes the name or ID of one of the CA's enabled templates from `pkiaas template list`. A wrong or disabled one fails with `template_not_found`, and a name that two enabled templates share fails with `template_ambiguous`: give the ID then.
- **The CA:** the active CA, or another one with `--ca` (see [Choose Your CA](certificate-authorities.md#choose-your-ca)).
- **Approval:** the request waits until a member of the CA approves it with [`pkiaas request approve`](pending-requests.md#approve) or on the website's [Pending Requests](../certificate-management/pending-requests.md) page, which issues the certificate. No email is sent. Then `pkiaas request show <ID>` shows the certificate's serial, and `pkiaas cert export <SERIAL>` [exports it](certificates.md#export).

```sh
pkiaas csr create --key server.key --cn www.example.com | pkiaas request create --csr - --template "Web Server"
```

## Get the Certificate Now
When you approve requests to your CA yourself, add `--approve` to approve the request in the same command, and `--out` to save the issued certificate too:

```sh
pkiaas request create --csr www.csr --template "Web Server" --approve --chain --out fullchain.pem
```

```text
Requested and issued a certificate for www.example.com from Example Root CA (a1B2c3D4e5) with the template Web Server (request Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a): serial 25ab765c7238b3d28d2bab03271f5fa8f2fccf86
Saved the certificate with its chain (2 certificates) to fullchain.pem
```

- **The certificate file:** `--out FILE` saves it as PEM, or DER with `--format der`. `--chain` adds the certificates that issued it, up to the root, which is what a server sends. The file is never replaced unless you add `--force`, and it's checked before anything is requested.
- **Standard output:** `--out -` writes only the certificate to standard output, for piping into another command.
- **If approving fails:** the request stays, waiting for approval, and the error gives its ID. Fix the cause and approve it with `pkiaas request approve <ID>` (see [Approve Requests](pending-requests.md#approve)).

The certificate is issued as the template says, as **Sign** on the website does without changes. To change its subject, subject alternative names or validity, add `--subject`, `--san`, `--not-before` or `--not-after`, as for [`request approve`](pending-requests.md#change-the-certificate-when-approving).

## Repeat a Request Safely
Each run of `request create` makes a new request. To make it safe to run again, for example when a script or an AI agent can't tell whether it worked because the connection dropped, give it an idempotency key: any text, such as a UUID, that you keep with the request.

```sh
pkiaas request create --csr www.csr --template "Web Server" --idempotency-key 8e03978e-40d5-43e8-bc93-6894a57f9324
```

- **Same key, same request:** run again within 24 hours with the same key, CSR, template and CA, it returns the first result rather than making a second request. After 24 hours the key is forgotten, and the command makes a new request.
- **Without `--idempotency-key`:** the CLI makes a key itself and uses it when it retries a failed connection on its own. With `--json`, it reports the key as `idempotencyKey`.
- **A key for one request only:** a key used for a different request in the last 24 hours fails with `idempotency_key_reused`. Make a new key for each new request.
- **With `--approve`:** running the same command again with the same key approves the same request, which is safe: an issued request stays as it is.
- **Still running:** while the first request with a key hasn't finished, the same key fails with `idempotency_key_in_use`. Wait a minute and run the same command with the same key again.

To request a certificate from the website instead, see [Sign a CSR from the Admin UI](../certificate-issuance-workflows/sign-a-csr-from-the-admin-ui.md).

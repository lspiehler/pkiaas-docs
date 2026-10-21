---
title: "Request Certificates with the pkiaas CLI"
description: "Request a certificate from your CA with the pkiaas CLI: list the CA's templates, send a CSR, and repeat a request safely with an idempotency key. The request waits for approval on the Pending Requests page."
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

Only enabled templates take requests. Templates are made and changed on the website (see [Create Templates](../certificate-templates/create.md)). It lists 50 templates by default; `--limit` shows up to 1000.

## Request a Certificate
`pkiaas request create` sends a certificate signing request (CSR) to your CA with one of its templates, as **Submit CSR** on the website does:

```sh
pkiaas request create --csr www.csr --template tmplweb001
```

```text
Requested a certificate for www.example.com from Example Root CA (a1B2c3D4e5) with the template Web Server (request Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a).
It waits for a member of the CA to approve it on the website's Pending Requests page.
```

- **The CSR:** `--csr` is a PEM or DER file, for example from [`pkiaas csr create`](keys-csrs-pkcs12.md), or `-` to read standard input. Only the CSR is sent, never anything else in the file. The server checks its signature: a CSR that can't be read, or was changed after it was signed, fails with `invalid_csr`.
- **The template:** `--template` takes the ID of one of the CA's enabled templates from `pkiaas template list`. A wrong or disabled one fails with `template_not_found`.
- **The CA:** the active CA, or another one with `--ca` (see [Choose Your CA](certificate-authorities.md#choose-your-ca)).
- **Approval:** the request waits on the CA's [Pending Requests](../certificate-management/pending-requests.md) page until a member of the CA approves it, which issues the certificate. No email is sent. Then `pkiaas cert list --search www.example.com` shows the certificate and its serial, and `pkiaas cert export <SERIAL>` [exports it](certificates.md#export).

```sh
pkiaas csr create --key server.key --cn www.example.com | pkiaas request create --csr - --template tmplweb001
```

## Repeat a Request Safely
Each run of `request create` makes a new request. To make it safe to run again, for example when a script or an AI agent can't tell whether it worked because the connection dropped, give it an idempotency key: any text, such as a UUID, that you keep with the request.

```sh
pkiaas request create --csr www.csr --template tmplweb001 --idempotency-key 8e03978e-40d5-43e8-bc93-6894a57f9324
```

- **Same key, same request:** run again within 24 hours with the same key, CSR, template and CA, it returns the first result rather than making a second request. After 24 hours the key is forgotten, and the command makes a new request.
- **Without `--idempotency-key`:** the CLI makes a key itself and uses it when it retries a failed connection on its own. With `--json`, it reports the key as `idempotencyKey`.
- **A key for one request only:** a key used for a different request in the last 24 hours fails with `idempotency_key_reused`. Make a new key for each new request.
- **Still running:** while the first request with a key hasn't finished, the same key fails with `idempotency_key_in_use`. Wait a minute and run the same command with the same key again.

To request a certificate from the website instead, see [Sign a CSR from the Admin UI](../certificate-issuance-workflows/sign-a-csr-from-the-admin-ui.md).

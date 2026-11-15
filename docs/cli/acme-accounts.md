---
title: "ACME Accounts in the pkiaas CLI"
description: "List and show a CA's ACME accounts, see which client each one is and when it was last used, and revoke an account so its client can't get certificates, with the pkiaas CLI."
---
## Overview
An ACME account is an ACME client (certbot, win-acme, Certify The Web, Traefik, ...) registered under an [ACME policy](acme-policies.md) with its own key, which signs its requests. Clients register with an [EAB](acme-eabs.md) or, before EABs, a [provisioning URL](acme-provisioning-urls.md).

The `pkiaas acme account` commands list a CA's ACME accounts, show one, and revoke one. They work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). An account is named by its ID: the number at the end of its account URL, which `certbot show_account` also prints. It isn't a certificate serial.

The last use, the client and the EAB or provisioning URL an account registered with are recorded since 2026-10-27. Accounts not used since then show `-` or "not recorded" there.

## List Accounts
```text
$ pkiaas acme account list
ACME accounts of Example Issuing CA (a1B2c3D4e5)
ID    STATUS       POLICY             CONTACT              CLIENT                   LAST USED             ORDERS  CERTS
1204  valid        Web servers (205)  ops@example.com      CertbotACMEClient/5.8.0  2026-11-05T14:14:03Z  14      12
1150  revoked      Web servers (205)  old-web@example.com  win-acme/2.2.9.1701      2026-10-29T09:30:12Z  0       2
 412  valid        Web servers (205)  noc@example.com      -                        -                     0       41
 377  deactivated  Intranet (206)     -                    -                        -                     0       0
4 accounts; "-" under CLIENT and LAST USED: not recorded (accounts used only before 2026-10-27)
```

The most recently used accounts come first, and never-used ones last.

- **Status:** `valid` accounts can order certificates. `deactivated` means its client ended it, and `revoked` means a CA member revoked it. Neither can be undone.
- **Client:** the User-Agent of its last request, as the client sent it.
- **Orders and certs:** how many orders the account made, and how many of them got a certificate. Orders that got no certificate are deleted some time after they expire.
- **Filters:** `--policy "Web servers"` keeps one policy's accounts, and `--status valid,deactivated,revoked` those with one of the statuses. `--search certbot` keeps those whose contacts, client or initial IP address contain the text, in any case. An ID matches that account.
- **Sorting:** `--sort` takes `id`, `contact`, `policy`, `status`, `client`, `createdAt`, `lastUsedAt`, `orderCount` or `certificateCount`, with `--order asc` (the default with `--sort`) or `desc`.
- **Limit:** it lists the first 50 accounts. `--limit` raises that to at most 1000.

## Show an Account
```text
$ pkiaas acme account show 1204
ACME account 1204 of Example Issuing CA (a1B2c3D4e5)
  URL:              https://acme-v02-api.pkiaas.io/acme/acct/1204
  Status:           valid
  ACME policy:      Web servers (205)
  Contacts:         ops@example.com
  Created:          2026-10-28T14:02:11Z
  Last used:        2026-11-05T14:14:03Z
  Client:           CertbotACMEClient/5.8.0 (certbot; Ubuntu 24.04) Authenticator/dns-cloudflare
  Initial IP:       203.0.113.24
  Registered with:  EAB web-servers (57)
  Key:              ES256, thumbprint pX3cJ0b1u9vYbq0s8yX5ZcT2wq3Fh7Lr1nM4aKd6sQk
  Orders:           14
  Certificates:     12 (last order 2026-11-05T14:13:58Z)
```

The key's thumbprint is its RFC 7638 SHA-256 thumbprint. [List its orders](acme-orders.md) with `pkiaas acme order list --acme-account 1204`.

Contacts and the client are text the ACME client chose. The text output escapes control characters in them, and `--json` gives them as stored.

## Revoke an Account
Revoking an account stops its client from ordering or renewing certificates: the ACME server refuses every request signed with its key. **It can't be undone.**

```text
$ pkiaas acme account revoke 1204
ACME account 1204: valid, Web servers (205), ops@example.com, CertbotACMEClient/5.8.0
Revoke ACME account 1204? Its client can't order or renew certificates any more, and this can't be undone. [y/N] y
Revoked ACME account 1204
  Status:          revoked
  Inactive since:  2026-11-06T15:20:44Z
Its 12 certificates stay valid; revoke any that mustn't be used with `pkiaas cert revoke SERIAL`.
Its key can't register again, but a new key can while policy Web servers (205) has enabled EABs or provisioning URLs;
to keep the client out, disable them too: pkiaas acme eab list --policy 205 --status enabled
```

- **Certificates stay valid.** Revoke any that mustn't be used with `pkiaas cert revoke SERIAL` (see [Certificates](certificates.md)).
- **Keep the client out:** its key can't register again, but the client could register a new key while the policy has enabled EABs or provisioning URLs. Disable those too, with `pkiaas acme eab update ID --enabled off`.
- **Without a terminal,** add `--yes` to revoke without asking.
- **Safe to run again:** an account that is revoked already, or that its client deactivated, is left as it is, and the command says so and succeeds.

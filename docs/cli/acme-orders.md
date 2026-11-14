---
title: "ACME Orders in the pkiaas CLI"
description: "List a CA's ACME orders, or one ACME account's, with their status, identifiers and certificates, and find out why renewals failed, with the pkiaas CLI."
---
## Overview
An ACME order is an [ACME account](acme-accounts.md)'s request for a certificate for some identifiers, such as host names. Its client proves control of them, then finalizes the order with a CSR, and a valid order names the certificate it got.

`pkiaas acme order list` lists a CA's ACME orders, newest first. It works in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). Listing changes nothing.

## List Orders
```text
$ pkiaas acme order list --limit 4
ACME orders of Example Issuing CA (a1B2c3D4e5)
ID    STATUS   CREATED               ACCOUNT               IDENTIFIERS                   CERTIFICATE
9812  valid    2026-11-05T14:13:58Z  1204 ops@example.com  www.example.com, example.com  4f1a9c2e7b0d3365 (valid)
9801  valid    2026-11-05T08:00:31Z  1188 lab@example.com  printer7.lab.example.com      5b2e8f01c6d7a943 (valid)
9790  invalid  2026-11-04T09:02:10Z  1204 ops@example.com  api.example.com               -
9761  ready    2026-11-03T03:40:12Z  1204 ops@example.com  test.example.com              -
4 of 31 shown; narrow them with --acme-account, --policy, --status or --search, or raise --limit (at most 1000)
Why invalid:
  9790: DNS problem: NXDOMAIN looking up TXT for _acme-challenge.api.example.com
```

- **One account's orders:** `--acme-account 1204`, with the ID from `pkiaas acme account list`.
- **One policy's orders:** `--policy "Web servers"` lists the orders of the accounts now under that [ACME policy](acme-policies.md).
- **Search:** `--search example.com` keeps orders with an identifier that contains the text. A wildcard is stored without its `*.`, so `example.com` also finds `*.example.com`. An order ID matches its order.
- **Identifiers:** the text output shows an order's first two identifiers and how many more there are (`+3 more`). `--json` gives all of them.
- **Certificate:** the serial of the certificate a valid order got, and whether it's still valid. `pkiaas cert show SERIAL` shows it (see [Certificates](certificates.md)).
- **Sorting:** `--sort` takes `id`, `createdAt`, `account` or `status`, with `--order asc` (the default with `--sort`) or `desc`.
- **Limit:** it lists the first 50 orders. `--limit` raises that to at most 1000.

## Order Statuses
`--status` keeps the orders with one of these statuses, comma-separated or repeated:

| Status | Meaning |
|---|---|
| `pending` | Waiting for its client to prove control of the identifiers. |
| `ready` | Validated, waiting for its client to finalize (send its CSR). A finalize refused before signing, for example over the subscription limit, also leaves an order ready; the CA's log says why (`pkiaas log list`). |
| `processing` | Being signed. |
| `valid` | Issued: the certificate column names the certificate it got. |
| `invalid` | Failed: a challenge failed validation, or signing refused it. "Why invalid:" after the table gives the reason of each invalid order shown, when one was stored. |
| `expired` | A pending or ready order past its expiration: a renewal its client never finished. Nothing failed, unlike invalid. |

An order's expiration is the order's lifetime (7 days by default), not the certificate's. After it, the certificate is what remains. Orders without a certificate are deleted some time after they expire, so an account with no orders may have had only old abandoned ones.

## Find Out Why Renewals Failed
```sh
pkiaas acme order list --status invalid,expired
pkiaas acme order list --acme-account 1204 --status invalid,expired
```

The first lists the failed and abandoned orders of the whole CA, the second those of one client.

## Find a Client's Certificates
```text
$ pkiaas acme order list --acme-account 1204 --status valid
```

Then `pkiaas cert show SERIAL` shows each certificate.

Identifiers and error details are text the ACME client (or its DNS) chose. The text output escapes control characters in them, and `--json` gives them as stored, except that challenge tokens are replaced with `…`.

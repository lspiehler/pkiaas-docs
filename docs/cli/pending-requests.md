---
title: "Approve Requests with the pkiaas CLI"
description: "List your CA's pending certificate requests with the pkiaas CLI, check what a request asks for, approve it to issue the certificate or email an approved voucher, resend the requester's email, or decline it."
---
## List Pending Requests
`pkiaas request list` lists your CA's requests that wait for something, newest first, as the website's [Pending Requests](../certificate-management/pending-requests.md) page does:

```text
Pending requests in Example Root CA (a1B2c3D4e5)
ID                              NAME               STATUS                    TEMPLATE    REQUESTED
Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a  www.example.com    pendingApproval           Web Server  2026-10-22
Pm4Wc8Hn2Jd6Rt1Kv9Bx5Fs3Lq7Ze0  laptop-042         preApproved               Devices     2026-10-21
Gh2Yt6Ns0Vr4Kc8Mx1Dp5Qw9Bj3Lf7  alice@example.com  pendingApproval (no CSR)  User        2026-10-20
3 requests
```

The status says what each request waits for:

- **pendingApproval:** a member of the CA approves or declines it. Approving a request with a CSR issues the certificate; approving one without a CSR (`(no CSR)` in the list), such as one from the public request form, emails the requester an approved voucher (see [Requests Without a CSR](#requests-without-a-csr)).
- **pendingEmailVerification:** the requester has yet to confirm their email address.
- **preApproved:** it's issued when the requester picks it up with its voucher, SCEP challenge or Apple profile. [`pkiaas request resend`](#resend-the-email) emails the requester a new link.
- **processing:** it's being signed, which takes seconds. One that has been processing for more than 10 minutes is stuck: decline it, and the requester can make a new request.

Issued and declined requests aren't listed, nor are requests from ACME. **Search** by name with `--search example.com`, in any case, and **sort** with `--sort` (requestedAt, name or template) and `--order asc` or `desc`. It lists 50 requests by default; `--limit` shows up to 1000.

## Check a Request
`pkiaas request show <ID>` shows a request, issued and declined ones too, with what its CSR asks for:

```text
Request: www.example.com (Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a)
  CA:         Example Root CA (a1B2c3D4e5)
  Status:     pendingApproval
  Template:   Web Server (tmplweb001)
  Source:     api
  Requested:  2026-10-22T14:05:31.000Z
  Subject:    CN=www.example.com
  Alt names:  DNS:www.example.com, DNS:example.com
  Key:        rsaEncryption (2048 bits)
```

The template, not the CSR, decides what the certificate holds, such as its validity and key usages. Once the request is issued, it shows the certificate's serial.

## Approve
`pkiaas request approve <ID>` approves a request: the CA signs its CSR as the request's template says, as **Sign** on the website does without changes, and the command ends once the certificate is issued. On a CA whose key is on an [IoT HSM](../iot-hsm/overview.md), that can take a few seconds.

```text
Approved the request Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a for www.example.com: issued the certificate with serial 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 (pkiaas cert export 25ab765c7238b3d28d2bab03271f5fa8f2fccf86)
```

- **Get the certificate too:** with `--out FILE`, the command also saves the issued certificate, as [`pkiaas cert export`](certificates.md#export) does: `--chain` adds the certificates that issued it, up to the root, `--format der` saves it as DER, and the file is never replaced unless you add `--force`. `--out -` writes the certificate to standard output instead, for piping.
- **Safe to repeat:** approving a request that is issued already changes nothing, so you can run the command again, for example after a lost connection.
- **What can be approved:** only a request that waits for approval (pendingApproval). Others fail with `request_not_approvable` (email not confirmed, pre-approved for SCEP or an Apple profile, no valid email address for a voucher), `request_declined`, or `request_processing` while it's being signed (wait a few seconds and check it with `request show`). These all exit with code 5.
- **When signing fails:** if the CA can't sign the request, for example because its IoT HSM doesn't answer, the command fails with `signing_failed` and the request waits for approval again. The CA's log on the website says why.

```sh
pkiaas request approve Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a --chain --out fullchain.pem
```

### Requests Without a CSR
A request without a CSR (`hasCsr` is false in `pkiaas request show --json`), such as one from the public request form, has no key to sign yet. Approving it does what **Send Approved Voucher** does on the website: the request becomes preApproved for 24 hours, and the requester is emailed an approved voucher, with which they make the key and pick up the certificate.

```text
Approved the request Gh2Yt6Ns0Vr4Kc8Mx1Dp5Qw9Bj3Lf7 for alice@example.com: emailed the requester an approved voucher, valid until 2026-11-24T15:05:31.000Z
```

- **No certificate yet:** it's issued when the requester picks it up, so `--out` is refused, and with `--json` the result has `status` `preApproved`, no `serial`, and the voucher's `expiresAt`. The voucher is never shown.
- **Changes:** `--subject`, `--san`, `--not-before` and `--not-after` go into the voucher (see [Change the Certificate When Approving](#change-the-certificate-when-approving)).
- **Safe to repeat:** approving it again changes nothing and sends no second voucher. To send the requester a new one, [resend the email](#resend-the-email).
- **When the email fails:** if the mail server doesn't take the email, the command fails with `email_failed` (exit code 1), but the request is approved all the same. Once the mail server works, run `pkiaas request resend <ID>`.

## Change the Certificate When Approving
By default the certificate holds what the CSR asks for, as the template allows. To change that, give `request approve` the new values, as **Override requested attributes** and **Override validity time** do on the website's [Pending Requests](../certificate-management/pending-requests.md) page:

- **`--subject DN`:** the subject in place of the CSR's, in RFC 4514 form (`"CN=www.example.com,O=Example,C=US"`) or OpenSSL's (`"/C=US/O=Example/CN=www.example.com"`), as [`pkiaas csr create`](keys-csrs-pkcs12.md) takes it. The template's subject attributes still win.
- **`--san NAME`:** a subject alternative name in place of the CSR's. Repeat it for each name, and list them all: the CSR's names are replaced, not added to. Write `dns:NAME`, `ip:ADDRESS`, `email:ADDRESS` or `uri:URI`, or a bare name whose kind is guessed.
- **`--not-after TIME`:** when the certificate expires, in place of the template's validity, in RFC 3339 form such as `2027-01-31T00:00:00Z`. It's valid from now, or from `--not-before TIME`.

```sh
pkiaas request approve Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a --san www.example.com --san example.com --not-after 2027-01-31T00:00:00Z
```

```text
Approved the request Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a for www.example.com with the given subject alternative names and validity: issued the certificate with serial 25ab765c7238b3d28d2bab03271f5fa8f2fccf86 (pkiaas cert export 25ab765c7238b3d28d2bab03271f5fa8f2fccf86)
```

- **Which requests:** changes need a request that waits for approval (`pendingApproval` in `pkiaas request show`). For one without a CSR, they go into its approved voucher. Others fail with `request_not_approvable`.
- **Values OpenSSL won't take**, such as a common name longer than 64 characters, fail with `invalid_overrides`. Nothing is signed or sent, and the request still waits for approval, so fix the value and approve it again.
- **Validity needs a subscription** while the CA has a validity limit (`validityLimitDays` in `pkiaas request show --json`); without one, `--not-before` and `--not-after` fail with `subscription_required`.
- **Repeating:** approving a request that is issued already never signs it again, so changes given then aren't applied, and the command says so.

`pkiaas request create --approve` takes the same flags, to request and issue a certificate with changes in one command (see [Get the Certificate Now](requests.md#get-the-certificate-now)).

## Resend the Email
`pkiaas request resend <ID>` emails the requester of a waiting request a new link, as **Resend Email** and **Resend Email Verification** do on the website's [Pending Requests](../certificate-management/pending-requests.md) page:

- **pendingEmailVerification:** a new email verification link.
- **preApproved:** a new voucher, SCEP challenge or Apple profile link, valid for 24 more hours.

Once the email has gone out, the links in earlier emails stop working. The new link is never shown. It asks you to confirm; in scripts, add `--yes`.

```sh
pkiaas request resend Pm4Wc8Hn2Jd6Rt1Kv9Bx5Fs3Lq7Ze0 --yes
```

```text
Emailed the requester of the request Pm4Wc8Hn2Jd6Rt1Kv9Bx5Fs3Lq7Ze0 for laptop-042 a new SCEP challenge, valid until 2026-11-24T15:05:31.000Z; links in earlier emails no longer work
```

- **Nothing to resend:** a request that waits for approval, or has no valid email address, fails with `request_not_resendable`; approve it instead. An issued, declined or processing request fails with `request_issued`, `request_declined` or `request_processing`. These all exit with code 5.
- **When the email fails:** the command fails with `email_failed` (exit code 1), and nothing changes: the earlier links still work.
- **Limit:** a request can be resent 10 times an hour; beyond that the command fails with `http_429` and says when to try again.
- **Safe to repeat:** each run sends an email, unless you give the `--idempotency-key` of an earlier run (any text, such as a UUID): within 24 hours, that returns the earlier result and sends no second email. Without it, the CLI makes a key and reports it as `idempotencyKey` with `--json`.

With `--json`, the result has the request's `id`, `status` (`pendingEmailVerification` or `preApproved`, as before), `name`, `expiresAt` (when the new link expires) and `idempotencyKey`.

## Decline
`pkiaas request decline <ID>` declines a request for good: it will never be issued, and its voucher, email confirmation link and SCEP challenge stop working. It asks you to confirm; in scripts, add `--yes`.

```text
Decline the request Gh2Yt6Ns0Vr4Kc8Mx1Dp5Qw9Bj3Lf7 for alice@example.com? This can't be undone. [y/N]
```

Declining can't be undone, but the requester can make a new request. Declining a request that is declined already changes nothing. An issued request can't be declined (`request_issued`): [revoke its certificate](certificates.md#revoke-a-certificate) instead.

Requests are approved, resent and declined in the active CA, or in another one with `--ca` (see [Choose Your CA](certificate-authorities.md#choose-your-ca)).

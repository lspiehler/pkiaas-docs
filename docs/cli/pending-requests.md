---
title: "Approve Requests with the pkiaas CLI"
description: "List your CA's pending certificate requests with the pkiaas CLI, check what a request asks for, approve it to issue the certificate, or decline it."
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

- **pendingApproval:** a member of the CA approves or declines it. A request without a CSR, such as one from the public request form, needs an approved voucher, which only the website sends.
- **pendingEmailVerification:** the requester has yet to confirm their email address.
- **preApproved:** it's issued when the requester picks it up with its voucher or SCEP challenge.
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
- **What can be approved:** only a request that waits for approval and has a CSR. Others fail with `request_not_approvable` (no CSR, email not confirmed, pre-approved), `request_declined`, or `request_processing` while it's being signed (wait a few seconds and check it with `request show`).
- **When signing fails:** if the CA can't sign the request, for example because its IoT HSM doesn't answer, the command fails with `signing_failed` and the request waits for approval again. The CA's log on the website says why.

```sh
pkiaas request approve Xq7Ld2Rk9TfP3wVb8NcJ5mHs1GyZ4a --chain --out fullchain.pem
```

To change the subject, subject alternative names or validity before signing, approve the request on the website's [Pending Requests](../certificate-management/pending-requests.md) page.

## Decline
`pkiaas request decline <ID>` declines a request for good: it will never be issued, and its voucher, email confirmation link and SCEP challenge stop working. It asks you to confirm; in scripts, add `--yes`.

```text
Decline the request Gh2Yt6Ns0Vr4Kc8Mx1Dp5Qw9Bj3Lf7 for alice@example.com? This can't be undone. [y/N]
```

Declining can't be undone, but the requester can make a new request. Declining a request that is declined already changes nothing. An issued request can't be declined (`request_issued`): [revoke its certificate](certificates.md#revoke-a-certificate) instead.

Requests are approved and declined in the active CA, or in another one with `--ca` (see [Choose Your CA](certificate-authorities.md#choose-your-ca)).

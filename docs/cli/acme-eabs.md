---
title: "ACME EABs in the pkiaas CLI"
description: "Create, list, show, change, disable and delete ACME external account bindings (EABs) with the pkiaas CLI, and register certbot with an EAB's HMAC key file."
---
## Overview
An ACME client such as certbot registers an account under an [ACME policy](acme-policies.md) with an external account binding (EAB): a key ID and an HMAC key made for that policy. The account then gets certificates as the policy says. See [Generate EAB Credentials](../acme/generate-eab-credentials.md) for doing the same on the website.

The `pkiaas acme eab` commands work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). An EAB is named by its numeric ID, which `pkiaas acme eab list` shows. A policy is named by its name (any case) or ID.

## Create an EAB
```sh
pkiaas acme eab create --policy "Web servers" --name web01 --out web01.eab
```

- **Name:** 1 to 50 letters, digits, spaces, hyphens and underscores.
- **Uses:** `--uses` is how many ACME accounts it may register, 0 to 65535 (default 10). Each registration takes one.
- **Expiration:** `--expires` is when it stops registering accounts: a time such as `2026-12-31T23:59:59Z`, a date (midnight in your computer's time zone), or how long from now (`24h`, `30d`). Without it, 7 days from now.

The command prints the EAB's key ID and the ACME directory URL, and a certbot command ready to use them:

```text
Created EAB web01 (12) in Example Issuing CA (a1B2c3D4e5)
  Key ID:            oX9R0AHUEJuWaW194umR9X
  ACME policy:       Web servers (205)
  Status:            enabled
  Enabled:           on
  Uses remaining:    10
  Expires:           2026-11-13T15:00:00Z
  Accounts created:  0
  Directory URL:     https://acme-v02-api.pkiaas.io/directory
  HMAC key:          saved to web01.eab (only you can read it); the server won't show it again, so keep this file
Register an ACME client with it, e.g.:
  certbot register --server https://acme-v02-api.pkiaas.io/directory --eab-kid oX9R0AHUEJuWaW194umR9X --eab-hmac-key "$(cat 'web01.eab')" --email EMAIL --agree-tos
```

**The HMAC key is shown only once.** The server never shows it again, so keep the file. `--out` writes the key alone on one line, readable by you only, and an existing file is replaced only with `--force`.

- **Without `--out`:** at a terminal, the key is shown on screen and not saved. In a pipe, in captured output or with `--json`, the command refuses with `secret_destination` (exit code 2) before it creates anything, so a key never ends up in a log or transcript by accident. `--out -` sends the key to standard output anyway, to pipe it to another command.
- **Safe to repeat:** give `--idempotency-key` with any text, e.g. a UUID. Running the same command again with the same key within 24 hours creates no second EAB, but it can't show the key again either, so it fails with `secret_shown` (exit code 5) and writes nothing. Disable that EAB (`pkiaas acme eab update ID --enabled off`) and create a new one.

Anyone with the key ID and the HMAC key can register accounts under the policy until the EAB is used up, expires or is disabled, and get certificates for the policy's pre-approved domains.

## Register an ACME Client
Give the key to the ACME client from the file, so it never appears on screen:

```sh
certbot register --server https://acme-v02-api.pkiaas.io/directory --eab-kid oX9R0AHUEJuWaW194umR9X --eab-hmac-key "$(cat web01.eab)" --email admin@example.com --agree-tos
```

Then request certificates as usual, e.g. `certbot certonly --server https://acme-v02-api.pkiaas.io/directory -d www.example.com`. See [Register an ACME Account](../acme/register-acme-account.md) for other ACME clients.

If the HMAC key is wrong, certbot says "The external account binding MAC is not valid".

## List and Show EABs
```text
$ pkiaas acme eab list
EABs of Example Issuing CA (a1B2c3D4e5)
ID  NAME   KEY ID                  POLICY             STATUS   USES  EXPIRES               ACCOUNTS
12  web01  oX9R0AHUEJuWaW194umR9X  Web servers (205)  enabled  9     2026-11-13T15:00:00Z  1
1 EAB
```

- **Status:** `enabled` means it can register an account now. Otherwise it shows the first of `disabled`, `expired` and `used` (no uses left) that applies.
- **Accounts:** the ACME accounts registered with it since 2026-10-27; earlier ones aren't counted.
- **Filters:** `--policy "Web servers"` keeps one policy's EABs, `--status enabled,disabled,expired,used` those with one of the statuses, and `--search web` those whose name contains the text.
- **Sort:** `--sort expiresAt --order desc` sorts by name, keyId, policy, enabled, usesRemaining or expiresAt.

`pkiaas acme eab show 12` shows one EAB. Neither command ever shows the HMAC key.

## Change, Disable or Delete an EAB
`pkiaas acme eab update 12` changes only the settings whose flags you give:

- `--enabled off` disables it, so it registers no accounts until `--enabled on`.
- `--uses 5` sets how many more accounts it may register.
- `--expires 30d` moves its expiration; a time in the past ends it now.
- `--name web02` renames it.

The key ID and HMAC key never change. Add `--dry-run` to see what would change, each setting old → new, without saving anything. Running the same command again changes nothing more. If the EAB changed in between (an ACME client registering with it takes a use, too), nothing is saved and the command fails with `acme_changed`: run it again.

`pkiaas acme eab delete 12` deletes it, after showing what it deletes and asking you to confirm. **It can't be undone.** Without a terminal, add `--yes` to delete without asking. Running it again after it succeeded fails with `not_found` (exit code 4).

**Accounts keep working.** Disabling or deleting an EAB stops new registrations only: ACME accounts already registered with it keep getting certificates. Revoking the CLI login that created an EAB doesn't stop the EAB or its accounts either.

You can also manage EABs on the website, under **ACME -> Policies**, with the gears in the "External Account Bindings" column.

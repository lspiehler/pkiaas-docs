---
title: "ACME Provisioning URLs in the pkiaas CLI"
description: "List, show, disable, enable and delete a CA's deprecated ACME provisioning URLs with the pkiaas CLI. New ACME clients register with an EAB instead."
---
## Overview
Before external account bindings (EABs), an ACME client registered under an ACME policy through a provisioning URL: an ACME directory URL with a secret in its path. **Provisioning URLs are deprecated, and new ones can't be created.** Register new clients with an [EAB](acme-eabs.md) instead.

Existing provisioning URLs keep working. The `pkiaas acme provisioning-url` commands list them and disable, enable or delete them. They work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). A provisioning URL is named by its numeric ID, which `pkiaas acme provisioning-url list` shows.

The URL's secret is never shown: PKIaaS.io stores only its hash, so a lost provisioning URL can't be recovered. Create an EAB instead.

## List and Show Provisioning URLs
```text
$ pkiaas acme provisioning-url list
Provisioning URLs of Example Issuing CA (a1B2c3D4e5) (deprecated: use EABs instead)
ID   NAME   POLICY             STATUS   USES  EXPIRES               ACCOUNTS
295  fleet  Web servers (205)  enabled  2     2026-12-31T23:59:59Z  3
1 provisioning URL
```

- **Status:** `enabled` means it can register an account now. Otherwise it shows the first of `disabled`, `expired` and `used` (no uses left) that applies.
- **Filters:** `--policy "Web servers"` keeps one policy's provisioning URLs, `--status enabled,disabled,expired,used` those with one of the statuses, and `--search fleet` those whose name contains the text.

`pkiaas acme provisioning-url show 295` shows one provisioning URL.

## Disable or Enable a Provisioning URL
```sh
pkiaas acme provisioning-url update 295 --enabled off
```

A disabled provisioning URL registers no accounts until `--enabled on`. Add `--dry-run` to see what would change without saving anything. Running the same command again changes nothing more and says so ("No changes: ... is already disabled.").

`--enabled on` only restores it. Its uses and expiration don't change, so an expired or used-up provisioning URL stays that way, and the command reminds you to create an EAB instead.

## Delete a Provisioning URL
`pkiaas acme provisioning-url delete 295` deletes it, after showing what it deletes and asking you to confirm. **It can't be undone**, and provisioning URLs can't be created any more. Without a terminal, add `--yes` to delete without asking. Running it again after it succeeded fails with `not_found` (exit code 4).

**Accounts keep working.** Disabling or deleting a provisioning URL stops new registrations only: ACME accounts already registered with it keep getting certificates.

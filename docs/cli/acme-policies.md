---
title: "ACME Policies in the pkiaas CLI"
description: "List, show, create, change and delete a CA's ACME policies with the pkiaas CLI, including pre-approved domains and moving ACME accounts to another policy."
---
## Overview
ACME clients such as certbot get certificates from a CA by registering under one of its ACME policies, with EAB credentials made for that policy. A policy names the template certificates are issued with, and the domains an order may have without a challenge (pre-approved domains). See the [ACME overview](../acme/overview.md) for how ACME works in PKIaaS.io.

The `pkiaas acme policy` commands work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). A policy is named by its numeric ID, which `pkiaas acme policy list` shows.

## List and Show Policies
`pkiaas acme policy list` lists the CA's policies by name, with their template, pre-approved domains and how many EABs, ACME accounts and issued orders each has:

```text
ACME policies of Example Issuing CA (a1B2c3D4e5)
ID   NAME         TEMPLATE    PRE-APPROVED      EABS  ACCOUNTS  ORDERS
205  Web servers  Web Server  *.example.com +1  3     2         14
1 ACME policy
```

- **Search:** `--search example.com` keeps the policies whose name, template or pre-approved domains contain the text.
- **Sort:** `--sort accountCount --order desc` sorts by name, template, preApprovedDomains, eabCount, accountCount or validOrderCount.
- **More than 50:** `--limit` lists up to 1000.

`pkiaas acme policy show 205` shows one policy with all its pre-approved domains.

## Create a Policy
```sh
pkiaas acme policy create --name "Web servers" --template "Web Server" --pre-approved "*.example.com,example.org"
```

This does the same as the website's [Create an ACME Policy](../acme/create-acme-policy.md) form.

- **Name:** 1 to 50 letters, digits, spaces, hyphens and underscores.
- **Template:** the name (any case) or ID of one of the CA's templates, as `pkiaas template list` shows it. If two templates have the same name, give the ID.
- **Pre-approved domains:** comma-separated, or repeat `--pre-approved`. `*` matches any text, and `*.example.com` also matches `example.com`. They are saved in lowercase. Other names need an HTTP-01, DNS-01 or TLS-ALPN-01 challenge. Without `--pre-approved`, every name needs a challenge.
- **Safe to repeat:** give `--idempotency-key` with any text, e.g. a UUID. Running the same command again with the same key within 24 hours returns the policy it created instead of a second one.

Anyone with the policy's EAB credentials can get certificates for its pre-approved domains without proving they control them. Pre-approve only domains you trust every holder of those credentials with.

Next, [generate EAB credentials](../acme/generate-eab-credentials.md) for the policy on the website.

## Change a Policy
`pkiaas acme policy update 205` changes only the settings whose flags you give:

- `--name "Web servers 2"` renames it.
- `--template "Web Server"` chooses another template.
- `--pre-approved "*.example.com,example.org"` replaces the whole list. `--pre-approved ""` clears it, so every name needs a challenge.

Accounts, EABs and earlier orders stay as they are; the new settings apply to the orders that follow. Add `--dry-run` to see what would change, each setting old → new, without saving anything. Running the same command again changes nothing more, and if someone changed the policy at the same time, nothing is saved and the command asks you to run it again.

If the policy's template was deleted, the policy shows no template, and its orders fail until you choose another with `--template`.

## Delete a Policy
`pkiaas acme policy delete 205` deletes a policy with its EAB credentials and provisioning URLs, so ACME clients can no longer register with them. **It can't be undone.**

The command first shows what the delete takes with it, then asks you to confirm. Add `--dry-run` to see that and delete nothing.

A policy with ACME accounts isn't deleted on its own. Move its accounts to another policy of the same CA, where they keep working:

```sh
pkiaas acme policy delete 205 --move-accounts-to 206
```

Without `--move-accounts-to`, the command fails with `policy_has_accounts` (exit code 5) and deletes nothing.

- **In scripts:** without a terminal, add `--yes` to delete without asking.
- **Changed in between:** if someone changed the policy after the command showed what the delete takes with it, nothing is deleted. Run the command again.

You can also manage ACME policies on the website, under **ACME -> Policies**.

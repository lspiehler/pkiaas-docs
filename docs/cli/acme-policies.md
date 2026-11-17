---
title: "ACME Policies in the pkiaas CLI"
description: "List, show, create, change and delete a CA's ACME policies with the pkiaas CLI, including pre-approved domains, moving ACME accounts to another policy, and restoring a policy's earlier revisions."
---
## Overview
ACME clients such as certbot get certificates from a CA by registering under one of its ACME policies, with EAB credentials made for that policy. A policy names the template certificates are issued with, and the domains an order may have without a challenge (pre-approved domains). See the [ACME overview](../acme/overview.md) for how ACME works in PKIaaS.io.

The `pkiaas acme policy` commands work in the active CA, or the one `--ca` names (see [Choose Your CA](certificate-authorities.md#choose-your-ca)). A policy is named by its name (any case) or its numeric ID, which `pkiaas acme policy list` shows, e.g. `pkiaas acme policy show "web servers"`. If two policies have that name, or a number is one policy's ID and another's name, the command fails with `policy_ambiguous` and lists their IDs: give the ID then. Scripts that change things should always use the ID.

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

Next, [create an EAB](acme-eabs.md) for the policy with `pkiaas acme eab create`, or [generate EAB credentials](../acme/generate-eab-credentials.md) on the website.

## Change a Policy
`pkiaas acme policy update 205` changes only the settings whose flags you give:

- `--name "Web servers 2"` renames it.
- `--template "Web Server"` chooses another template.
- `--pre-approved "*.example.com,example.org"` replaces the whole list. `--pre-approved ""` clears it, so every name needs a challenge.

Accounts, EABs and earlier orders stay as they are; the new settings apply to the orders that follow. Add `--dry-run` to see what would change, each setting old → new, without saving anything. Running the same command again changes nothing more, and if someone changed the policy at the same time, nothing is saved and the command asks you to run it again.

If the policy's template was deleted, the policy shows no template, and its orders fail until you choose another with `--template`.

## Delete a Policy
`pkiaas acme policy delete 205` deletes a policy with its [EABs](acme-eabs.md) and [provisioning URLs](acme-provisioning-urls.md), so ACME clients can no longer register with them. **It can't be undone.**

The command first shows what the delete takes with it, then asks you to confirm. Add `--dry-run` to see that and delete nothing.

A policy with ACME accounts isn't deleted on its own. Move its accounts to another policy of the same CA, where they keep working:

```sh
pkiaas acme policy delete 205 --move-accounts-to "Intranet servers"
```

Without `--move-accounts-to`, the command fails with `policy_has_accounts` (exit code 5) and deletes nothing.

- **In scripts:** without a terminal, add `--yes` to delete without asking.
- **Changed in between:** if someone changed the policy after the command showed what the delete takes with it, nothing is deleted. Run the command again.

## Policy History
Creating a policy and every change of its name, template or pre-approved domains is saved as a revision, whether it was made on the website, with the CLI or with the API. Accounts, EABs and orders aren't part of it.

`pkiaas acme policy revision list "Web servers"` lists them, newest first, with who saved each, from where, and what changed:

```text
Revisions of ACME policy Web servers (205) of Example Issuing CA (a1B2c3D4e5)
REVISION  SAVED (UTC)       BY                 VIA      CHANGED
3         2026-11-15 08:15  admin@example.com  cli      restored from 1: pre-approved domains
2         2026-11-14 12:00  -                  outside  changed outside history: name, template
1         2026-11-14 09:30  admin@example.com  app      as created
3 revisions
```

- **Via:** where it was saved: `app` or `admin` (the website), `cli`, or `api` (another API client).
- **Found and outside:** a policy saved before PKIaaS.io began keeping its history has no revisions until its next change, which first records it as it was (`found`). A change made without a revision, such as by an older release of the server, is recorded at the next change (`outside`). Neither has a user.
- **More than 50:** `--limit` lists up to 1000.

`pkiaas acme policy revision show "Web servers" 1` shows the name, template and pre-approved domains of revision 1.

`pkiaas acme policy revision restore "Web servers" 1` saves the settings of revision 1 as a new revision, marked as restored from 1; history is never rewritten. Run it with `--dry-run` first to see what would change, without sending anything:

```text
$ pkiaas acme policy revision restore "Web servers" 1 --dry-run
Dry run: would restore revision 1 of ACME policy Web servers (205) as a new revision; nothing was sent.
  Name: Web servers → Web
  Template: Web Server (tmplweb001) → Intranet (tmplint001)
  Pre-approved domains: *.example.com, example.org → *.example.com
```

As with `pkiaas acme policy update`, accounts, EABs and earlier orders stay as they are, and the restored template and domains apply to the orders that follow. Restoring settings the policy has already changes nothing. The CA's log records each restore.

- **Template deleted since:** a revision whose template was deleted is refused with `template_not_found`, and nothing is saved. Restore another revision, or choose a template with `pkiaas acme policy update --template`.
- **Changed in between:** if someone changed the policy after the command read it, nothing is saved and the command fails with `acme_changed`: run it again.
- **Wrong number:** a revision the policy doesn't have fails with `revision_not_found` (exit code 4). `pkiaas acme policy revision list` shows the numbers.
- **Saved by a newer server:** a revision that a later release of the server saved can't be read or restored by this one (`acme_revision_unreadable`). Restore another revision.

You can also manage ACME policies on the website, under **ACME -> Policies**.

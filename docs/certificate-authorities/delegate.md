---
title: Delegate Access to a CA
description: Learn how to delegate access to a certificate authority on PKIaaS.io.
---
To allow multiple users to share management of a certificate authority (CA) on PKIaaS.io, you can delegate access to the CA. Delegation enables other users to issue certificates, manage templates, and perform other administrative tasks without needing to share account credentials.

## Delegating a CA
To delegate access to a CA, follow these steps:

1. Log in to [PKIaaS.io](https://www.pkiaas.io/auth/login).
2. Navigate to **Certificate Authorities -> Manage CAs** in the left navigation pane.
3. Click on the CA you want to delegate.
4. Select **Delegate Access** from the menu.
5. On the delegation page, click "Invite".
6. Enter the email address of the user you want to delegate access to. You may optionally choose an authentication provider to force the user to login with while logging in to accept the invitation and whether to require the login email to match the email address provided.
7. Click "Send Invitation" to send the invitation email to the user.
8. The invited user will receive an email with a link to accept the invitation. Once accepted, the user will have access to the delegated CA. The invitation must be accepted within 7 days, or it will expire.

**Note:** When sending a delegation invitation, use of the "Authentication Provider" option and "Require login email to match invitation email" is recommended to improve security. Without these options, any user with access to the link in the invitation email can accept the invitation.

## Resending Invitations
If the invited user does not receive the invitation email or it expires, the invitation can be resent. To resend an invitation:

1. Log in to [PKIaaS.io](https://www.pkiaas.io/auth/login).
2. Navigate to **Certificate Authorities -> Manage CAs** in the left navigation pane.
3. Click on the CA you want to resend the invitation for.
4. Select **Delegate Access** from the menu.
5. On the delegation page, select the user you want to resend the invitation to.
6. Click the "Resend" button.

## Remove Delegated Access
To remove delegated access for a user:

1. Log in to [PKIaaS.io](https://www.pkiaas.io/auth/login).
2. Navigate to **Certificate Authorities -> Manage CAs** in the left navigation pane.
3. Click on the CA you want to remove delegated access from.
4. Select **Delegate Access** from the menu.
5. On the delegation page, select the user you want to remove.
6. Click the "Remove" button.

## Limitations
* The owner of the CA must be a Patreon subscriber to lift account limitations for all delegated users.
* PKIaaS.io currently does not support RBAC (Role-Based Access Control) for delegated CAs. All delegated users will have full administrative access to the CA, including the ability to delete it and delegate to other users.
* Delegated users may remove access to other delegated users, except the CA owner.

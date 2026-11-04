---
title: Status and Ping
description: Read the IoT-HSM page's status icons, ping an appliance, and know what to do when an appliance needs attention.
---
The **IoT-HSM** page, under **Certificate Authorities** in the navigation pane, shows each IoT-HSM appliance that holds your CA keys and what PKIaaS.io last heard from it. It appears when you can see at least one CA with an HSM key.

PKIaaS.io hears from an appliance only when it asks it something: a signature, a CRL or a ping. There is no live status, so an idle appliance and one that is switched off look the same until it is pinged or asked to sign.

## Appliances

Each card is one appliance, titled **IoT-HSM appliance** and its ID, with the CAs whose keys it holds. The card shows the appliance's IoT-HSM version and when it last answered.

* **Update available** means a newer IoT-HSM release exists. The version next to it links to the release notes. Update the appliance; if it runs as a container, update its image.
* **Older agent** means the appliance runs a version from before IoT-HSM 1.0.0. It signs, but doesn't describe itself, so its version, token and PIN state aren't shown. Update it to see them.

CAs that no appliance has answered for yet are listed together on the last card, **Appliance not known yet**. Ping one of them to find out which appliance holds its key.

## Status icons

Each CA has a status icon before its name, on the IoT-HSM page and in **Manage CAs**. Click the icon to open the CA's details. A card's icon shows the worst status of its CAs.

| Icon | Status | Meaning | What to do |
| --- | --- | --- | --- |
| Red ✕ | Dormant | No answer for over 7 days, and the last request went unanswered. Requests for the CA fail at once. | Check that the appliance is on and online, that IoT-HSM is running and that the token is in it. Restart IoT-HSM, then ping again. A restart, or a ping it answers, ends dormant at once. |
| Red ✕ | PIN rejected | The token refused the PIN the appliance has, so it signs nothing for the token's CAs. | In the IoT-HSM web interface, choose **HSM Options**, then **Set PINs**, and enter the right PIN; saving reloads the slots. Don't retry the wrong PIN: a YubiKey locks after 3 wrong PINs. |
| Red ✕ | PIN locked | The token is locked after too many wrong PINs. | Unblock the PIN with the token's PUK, then set it in the IoT-HSM web interface (**HSM Options**, **Set PINs**). |
| Amber ▲ | Busy | Its last answer said it was too busy to sign in time. | Usually passes on its own. If it keeps happening, check the appliance's load, or spread the CAs over more appliances. |
| Amber ▲ | PIN: one try left | Wrong PINs were tried on the token; one more locks it. | Correct the PIN in the IoT-HSM web interface (**HSM Options**, **Set PINs**) before anything signs with it again. |
| Amber ▲ | PIN: tries running low | Wrong PINs were tried on the token. | Correct the PIN in the IoT-HSM web interface (**HSM Options**, **Set PINs**) before it locks. |
| Amber ▲ | No answer to the last ping | The ping reached the appliance and nothing answered in 10 seconds. | Check that the appliance is on and online, that IoT-HSM is running and that the token is in it. Restart IoT-HSM, then ping again. |
| Green ● | Answered in the last 7 days | The appliance answered a request or a ping in the last 7 days. It's not a live status. | Nothing. Ping it to check now. |
| Grey ? | Not heard from in over 7 days | Nothing for over 7 days. Not a fault in itself: a CA nobody uses has nothing to answer. | Ping it. The CA's next request also tests it. |
| Grey ? | Nothing heard from it yet | No appliance has answered for the CA yet. | Ping it. |

The **Help** button on the IoT-HSM page shows the same list.

## Ping

**Ping** asks the appliance to answer for a CA without signing anything. It takes up to 10 seconds, and the result shows under the button, for example "Answered in 0.4 s" or "No answer in 10 s". An answer updates the CA's status and details.

A CA can be pinged once a minute; a second ping within the minute shows the first one's result. Each CA can be pinged up to 60 times a day.

If the appliance's message certificate has expired, the appliance renews it with the CA key before it answers, which is one signature on the HSM.

## Details

Click a CA's name to see its details: its status and what to do about it, when the appliance last answered, signed and started, the result of the last ping, the appliance's version and software, and the token and key.

The same information is available from the command line with `pkiaas hsm list`, `pkiaas hsm show` and `pkiaas hsm ping`.

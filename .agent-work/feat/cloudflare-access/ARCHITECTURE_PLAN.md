# Cloudflare Access architecture proposal

Status: APPROVED by the user on 2026-11-25. Live application remains pending.

## Architecture Summary

Browser -> Cloudflare Access -> existing Cloudflare Tunnel -> existing proxy
-> Nginx landing or protected service.

Configure one self-hosted Access application per exact hostname for clear
policy auditing and route-specific audience validation:

| Application | Protected hostname |
| --- | --- |
| SKYSERVER landing | skydriven.xyz |
| SKYSERVER uptime | uptime.skydriven.xyz |
| SKYSERVER metrics | beszel.skydriven.xyz |
| SKYSERVER deployments | coolify.skydriven.xyz |

Use an Allow policy containing only the exact approved address from the
conversation. Reuse an existing suitable login method; otherwise enable email
one-time PIN. Proposed application session duration: 8 hours. Default deny
applies to everyone outside the allowlist. Do not add Everyone, email-domain
wildcards, Bypass rules, or Service Auth exceptions as part of this feature.

Do not include nextcloud.skydriven.xyz in these applications or a wildcard
application. Inspect pre-existing wildcard/more-specific applications before
changes, since they may alter the effective policy.

## Reused Components

- Existing Nuxt landing, four service URLs, Nginx image, and Docker network.
- Existing Cloudflare zone, tunnel, proxy routing, and service-native logins.
- Existing approved identity provider when suitable; do not replace it blindly.

## Database Schema Changes

None. Cloudflare manages identity checks and Access sessions. The Nuxt client
does not receive a stored password, API token, or private allowlist.

## Security & Tenancy

- Cloudflare enforces authentication before serving the protected applications.
- Enable Protect with Access on each protected hostname's tunnel route, using
  the correct team name and corresponding application audience tag.
- Preserve route destinations and any existing Host-header/TLS requirements.
- A wildcard tunnel route or shared ingress may need explicit per-host routes;
  inspect actual configuration before proposing a mutation.
- Audit public IP/port exposure and alternate hostnames. Tunnel validation does
  not protect an independently reachable origin. Close or separately protect
  bypass routes before claiming protection is complete.
- Retain service-native authorization after Access; Access does not grant an
  application account or administrator role.
- Keep Nextcloud outside this change so its browser and sync authentication
  remain owned by Nextcloud.
- Configuration is not active until applied and verified in the real account.

## QA Risk Matrix

| Risk | Verification |
| --- | --- |
| Direct service URL bypass | Fresh anonymous browser for every protected hostname |
| Wrong email selector or permissive existing policy | Inspect effective policy and test unlisted identity |
| Incorrect audience/team rejects valid users | Approved-user login and real application response per route |
| Alternate origin bypass | Inspect proxy/network exposure and test documented public alternate routes |
| Nextcloud accidentally gated | Check direct Nextcloud login and a representative sync client |
| Application assets/API requests blocked after login | Browser console/network checks during actual service use |
| Expired session still reaches content | Revoke/expire a test session and repeat protected requests |
| Existing automation disrupted | Inventory API/webhook consumers before activating browser-only Access |

## Implementation Tasks

- TASK-001: Inspect actual Cloudflare account applications/policies, approved
  identity providers, tunnel routes, proxy/origin exposure, and service consumers.
  Record existing settings for a targeted rollback. Do not copy credentials into
  task artifacts.
- TASK-002: Prepare exact application/policy and tunnel changes for the approved
  scope. If an existing configuration conflicts, revise this plan for review
  before applying changes. Missing live access remains an explicit blocker.
- TASK-003: Configure the four Access applications, approved login method,
  exact-email Allow policies, 8-hour sessions, and corresponding tunnel token
  validation. Preserve Nextcloud and unrelated policies.
- TASK-004: Verify allowed/denied/anonymous flows, direct service URLs, sessions,
  native service authorization, assets/API use, and origin bypass resistance.
- TASK-005: Document verified settings and setup/recovery steps in the repository
  without publishing personal allowlists or secrets. Request the workflow's final
  user verdict; do not imply a commit or deployment is approved.

## Rollback

Restore only the applications/policies/route settings changed by this task from
the recorded prior state. Never remove unrelated existing protection. Rollback
may reopen formerly public services and requires explicit review before live use.

## References

- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/
- https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/origin-parameters/#access

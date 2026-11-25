# Cloudflare Access setup

Status: approved design; live configuration and verification are pending.
This document does not activate authentication. Access is configured in the
Cloudflare account and the existing tunnel, outside this Nuxt repository.

## Approved applications

Create or update these exact self-hosted applications, protecting the entire
hostname with no path restriction:

| Application           | Public hostname       | Session duration |
| --------------------- | --------------------- | ---------------- |
| SKYSERVER landing     | skydriven.xyz         | 8 hours          |
| SKYSERVER uptime      | uptime.skydriven.xyz  | 8 hours          |
| SKYSERVER metrics     | beszel.skydriven.xyz  | 8 hours          |
| SKYSERVER deployments | coolify.skydriven.xyz | 8 hours          |

Each application permits only the single email address approved by the owner
in the task conversation. Enter that address directly in Cloudflare. Keep the
personal allowlist and credentials out of repository source and screenshots.

`nextcloud.skydriven.xyz` is excluded. Preserve Nextcloud's native login and
desktop/mobile sync. Do not use `*.skydriven.xyz` for this policy.

## Inspect existing configuration

Before saving changes:

1. Confirm the Cloudflare account and zone for `skydriven.xyz`.
2. Inspect existing Access applications, wildcard/path-specific matches, policy
   actions, and login methods. Record the exact affected prior configuration in
   a private location so it can be restored without removing unrelated rules.
3. Locate the tunnel and route for each approved hostname. Record its actual
   service destination and existing Host-header/TLS settings; preserve them.
4. Check monitoring/API/webhook consumers. Browser authentication may interrupt
   non-browser clients. Resolve an actual conflict before activation; this plan
   does not authorize adding broad Bypass or Service Auth exceptions.
5. Inspect public origin IPs, port forwards, alternate DNS names, proxy routes,
   and any cached public responses. A protected tunnel does not secure a
   separately reachable origin. Do not claim completion until alternate public
   routes are closed or independently protected. Record intended private/LAN
   management access separately.

The local Compose file publishes no host ports, but it cannot establish the
exposure of the shared proxy or the other service containers.

## Configure login and policies

1. Open the [Cloudflare dashboard](https://dash.cloudflare.com/), select the
   correct account, and enter Zero Trust.
2. Inspect **Integrations > Identity providers**. Reuse a suitable approved
   provider if present. Otherwise select **Add new identity provider > One-time
   PIN**. This login method emails a code to an allowed address; it is not
   automatically enabled for every new organization.
3. Open **Access controls > Applications**. For each approved hostname, create a
   self-hosted application using **Self-hosted and private > Add public
   hostname**, or update the matching existing application after inspection.
4. Set the exact hostname from the table and leave its path unrestricted.
5. Configure an **Allow** policy with **Include > Emails** containing only the
   approved full email address. Reuse the same narrowly scoped policy where
   supported. Do not add an email-domain wildcard or an Everyone selector.
6. Enable only the approved login method for these applications. Set each
   application's session duration to **8 hours**. Do not alter organization-wide
   login/session settings or unrelated applications.
7. Inspect all effective policies for conflicting Allow, Bypass, Service Auth,
   or more-specific application rules. Default deny covers unmatched users;
   do not add an unnecessary catch-all rule that overrides the intended Allow.
8. Save each application and privately record its application audience (AUD)
   tag for the next step. Keep existing service-native logins and permissions.

## Validate tokens at the tunnel

For each of the four protected hostname routes:

1. Open **Networking > Tunnels**, select the existing tunnel, and open **Routes**.
2. Edit the route for the exact hostname and inspect its additional origin
   settings. Enable **Protect with Access**, providing the correct team name
   and the corresponding application's AUD tag.
3. Save without changing the origin service destination, TLS validation, or
   Host-header behavior.
4. If a shared wildcard ingress currently serves these hostnames, prepare
   explicit matching routes first. Do not enable a shared global requirement
   that also gates Nextcloud.

For a locally managed tunnel, the equivalent per-ingress origin configuration
has this shape. These are placeholders, not a deployable configuration; retain
the existing route's hostname and service:

```yaml
originRequest:
  access:
    required: true
    teamName: <existing-team-name>
    audTag:
      - <this-hostname-application-audience-tag>
```

Do not trust an arbitrary request header as proof of authentication. The tunnel
must validate the Access JWT signature and application audience. The origin must
also be unreachable through an unprotected public route.

## Verify before declaring completion

Record actual results for each protected hostname:

| Check                                       | Required result                                                                 |
| ------------------------------------------- | ------------------------------------------------------------------------------- |
| Fresh browser with no session               | Access authentication before application content                                |
| Direct service URL, asset, or API request   | Same Access protection; no path bypass                                          |
| Approved email                              | Successful login and working service, including its own authorization           |
| Unlisted identity                           | No protected application content                                                |
| Invalid/revoked/expired application session | Reauthentication or valid session renewal required before content               |
| Application use after login                 | Assets, API requests, metrics, and deployment controls work without auth errors |
| Public alternate origin/hostname            | Unreachable or independently protected                                          |
| Direct Nextcloud browser and sync client    | Existing native authentication and sync still work                              |

Use fresh isolated browser contexts for anonymous checks. In Playwright, avoid
including a saved authenticated storage state in the anonymous tests. Keep login
codes and session cookies out of reports. A redirect to a service's own `/login`
or `/dashboard` is not proof that Cloudflare Access is active.

Local Playwright tests of `.output/public` verify the Nuxt page only. They cannot
verify Cloudflare policies, tunnel token validation, or live origin exposure.

## Recovery

Use the privately recorded prior configuration to restore only settings changed
by this task. Restoring a previously public route can reduce protection: review
that consequence before applying a rollback. Preserve unrelated security rules,
Nextcloud routes, and existing service-native authentication.

## References

- [Self-hosted applications](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)
- [Email one-time PIN login](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/)
- [Tunnel Access-token validation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/origin-parameters/#access)

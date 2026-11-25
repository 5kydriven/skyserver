# Cloudflare Access protection

TASK_ID: feat/cloudflare-access
Workflow: FEATURE, MEDIUM

## Feature Scope

Protect skydriven.xyz and the uptime, beszel, and coolify subdomains with
Cloudflare Access. Preserve Nextcloud's native authentication and client access.
The user accepted Cloudflare Access and the feature workflow, then explicitly
excluded Nextcloud from the additional login gate.

## Business Goal

Require authentication when opening either the landing page or a protected
service URL directly. Hiding links does not meet this requirement.

## Actors & Permissions

- One approved email address supplied in the conversation. Configure it directly
  in Cloudflare; do not publish the personal allowlist in repository source.
- All other users are denied access to the four protected hostnames.
- Nextcloud continues to enforce its own account permissions.

## Requirements

- Use exact hostnames: skydriven.xyz, uptime.skydriven.xyz,
  beszel.skydriven.xyz, coolify.skydriven.xyz.
- Reuse an existing approved identity provider if present; otherwise propose
  email one-time PIN login for the supplied allowlist.
- Protect entire hostnames, including assets and service API paths.
- Validate Access tokens on each protected tunnel route.
- Inspect existing applications, policies, tunnel routes, and origin exposure
  before making changes. Preserve working unrelated policies.
- Verify anonymous, allowed-user, denied-user, and direct-URL access.

## Constraints

- Current Nuxt static build and Nginx deployment remain applicable.
- No live Cloudflare configuration is available through a connected plugin.
  Plugin search returned no Cloudflare integration. Browser inventory reported
  the browser access host unavailable; no dashboard state was inspected.
- Actual tunnel/proxy/firewall configuration is outside the inspected checkout.
- Scope approval is confirmed; architecture and final verdict gates remain pending.
- No commit, push, deployment, or live policy application has occurred.
- Preserve the existing uncommitted migration and favicon changes.

## Evidence

- README.md and compose.yml: landing container on npm_default, port 80 through
  existing proxy; no host ports published by this Compose service.
- app/pages/index.vue: four external service destinations, previously tested.
- Official Cloudflare documentation consulted for self-hosted applications,
  one-time PIN login, and tunnel origin Access-token validation.

## Acceptance Criteria

- Anonymous requests to each protected hostname cannot return application
  content, including direct service URLs and protected asset/API paths.
- The approved user can sign in and reach each protected application.
- An unlisted identity cannot reach protected application content.
- Sessions expire according to the configured duration; an expired session
  cannot reach protected content.
- Nextcloud browser login and existing sync-client behavior are preserved.
- Alternate public origin routes cannot bypass Access; private management
  routes are explicitly documented and scoped.
- Local Playwright results are not represented as proof of live Access policy.

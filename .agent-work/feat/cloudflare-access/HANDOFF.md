# Server handoff

Branch: dev. The user explicitly requested committing and pushing this session
to continue on the server. This is a work checkpoint, not approval to deploy or
to mark the Cloudflare Access feature complete.

## Completed application changes

- Migrated standalone index.html into app/pages/index.vue using Nuxt UI.
- Added the cyan/slate theme, responsive service cards, SEO metadata, and favicon.
- Added a Node 24 build stage that prerenders Nuxt and copies its output into
  the existing digest-pinned Nginx runtime.
- Updated compose.yml to build the image while retaining the landing service,
  homelab-landing container, npm_default network, port 80 proxy contract,
  healthcheck, and log rotation. No host port is published.
- Updated README.md and added docs/cloudflare-access.md.

## Verified on Windows, 2026-11-25

- npm run generate passed using Node 24.22.3. Nonfatal dependency/build warnings
  remain; generation does not mean the warning-free browser run covers them.
- docker compose -f compose.yml config -q passed.
- Playwright with Chrome passed at widths 1440, 1024, 768, 390, and 320 pixels:
  page hydration, metadata, service URLs, responsive layout, dark theme,
  keyboard order, visible focus, and card-click navigation.
- No browser errors, console warnings, failed requests, or HTTP errors were
  recorded after fixing the favicon. Prerendered content and links worked with
  JavaScript disabled.
- Service destinations were intercepted for click checks; external application
  health was not tested. Screenshots were visually inspected at desktop/mobile
  sizes. Local generated reports/screenshots under .output are not committed.
- Docker engine was stopped. Image build, container health, Debian deployment,
  and live Cloudflare authentication have not been verified.

## Approved Cloudflare scope

- Protect skydriven.xyz, uptime.skydriven.xyz, beszel.skydriven.xyz, and
  coolify.skydriven.xyz using Cloudflare Access.
- Allow only the exact email supplied by the user in the transferred conversation.
  Do not publish the personal allowlist or credentials in the repository.
- Use the approved suitable identity provider, otherwise email one-time PIN;
  application sessions last 8 hours.
- Validate Access tokens at the corresponding tunnel routes and audit public
  alternate-origin access. Preserve service-native authorization.
- Nextcloud is explicitly excluded and retains its own login/sync behavior.

Scope and architecture gates are APPROVED. Final verdict remains PENDING.
The workflow is at node_2_implementation, WAITING_EXTERNAL_ACCESS.

## Resume here

1. Pull dev in the server checkout and read docs/cloudflare-access.md plus the
   task's approved ARCHITECTURE_PLAN.md and IMPLEMENTATION_PLAN.md.
2. Inspect the actual Cloudflare applications/policies, identity providers,
   tunnel routes, proxy/firewall exposure, and automation/API consumers before
   applying settings. The Windows browser connection was unavailable and no
   Cloudflare plugin was connected; no live settings were changed.
3. Apply the approved policy in the correct account, preserving existing
   unrelated rules. Do not use a wildcard that also gates Nextcloud.
4. Verify anonymous, approved-user, denied-user, expired-session, direct-URL,
   origin-bypass, and Nextcloud behavior. Complete review/QA and obtain the final
   verdict before marking the feature complete.

Anonymous probes from Windows returned 200 for the landing and Beszel, a
same-host /dashboard redirect for Uptime Kuma, and a same-host /login redirect
for Coolify. None encountered an Access login. These are limited observations,
not a full audit of policies or origin exposure.

Task artifact paths in STATE.json are repository-relative for portability.
The workflow helper may rewrite them to the current checkout's absolute paths
when transitioning; preserve the recorded approvals and pending final verdict.

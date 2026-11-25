---
id: domain.landing
tag: [TAG:LANDING]
domain: Public landing page
updated: 2026-11-25T05:21:01+00:00
relevant_services: []
relevant_models: []
---

# Domain: Public landing page `[TAG:LANDING]`

## 1. Domain Overview
index.html is the active static service directory for skydriven.xyz. It links to Nextcloud, Uptime Kuma, Beszel, and Coolify on their existing subdomains. It contains its own CSS and has no login or application session. Each linked service owns its access policy. The Nuxt starter has not replaced this page.

---

## 2. Verified implementation files

- [index.html](../../../index.html)
- [compose.yml](../../../compose.yml)

No application services or database models are implemented.

## 3. Invariant Rules for Public landing page

- Keep the public directory accessible when implementing the future dashboard.
- External service links are navigation, not implemented backend integrations or health checks.
- Preserve service addresses unless link changes are requested; do not infer that protected services are publicly accessible.
- Inspect the rendered page to verify visual changes; a successful build alone does not establish appearance.

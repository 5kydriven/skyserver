---
id: domain.deployment
tag: [TAG:DEPLOY]
domain: Debian homelab deployment
updated: 2026-11-25T05:21:01+00:00
relevant_services: []
relevant_models: []
---

# Domain: Debian homelab deployment `[TAG:DEPLOY]`

## 1. Domain Overview
The deployment target is a Debian homelab. compose.yml currently mounts index.html read-only into a digest-pinned Nginx container. Project landing and container homelab-landing join external network npm_default; README documents a Traefik route to container port 80. The checkout is projects/skyserver under the homelab root. Nuxt production packaging is future work; the user decided no dev container is needed.

---

## 2. Verified implementation files

- [compose.yml](../../../compose.yml)
- [README.md](../../../README.md)

No application services or database models are implemented.

## 3. Invariant Rules for Debian homelab deployment

- No host port is currently published. Preserve proxy/network contracts unless migration is explicitly in scope.
- Use docker compose -f compose.yml config -q to validate configuration; it does not prove live service health.
- After replacing the bind-mounted static file during checkout, README specifies force-recreating landing.
- A future Nuxt deployment should build a production image with a compatible Node runtime and preserve intended proxy routing.
- Do not describe local checks as Debian deployment validation. No live server was contacted for this bootstrap.

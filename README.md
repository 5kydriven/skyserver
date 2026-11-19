# SKYSERVER

Landing page for the SKYSERVER homelab at https://skydriven.xyz.

## Current application

A static HTML service directory served by Nginx. The page has no application-level
login or session handling. Each linked service enforces its own access policy.

- `index.html`: landing page, styles, and service links.
- `compose.yml`: existing Docker Compose deployment, retaining project name
  `landing`, container name `homelab-landing`, and external network `npm_default`.

## Deploy on the existing homelab

The external Docker network `npm_default` must already exist. The existing
Traefik proxy joins that network and routes to `homelab-landing:80`.
No host port is published by this application.

```sh
docker compose -f compose.yml config -q
docker compose -f compose.yml up -d
```

The HTML is bind-mounted read-only. After replacing the file during a checkout
or pull, recreate the service to ensure the container sees the current file:

```sh
docker compose -f compose.yml up -d --force-recreate landing
```

The homelab checkout lives at `projects/skyserver`. Its legacy `landing` path is
a compatibility symlink, so existing deployment references continue resolving.
The independent repository must be cloned separately when restoring the homelab.

## Future admin dashboard

Framework selection and authentication are future work. Keep the public landing
page accessible and enforce authentication and authorization on server-side
admin routes and data operations when the dashboard is implemented.

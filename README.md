# SKYSERVER

Landing page for the SKYSERVER homelab at https://skydriven.xyz.

## Nuxt development

The repository includes a minimal Nuxt 4.7.0 starter. Dashboard structure and
landing-page migration will follow separately; Docker Compose still serves the
existing `index.html` through Nginx.

Use Node.js `^22.22.3`, `^24.15.0`, or `>=26.0.0` (Node 24 LTS recommended).

```sh
npm install
npm run dev
```

Open http://127.0.0.1:3000. Run `npm run build` to create a production build,
then `npm run preview` to preview it locally.

### VS Code

Install the workspace's recommended extensions when prompted: Vue (Official),
Prettier, and EditorConfig. Disable Vetur in this workspace if already installed.
Vue (Official) provides Vue and TypeScript language support; Prettier formats
Vue, JavaScript, TypeScript, and JSON files on save using `.prettierrc.json`.
EditorConfig standardizes indentation and line endings across editors.

Use **Terminal > Run Task** for the Nuxt dev, build, and preview commands.
These commands require the compatible Node version described above.

## Existing landing page

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

The homelab checkout and live bind mount use `projects/skyserver` directly.
From the homelab root, deploy with:

```sh
docker compose -f projects/skyserver/compose.yml up -d
```

The independent repository must be cloned separately when restoring the homelab.

## Future admin dashboard

Framework selection and authentication are future work. Keep the public landing
page accessible and enforce authentication and authorization on server-side
admin routes and data operations when the dashboard is implemented.

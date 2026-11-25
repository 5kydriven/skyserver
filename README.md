# SKYSERVER

Landing page for the SKYSERVER homelab at https://skydriven.xyz.

## Nuxt development

The public service directory runs on Nuxt 4 with Nuxt UI and Tailwind CSS.
Docker Compose builds a prerendered version and serves it through Nginx.

Use Node.js `^22.22.3`, `^24.15.0`, or `>=26.0.0` (Node 24 LTS recommended).

```sh
npm ci
npm run dev
```

Open http://127.0.0.1:3000. Run `npm run build` to create a production build,
then `npm run preview` to preview it locally.
Run `npm run generate` to produce the static site in `.output/public`, as used
by the Docker image. This deployment supports prerendered public pages; future
server-side APIs will require a Node runtime deployment.

### VS Code

Install the workspace's recommended extensions when prompted: Vue (Official),
Prettier, and EditorConfig. Disable Vetur in this workspace if already installed.
Vue (Official) provides Vue and TypeScript language support; Prettier formats
Vue, JavaScript, TypeScript, and JSON files on save using `.prettierrc.json`.
EditorConfig standardizes indentation and line endings across editors.

Use **Terminal > Run Task** for the Nuxt dev, build, and preview commands.
These commands require the compatible Node version described above.

## Public landing page

A Nuxt service directory prerendered for Nginx. The page has no application-level
login or session handling. Each linked service enforces its own access policy.

- `app/pages/index.vue`: landing page and service links using Nuxt UI cards.
- `app/assets/css/main.css` and `app/app.config.ts`: styles and UI theme.
- `Dockerfile`: Node 24 build stage and digest-pinned Nginx runtime.
- `compose.yml`: Docker Compose deployment, retaining project name
  `landing`, container name `homelab-landing`, and external network `npm_default`.

## Deploy on the existing homelab

The external Docker network `npm_default` must already exist. The existing
Traefik proxy joins that network and routes to `homelab-landing:80`.
No host port is published by this application.

```sh
docker compose -f compose.yml config -q
docker compose -f compose.yml up -d --build
```

After a checkout or pull, rebuild the image and recreate the service:

```sh
docker compose -f compose.yml up -d --build landing
```

The homelab checkout uses `projects/skyserver` directly.
From the homelab root, deploy with:

```sh
docker compose -f projects/skyserver/compose.yml up -d --build
```

The independent repository must be cloned separately when restoring the homelab.

## Future admin dashboard

The approved [Cloudflare Access setup](docs/cloudflare-access.md) covers the
landing page, Uptime Kuma, Beszel, and Coolify, while Nextcloud retains its native
login. Live Access configuration and verification are pending; repository changes
alone do not enable this protection.

The admin dashboard is future work. Preserve the landing page for authorized
users and enforce authentication and authorization on server-side admin routes
and data operations when the dashboard is implemented.

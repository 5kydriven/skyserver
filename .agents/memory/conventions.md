---
id: memory.conventions
updated: 2026-11-25T05:21:01+00:00
---
# Skyserver Conventions `[TAG:CONVENTIONS]`

- Nuxt 4.7.0, Vue 3, TypeScript; one app under `app/`, no Nuxt layers.
- Approved [architecture baseline](../../.agent-work/architecture/readable-nuxt/ARCHITECTURE_PLAN.md): read page code top to bottom; keep local logic inline where clear and use short descriptive names. Extract meaningful shared behavior, substantial UI, and security boundaries while following Nuxt practices.
- Architecture may evolve with demonstrated requirements or evidence. Explain material changes and migration scope, update affected guidance, and avoid speculative abstractions or unrelated rewrites.
- `app/app.vue` currently renders `NuxtWelcome`; dashboard routes and auth are future work.
- Keep `index.html` public. `compose.yml` still deploys Nginx; Nuxt is not deployed by that service.
- Preserve Compose project `landing`, container `homelab-landing`, and external network `npm_default` unless deployment work explicitly changes them.
- `dev` is development; `main` is production. Preserve unrelated changes and existing authorization; do not deploy without authorization.
- Node engine: `^22.22.3 || ^24.15.0 || >=26.0.0`. Use npm and the committed lockfile; use `npm ci` for reproducible installation.
- Match `.editorconfig` and `.prettierrc.json`: two spaces, LF, single quotes, no semicolons in JS/TS. Do not reformat unrelated files.
- No ORM, schema, PK strategy, tenancy, queues, API envelope, or transaction convention exists. Do not infer those from templates.
- No app session/auth exists. Future admin endpoints must enforce server-side authentication and authorization; route middleware alone is insufficient. Keep secrets outside client configuration.
- No test runner, lint, or typecheck script is configured. `npm run build` and a local HTTP check are verification, not test coverage or visual QA.
- Use graph discovery plus per-path coverage and exact source fallback. Consult Nuxt MCP for current APIs; templates and memory may be stale.

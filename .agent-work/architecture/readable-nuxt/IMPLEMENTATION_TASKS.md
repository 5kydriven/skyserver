# Implementation Tasks

TASK_ID: architecture/readable-nuxt
These tasks describe later work, not authorization to execute every phase now.

## TASK-001: Adopt the approved reading and naming rules

Status: recorded in the project conventions and dashboard guidance. The detailed
plan is approved as a living baseline, open to future changes. Remaining tasks are
deferred until the corresponding implementation scope is requested.

- Inspect/reuse: existing .agents/memory/conventions.md and dashboard chunk.
- Modify after approval: those guides, adding the concise agreed conventions.
- Keep detailed examples in one architecture reference; avoid duplicating rules.
- Acceptance: a developer can identify local state, fetch, derived values, and
  actions in reading order; short names remain unambiguous; no unused modules.

## TASK-002: Add development checks

- Inspect/reuse: package.json, lockfile, tsconfig, Prettier config, VS Code settings.
- Add a reproducible format check, Nuxt-aware linting, and nuxt typecheck with its
  required TypeScript/vue-tsc tooling; choose compatible versions at execution time.
- Keep Prettier responsible for formatting and ESLint responsible for code quality;
  avoid competing formatting rules and do not force semicolon/style rewrites.
- Acceptance: documented commands actually run; each failure is reported
  separately. Do not add an app test suite merely to test the welcome placeholder.

## TASK-003: Build the first route/layout slice

- Prerequisite: agree on the actual initial UI, including whether to migrate the
  public landing at this stage. No fake dashboard feature is implied by this plan.
- Modify app/app.vue for NuxtLayout/NuxtPage once page files are introduced.
- Add only used pages/layouts/components; keep one-use local behavior in pages.
- Reuse index.html content and service destinations if migrating the landing.
- Acceptance: SSR/direct navigation and client navigation work; loading, empty,
  error and success states are explicit; appearance is checked separately.
- Preserve the existing production Compose behavior during development.

## TASK-004: Add protected domain behavior when defined

- Prerequisite: choose the first data operation and session/access requirements.
- Add method-named server handlers, shared public contracts where needed, and
  reusable server auth/integration helpers. Keep handlers sequential.
- Select persistence only if the feature actually needs it. Define transaction,
  uniqueness, retry and concurrency rules with those operations.
- Test behavior with Vitest and Nuxt test utilities where appropriate. Add a
  Playwright journey for important routing/auth flows when they exist.
- Acceptance: unauthorized API requests are rejected directly; invalid inputs
  cause no side effects; secrets stay server-side; the route's flow remains clear.

## TASK-005: Implement production deployment separately

- Prerequisite: approve replacing the active static landing service with Nuxt.
- Add a production image with a compatible Node runtime; update Compose/proxy
  routing deliberately. No dev container is required.
- Acceptance: production build and container health verified; existing network,
  public route and admin policy maintained; Debian validation reported explicitly.

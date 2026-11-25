# Task Context

TASK_ID: architecture/readable-nuxt
Target branch: dev
Status: architecture direction approved as an adaptable baseline; implementation is a separate step.

## Feature

Plan a maintainable, scalable Nuxt architecture that reads from top to bottom.

## Business Goal

Make a feature understandable from its route without repeated navigation between
small wrappers, long names, or unnecessary abstractions. Keep Nuxt conventions,
SSR correctness, security, and testability while preferring local inline logic.

## Actors & Permissions

- Developer: reads and extends the code on Windows.
- Public visitor: retains access to the homelab landing directory.
- Future admin: protected dashboard access; auth design is not selected here.
- Operator: deploys on a Debian homelab through production Docker/Compose.

## Requirements

- One standard Nuxt app, with domain folders inside conventional directories.
- Simple descriptive names and a consistent declaration order.
- Page-local state, fetching, derived values, and actions remain visible together.
- Extract meaningful shared behavior, substantial UI, and server boundaries.
- Follow Nuxt data fetching, routing, SSR, configuration, and state practices.
- Give concrete extraction rules, examples, validation criteria, and a phased plan.

## Constraints

- Planning only: no application restructuring, dependency installation, or deployment.
- Preserve existing app, landing page, templates, and Compose configuration.
- No Nuxt layers or dev container in the initial architecture.
- Do not choose a database, auth provider, or feature requirements speculatively.
- Existing test/build capabilities must be distinguished from proposed tooling.

## Evidence

Current app/app.vue renders NuxtWelcome. package.json has build/dev/generate/
preview scripts and no app test/lint/typecheck scripts. Source reads and bounded
graph discovery show a starter, not an existing business architecture to refactor.

The user explicitly added that Nuxt best practices must be preserved. That
requirement takes precedence over making every expression inline.

The user approved this direction and explicitly requested that future architecture
changes remain possible. Treat the plan as living guidance and revise it when
concrete requirements or evidence justify doing so.

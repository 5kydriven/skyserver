# Acceptance Criteria

TASK_ID: architecture/readable-nuxt

## Architecture proposal

- Uses one conventional Nuxt app and distinguishes existing files from proposals.
- Keeps route-local behavior visible in the page in dependency/reading order.
- Gives concrete inline/extraction rules and short descriptive naming examples.
- Preserves meaningful composables, components, server boundaries and SSR practices.
- Defines page-local vs shared state and server vs client ownership.
- Preserves the public landing and deployment configuration until migration scope.
- Contains no speculative auth provider, database, generic repository layer or store.
- Provides reuse evidence, implementation phases, risks and verifiable QA criteria.

## Future implementation

- Custom imports and dependencies have a clear origin; no unnecessary barrels.
- Components use typed props/emits for shared UI; no implicit page-data ownership.
- useFetch/useAsyncData own initial SSR reads; action requests have local handling.
- Server endpoints enforce auth and input validation independently of route guards.
- No credentials enter shared code, public runtimeConfig, or rendered payloads.
- Refs/computed values avoid duplicate state; no mutable module-scoped user state.
- Each new file has a real consumer and responsibility. Splitting code must reduce
  complexity or enforce a boundary, rather than only reduce a page's line count.
- Build, lint, typecheck, tests, visual checks and deployment results are reported
  separately; proposed commands are not reported as currently installed checks.

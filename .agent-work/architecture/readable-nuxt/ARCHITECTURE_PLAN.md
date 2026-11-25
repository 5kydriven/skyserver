# Readable Nuxt Architecture

TASK_ID: architecture/readable-nuxt
Status: approved starting architecture; application changes are not implemented.

## Architecture Summary

Use one conventional Nuxt app. Keep each route's behavior visible in its page;
extract code when it has a clear responsibility, meaningful reuse, or a security
boundary. Scale by grouping related files in Nuxt's directories before adding
new architectural mechanisms.

### Evolution policy

This is a living baseline, not a permanent architecture contract. The user
approved the direction with the explicit condition that it remain open to future
changes. Revisit boundaries, folders, dependencies, and rendering/state choices
when real feature requirements, complexity, performance, or operational evidence
justify a change.

For a material revision, explain the concrete problem, proposed change, tradeoffs,
and migration scope. Keep changes proportional to the task and update the affected
guidance so the code and documented architecture agree. Preserve top-to-bottom
readability, clear naming, and Nuxt best practices as evaluation criteria; prefer
the solution that best serves those goals over rigidly preserving this layout.
Do not add speculative flexibility or perform unrelated rewrites in anticipation
of future requirements.

### Intended shape

This is an ownership map, not a request to create empty folders or placeholder
features. Only app/app.vue and nuxt.config.ts currently implement the Nuxt app.

```text
app/
  app.vue                 # NuxtLayout > NuxtPage once routes exist
  pages/
    index.vue             # Future public landing migration
    admin/
      index.vue           # Future overview
      services/
        index.vue         # Future service route and its local behavior
  layouts/
    default.vue           # Public shell when needed
    admin.vue             # Shared dashboard navigation and frame
  components/
    admin/                # Substantial shared admin UI
    services/             # Substantial service UI, when justified
  composables/            # Shared reactive behavior, e.g. useSession.ts
  middleware/             # Navigation guards, not API security
  utils/                  # Shared pure client helpers
  assets/                 # Global styles/tokens when needed
server/
  api/
    admin/services/       # Method-named handlers when implemented
  utils/                  # Shared auth checks/integration helpers
shared/
  types/                  # Public contracts used by app and server
  utils/                  # Pure helpers needed by both runtimes
test/
  unit/                   # Pure logic tests when behavior exists
  nuxt/                   # Nuxt runtime/component tests
  e2e/                    # Important browser journeys
```

Keep domain grouping within these directories. Do not add a feature framework,
barrel exports, a generic API client, repositories, or stores without a concrete
consumer and a reason. An integration client or data-access module is appropriate
when it owns real complexity; this is not a ban on future abstractions.

### Where each responsibility lives

| Responsibility | Default location | Extract when |
| --- | --- | --- |
| Route state, initial fetch, filters, actions | Page script | Shared behavior or a substantial independent concern emerges |
| Small view conditions and event calls | Template | Multi-step behavior needs an explicitly named action |
| Shared navigation and shell | Layout | Multiple screens need the frame |
| Reusable or substantial UI | Domain component | Reused, independently testable, or a coherent large section |
| Reactive workflow | Composable | Shared, or a self-contained lifecycle/polling/subscription concern |
| Stateless transformation | Local expression/function | Promote to utils only when shared |
| Authentication, input validation, protected I/O | Server handler | Share auth/integration behavior in server utilities |
| Cross-runtime response/input contract | shared/types | App and server actually share it |

### Reading order

Use script setup with TypeScript, then template, then scoped styles when needed.
Within the script, declare dependencies before their consumers:

1. Explicit imports of custom types/helpers, page metadata, props and emits.
2. Route/context inputs and local state.
3. Initial data fetching.
4. Computed/derived state.
5. User actions in the same order they appear in the UI.
6. Watchers and lifecycle effects, only when needed.

This order is a convention, not a reason to introduce forward references. A
helper used during setup belongs before that setup call. Prefer a clear direct
sequence over functions calling functions declared far away.

### Inline and extraction rules

- Keep a simple filter, boolean, assignment, or event call inline near its use.
- Use computed for derived lists or expensive/reused view expressions. A computed
  value is still visible page-local logic; do not replace it with a watcher that
  copies the result into another ref.
- Give a multi-step async action a named function. Keep its validation, request,
  success, error, and cleanup in one readable try/catch/finally sequence.
- Keep templates declarative. Avoid network calls, assignments with side effects,
  deep ternaries, and multi-step blocks inside template expressions.
- Do not extract a one-use pass-through wrapper just to shorten a page. Extract
  coherent reusable behavior or genuinely complex independent concerns instead.
- Duplication is a signal, not a numeric law. Share security and integration
  behavior early; unrelated lookalike code does not need a common abstraction.
- Component children receive props and emit intent. They normally do not fetch
  page-owned data or silently modify unrelated global state.

### Naming

Use the shortest name that remains clear within its scope:

| Purpose | Preferred examples | Avoid |
| --- | --- | --- |
| Collection/item | services / service | serviceCollectionData / s |
| Local text input | search | serviceSearchInputValue |
| Derived list | filteredServices | processedResultData |
| Boolean | isOpen, canEdit, isSaving | flag, state1 |
| Action | saveService, removeService | handleServiceSaveActionExecution |
| Scoped input | name, url | serviceFormNameInput |
| Multiple entities | serviceName, userName | Two unrelated values both called name |

Use camelCase variables/functions, PascalCase types/components, useX composables,
and Nuxt's route naming conventions. Choose Service, not IService/ServiceModelDTO,
unless those distinctions represent genuinely different contracts. Avoid generic
data/result names when several values are in scope. Local familiar callback names
remain fine when unambiguous.

For domain components, preserve default Nuxt path-based naming. For example,
components/services/Card.vue is used as ServicesCard; avoid repeating the domain
in both the folder and file name without a naming reason. Do not disable Nuxt
component prefixes just to make names shorter.

### Nuxt data, state, and imports

- Use useFetch for initial HTTP data; use useAsyncData for composed asynchronous
  reads. They transfer server-fetched results through the Nuxt payload.
- Use $fetch inside user-triggered actions, then refresh affected data after a
  successful write. Avoid watchers whose only purpose is redundant fetching.
- Keep fetched data in the fetching composable; do not mirror it into a second
  ref or global store. Use explicit shared keys only when cross-component data
  sharing is intentional, with compatible options and no user data leakage.
- ref/reactive own local state. Use useState only for genuinely shared SSR-safe
  state; do not create mutable module-level refs that can leak across requests.
- Pinia is a future option if shared state/workflows justify it; it is not an
  initial dependency. Do not use storage as an authoritative auth state.
- Use standard Nuxt/Vue auto-imports and component discovery. Prefer explicit
  imports for custom business helpers/types where they clarify origin. No custom
  recursive import configuration or barrel layer initially; nested composables
  and shared files need explicit imports if default scanning does not cover them.
- Keep browser-only APIs in appropriate client lifecycle code, ClientOnly, or
  client plugins as needed. Preserve SSR defaults; change rendering per route
  only for a demonstrated requirement.
- Prefer reactive fetch inputs/computed values over keeping independent copies
  of the same state. Clean up manually created subscriptions and timers.

### Illustrative page

This is a future example, not working application code: the endpoint and Service
contract are not implemented. Error text is deliberately safe for display.

```vue
<script setup lang="ts">
import type { Service } from '#shared/types/service'

const search = ref('')

const { data: services, status, error, refresh } = await useFetch<Service[]>(
  '/api/admin/services',
  { default: () => [] },
)

const filteredServices = computed(() => {
  const term = search.value.trim().toLowerCase()
  return services.value.filter((service) =>
    service.name.toLowerCase().includes(term),
  )
})
</script>

<template>
  <main>
    <h1>Services</h1>
    <label for="search">Search services</label>
    <input id="search" v-model="search" type="search" />
    <button :disabled="status === 'pending'" @click="refresh()">Refresh</button>

    <p v-if="status === 'pending'" role="status">Loading services...</p>
    <p v-else-if="error" role="alert">Could not load services. Try again.</p>
    <p v-else-if="!filteredServices.length">No services found.</p>
    <ul v-else>
      <li v-for="service in filteredServices" :key="service.id">
        {{ service.name }}
      </li>
    </ul>
  </main>
</template>
```

The route file shows fetching, filtering, and rendering without a page controller
composable, a separate store, or a wrapper around refresh. Extract a card once the
service row gains a substantial responsibility; don't fragment this small list.

## Reused Components

| Existing file | Reuse | Planned change boundary |
| --- | --- | --- |
| app/app.vue | Nuxt entry | Introduce NuxtLayout/NuxtPage only when routes exist |
| nuxt.config.ts | Central Nuxt configuration | Keep compatible defaults; add modules/config as needed |
| package.json and package-lock.json | npm/runtime contract | Add tooling only during approved implementation |
| tsconfig.json | Generated Nuxt project references | Extend Nuxt-generated config, do not replace it wholesale |
| .editorconfig and .prettierrc.json | Existing formatting | Keep style consistent; avoid unrelated rewrites |
| index.html and compose.yml | Working static landing/deployment | Preserve until explicit migration work |

No existing application services, domain models, API handlers, or auth utilities
were found in the bounded app/server/shared scope. Graph coverage is best-effort;
current starter source and config reads ground that conclusion. No runtime
application call chain exists to trace for a proposed feature.

## Database Schema Changes

None in this plan. Persistence, ORM, schema, ID strategy, and concurrency rules
will be selected against the first feature's data requirements. Do not create
generic repositories, pretend models, or tables now.

## Security & Tenancy

Future protected flow: page -> /api/admin handler -> server auth/permission check
-> validated input -> actual integration or persistence -> safe public response.

Navigation middleware improves UX but does not secure /api routes. Keep auth
checks reusable in server/utils and call them from every protected handler. Keep
secrets in private runtimeConfig and server code; shared/ contains public-safe
contracts/pure logic only. Avoid caching personalized responses across users.
Choose sessions, authorization, and CSRF protection with the auth implementation.
No tenancy exists or is proposed here.

Server handler reading order: authenticate/authorize, validate params/body/query,
perform the operation, return the safe result. Keep a simple single-use operation
inline; extract a service/client for real integration complexity or shared rules.
Catch errors where they can be meaningfully handled and preserve deliberate HTTP
errors; do not add catch-and-rethrow wrappers everywhere.

## QA Risk Matrix

| Risk | Impact | Planned mitigation |
| --- | --- | --- |
| Inline preference hides security checks | High | Keep server boundaries explicit; every protected endpoint enforces auth |
| Overgrown pages | Medium | Extract a coherent section/workflow when complexity makes the page harder to follow |
| Excessive helper/composable indirection | Medium | Review whether the reader can follow a route without trivial wrappers |
| Hydration duplication or browser globals on server | Medium | useFetch/useAsyncData, SSR-safe state, and correct client boundaries |
| Shared state or cached data leaks | High | No mutable module globals; scoped sessions and deliberate fetch/cache keys |
| Premature tooling or domain structure | Low | Create only consumed files; add testing tools with meaningful tests |
| Static landing/proxy regression | High | Defer migration; verify public route and proxy separately when changing them |

No current vulnerability is asserted by this proposed-risk matrix. Auth and
deployment work need feature-specific decisions before implementation.

## Implementation sequence

TASK-001: Document approved readability and naming conventions in the existing
project guidance. TASK-002: Add format/lint/typecheck tooling with a deliberate
Prettier/ESLint split. TASK-003: Introduce routes/layouts with the first real UI
slice. TASK-004: Add protected server behavior and relevant tests once feature/auth
scope is defined. TASK-005: Package Nuxt for Debian deployment as separate work.
See IMPLEMENTATION_TASKS.md for boundaries and acceptance conditions.

## Official references

- [Nuxt data fetching](https://nuxt.com/docs/4.x/getting-started/data-fetching)
- [Nuxt app auto-imports](https://nuxt.com/docs/4.x/guide/concepts/auto-imports)
- [Shared runtime boundaries](https://nuxt.com/docs/4.x/directory-structure/shared)
- [Route middleware](https://nuxt.com/docs/4.x/getting-started/routing#route-middleware)
- [Runtime configuration](https://nuxt.com/docs/4.x/guide/going-further/runtime-config)
- [Nuxt testing](https://nuxt.com/docs/4.x/getting-started/testing)

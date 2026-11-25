# Skyserver Agent Setup Report

## Scope and approved defaults

- Mode: UPDATE, preserving existing golden templates and task history.
- Protected custom agents: none specified.
- Domains: Nuxt dashboard, public landing page, Debian homelab deployment.
- Branches: `dev` for development; `main` for production.
- Check detection: no automated application test runner is configured.

## Verified repository state

The application is a Nuxt 4.7.0 starter using Vue 3 and TypeScript. The root
component renders `NuxtWelcome`. The live deployment configuration remains a
static HTML service directory in Nginx. The dashboard, application authentication,
database, ORM, tenancy, and application API are not implemented.

Evidence came from the graph project `C-Users-KODA-JA-Documents-skyserver`, file
inventory, per-path coverage, and current source/configuration reads. The graph
reported changed metadata for evidence paths; source reads supplied the current
facts. Coverage is a best-effort signal, not a completeness guarantee.

## Generated setup

- [Memory router](memory/INDEX.md), conventions, three domain chunks, two catalogs,
  a slim [history router](MEMORY.md), and an [archive](MEMORY_ARCHIVE.md).
- Six [role guides](README.md#roles), [context boundaries](CONTEXT_POLICY.md),
  feature/hotfix workflows, and one lean global guardrail document.
- On-demand QA and workflow-optimization skills. Test guidance is a QA reference,
  not an always-on persona rule.
- Python state, artifact-validation, catalog-inventory, and smoke-test helpers.

The generated documents derive from the golden templates, with backend-specific
assumptions replaced or qualified for the current Nuxt starter. Relative links
work across Windows and Debian checkouts. No previous memory/history files
existed; the new archive contains no fabricated completed-task records.

## Verification

- All nine isolated helper smoke tests passed on Windows with Python 3.14.3.
  They exercise task-path confinement, state/history preservation, corruption
  handling, final release gating, three-failure review/QA escalation, explicit
  verdicts, artifact acceptance/rejection, and catalog additions/removals.
- Generated Python parses successfully; generated YAML metadata and both skill
  frontmatters validate. Generated Markdown links resolve and contain no
  unresolved template placeholders or machine-specific file URLs.
- The master index measures 118 reference tokens; global guardrails measure
  256 reference tokens and 1,235 UTF-8 bytes across 14 lines. Token counts use
  `cl100k_base` as a reproducible reference, not a promise for every host tokenizer.
- The root history router is 27 lines. Golden templates and application files
  remain unchanged.

## Limits and operational notes

- The catalog helper inventories bounded Nuxt file paths. It does not implement
  TypeScript AST analysis or infer database tables, keys, or relationships.
- State files support one orchestrator. Atomic replacement protects writes;
  concurrent-writer locking and a full enforced transition topology are not
  implemented. Human gate values record actual user decisions; the script cannot
  authenticate or grant user approval.
- Role guides do not register slash commands or launch agents. Load them through
  the host's supported workflow; delegate only within authorization.
- Python 3.10+ is required for helpers, separate from Nuxt's Node requirement.
  PHP templates remain untouched alternatives; generated helpers use Python.
- No application build, browser comparison, Docker launch, or live Debian
  deployment was performed for this documentation/helper-only change.
- No dev container, application dependency, or global agent configuration was
  added. No commit, push, PR, or deployment was performed by this bootstrap.

See [the quick-start guide](README.md) for role paths and helper commands.

# Skyserver Global Guardrails

1. Follow the user's scope and existing authorization; obtain unresolved human gate decisions before proceeding.
2. Preserve unrelated edits, golden templates, and feature history. Use minimal diffs.
3. Read the [router](../memory/INDEX.md) and only relevant chunks; verify live source before reuse.
4. Use graph discovery, relevant traces/snippets, and per-path coverage; read missed source directly.
5. Follow [conventions](../memory/conventions.md) and [context policy](../CONTEXT_POLICY.md).
6. Keep one Nuxt app; no layers or dev container without a demonstrated need and task scope.
7. Keep the landing public and preserve current Compose/proxy contracts unless migration is requested.
8. Future admin operations need server-side authentication and authorization; never expose credentials in client code.
9. No database, ORM, auth, or test runner exists yet. Document absence; do not invent conventions.
10. Build, test, HTTP, visual, and live deployment checks are separate evidence. Report limits accurately.
11. Respect approved task scope; commit, push, open a PR, or deploy only when authorized for that task.
12. Load role and QA instructions on demand; keep this directory free of personas.

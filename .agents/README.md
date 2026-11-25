# Skyserver Agent Setup

Start with [memory/INDEX.md](memory/INDEX.md), then read only the relevant chunk.
Follow the [context policy](CONTEXT_POLICY.md) and [lean guardrails](rules/codebase-standards.md).

## Roles

These are instruction documents to load through the host agent, not registered commands:

- [Task context builder](agents/task-context-builder/agent.md)
- [Architect](agents/architect/agent.md)
- [Implementation engineer](agents/implementation-engineer/agent.md)
- [Code reviewer](agents/code-reviewer/agent.md)
- [QA validator](agents/qa-validator/agent.md)
- [Release manager](agents/release-manager/agent.md)

Use the [feature workflow](workflows/multiple-agent-workflow.md) or
[hotfix workflow](workflows/hotfix-workflow.md) when applicable. Small tasks can
run directly; use additional agents only when authorized and supported by the host.
The scope, architecture, and final-release gates require decisions not already
authorized by the user. Task packets follow [the existing template](templates/TASK_PACKET.md).

## Local helpers

Python 3.10+ is optional tooling for this workflow, separate from the Nuxt runtime.
Use `python` on Windows or `python3` on Debian. Run from the repository root:

```sh
python .agents/scripts/sync-catalogs.py
python .agents/scripts/manage-state.py --action=init --task=feat/example --complexity=SMALL
python .agents/scripts/manage-state.py --action=status --task=feat/example
python .agents/scripts/validate-artifact.py --file=.agent-work/feat/example/TASK_CONTEXT.md --type=task_context
python .agents/scripts/smoke-test.py
```

The state helper records manually supplied decisions for one orchestrator; it
does not approve tasks or execute agents. Record human approvals only when given.
Catalog sync inventories bounded Nuxt paths; verify symbols and relationships
using graph/source evidence. It does not parse TypeScript ASTs or infer schemas.

The [QA skill](skills/qa-engineer/SKILL.md) and
[workflow optimizer](skills/agentic-workflow-optimizer/SKILL.md) load on demand.
Their discovery depends on the host; each can also be read by its path.
Golden templates under `master-templates/` remain unchanged. PHP helper templates
are retained as alternatives; the generated helpers use Python for both platforms.

No automated app tests, auth, database, Nuxt layers, or dev container are configured.
`npm run build` is a build check. See the [bootstrap report](BOOTSTRAP_REPORT.md)
for verification results and limits.

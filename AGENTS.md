# Repository Guidelines

Skyserver contains a Nuxt 4.7.0 starter and the existing public homelab landing page. Production currently serves static HTML through Nginx.

## Project Structure & Module Organization

- `app/app.vue`: Nuxt entry, currently rendering `NuxtWelcome`.
- `index.html` and `compose.yml`: active static landing and Docker deployment.
- `nuxt.config.ts`: Nuxt configuration; `tsconfig.json` references generated Nuxt configurations.
- `.agents/`: contributor workflows, memory, and Python helpers; preserve `master-templates/`.
- `.agent-work/architecture/readable-nuxt/`: approved, evolving architecture plan.

As features arrive, use standard `app/pages`, `layouts`, `components`, `composables`, and `assets`; server operations belong in `server/`, shared public contracts in `shared/`. Create directories only when used. No application tests or asset directory exist yet.

## Build, Test, and Development Commands

Use Node matching `package.json` engines; Node 24 LTS is recommended.

- `npm ci`: install locked dependencies and generate Nuxt types.
- `npm run dev`: start development at `http://127.0.0.1:3000`.
- `npm run build`: generate the production build.
- `npm run preview`: preview that build locally.
- `npm run generate`: prerender static output when appropriate.
- `python .agents/scripts/smoke-test.py`: test agent helpers; use `python3` on Debian.

## Coding Style & Naming Conventions

Follow `.editorconfig` and `.prettierrc.json`: two spaces, LF, single quotes, and no JavaScript/TypeScript semicolons. VS Code recommends Vue Official, Prettier, and EditorConfig.

Use TypeScript and Vue `script setup`. Read scripts top to bottom: imports/metadata, inputs/state, fetching, computed values, actions, lifecycle effects; then template/styles. Prefer clear local inline logic. Extract meaningful reusable behavior, substantial UI, or security boundaries. Use names like `services`, `search`, and `saveService`; PascalCase components/types and `useX` composables.

The architecture may evolve with demonstrated needs; explain material changes and update guidance.

## Testing Guidelines

No application test framework, coverage threshold, lint script, or typecheck script is configured. Builds and helper tests do not establish application coverage. Proposed future tests use `test/unit`, `test/nuxt`, and `test/e2e`, with descriptive `*.test.ts` or `*.spec.ts` names. Report runtime and visual checks separately.

## Commit & Pull Request Guidelines

Work on `dev`; `main` targets production. History uses imperative summaries, with recent Conventional Commits such as `chore(agents): ...`. Prefer that format. Describe behavior, validation, limitations, and relevant issues; include screenshots for visual changes. Preserve unrelated edits.

## Security & Agent Workflow

Keep secrets server-side; future admin APIs must enforce authorization independently of route guards. Preserve public landing access and deployment contracts. Use graph-first structural discovery, per-path coverage checks, and source fallback for gaps. Read `.agents/memory/INDEX.md` selectively; commit, push, or deploy only within user authorization.

## Workflow Selection Before Implementation

Before implementing a new feature or fixing an issue, assess scope, complexity, and risk. Recommend the best approach with a brief reason, then let the user choose:

- [Feature workflow](.agents/workflows/multiple-agent-workflow.md): substantial features or changes needing architecture, review, and QA.
- [Hotfix workflow](.agents/workflows/hotfix-workflow.md): urgent, focused fixes needing root-cause analysis and targeted verification.
- **Direct change**: small, low-risk features or fixes; make a focused edit and run appropriate checks.

Wait for the user's selection before implementation; read-only investigation may continue. Respect an explicit choice already given for the same task without asking again. Follow the selected workflow's applicable gates; direct changes still require validation and respect existing authorization boundaries.

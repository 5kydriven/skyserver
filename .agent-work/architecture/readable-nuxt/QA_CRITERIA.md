# QA Criteria

TASK_ID: architecture/readable-nuxt

## Plan review

- Compare the proposed ownership map with Nuxt's documented app/server/shared
  boundaries, data fetching, middleware and auto-import behavior.
- Confirm snippets are explicitly illustrative; the sample Service contract and
  admin endpoint must not be described as existing or runtime-tested.
- Check the sample route can be understood by reading dependencies, input, fetch,
  computed result, then template. Avoid wrappers that hide those operations.
- Confirm extraction is justified by reuse, substantive complexity or boundaries;
  inline preference must not move privileged operations into client code.
- Check naming examples against both readability and ambiguity in multi-entity scopes.

## Future behavioral checks

- Render/directly load routes, hydrate, then navigate client-side. Inspect duplicate
  initial requests, browser-only API use, console errors and unintended layout reuse.
- Verify loading, empty, error, success, action-in-progress, failure and retry states.
- Exercise actual protected API URLs while unauthenticated and underprivileged;
  do not rely solely on redirect tests. Test malformed parameters before mutations.
- Confirm state/session data is isolated between independent requests/users and
  personalized endpoints have no accidental cross-user caching.
- Check labels, keyboard/focus behavior, responsive layout and rendered appearance.
- Add meaningful logic/component tests when behavior exists, plus critical browser
  journeys. Mock external services for tests; avoid live homelab side effects.
- Run build/lint/typecheck/test commands only after the tooling is installed and
  report each result independently. Docker configuration validation and local HTTP
  checks do not prove a live Debian deployment works.

## Validation for this planning task

Documentation/artifact validation only. No runtime, visual, security-test, build,
or deployment result is implied by approving the architectural direction.

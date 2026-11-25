# Cloudflare Access implementation

## Implementation Summary

Implement the approved four-hostname Access policy in Cloudflare, preserving
Nextcloud's native login. Prepare a reusable setup and verification runbook in
the repository. No client-side login gate can substitute for the live policy.

## Files to Create

- docs/cloudflare-access.md: exact application matrix, dashboard procedure,
  origin validation, acceptance checks, and recovery guidance.
- .agent-work/feat/cloudflare-access/IMPLEMENTATION_REPORT.md: completed local
  work, live access blockers, and outstanding verification.

## Files to Modify

- README.md: link the setup runbook and distinguish prepared configuration from
  activated protection.
- Workflow state and approved plan status: record existing user approvals.
- No Nuxt or Compose code changes are required by this approved architecture.

## Implementation Order

1. Validate this plan before repository implementation.
2. Probe the four public hostnames without credentials to record present edge
   behavior. Do not equate login redirects with verified origin protection.
3. Prepare exact Cloudflare dashboard settings and verification guidance.
4. Inspect real account applications/policies, login methods, tunnel routes,
   automation consumers, and public origin exposure when access is available.
5. Apply only the approved hostname/email/session settings, preserving unrelated
   policies and Nextcloud. If existing configuration conflicts, report it first.
6. Run real anonymous/allowed/denied/expiry/bypass checks, review, and QA.
7. Request final user verdict only after actual verification is complete.

## External Dependency

No Cloudflare plugin was found. Browser access was retried after architecture
approval and again returned: The browser access host is unavailable.
The task is not complete and no live authentication is claimed.

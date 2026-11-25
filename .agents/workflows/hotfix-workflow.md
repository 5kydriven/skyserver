---
description: Fast-track, token-optimized hotfix state graph workflow for critical bugs, crashes, regressions, and security patches.
---

# Fast-Track Hotfix State Graph Workflow

A streamlined, token-efficient hotfix state machine designed for rapid, surgical remediation of production bugs, regressions, or security issues in **Skyserver**.

---

## 1. Hotfix State Graph Flow

```mermaid
stateDiagram-v2
    [*] --> Node_RootCause: State Init (manage-state.py --action=init --task=hotfix/...)
    
    Node_RootCause --> Node_HotfixImplementer: Slice Context Extracted
    
    Node_HotfixImplementer --> Node_AdversarialDiffCheck: validate-artifact (HOTFIX_PLAN)
    
    Node_AdversarialDiffCheck --> Node_HotfixImplementer: Review FAIL (Zero collateral check)
    Node_AdversarialDiffCheck --> Node_TargetedQA: Review PASS
    
    Node_TargetedQA --> Node_HotfixImplementer: Test FAIL
    Node_TargetedQA --> Gate_EmergencyUserApproval: Test PASS
    
    state Gate_EmergencyUserApproval {
        [*] --> UserEmergencySignoff
    }
    
    Gate_EmergencyUserApproval --> Node_HotfixRelease: Approved
    Gate_EmergencyUserApproval --> Node_HotfixImplementer: Rejected
    
    Node_HotfixRelease --> [*]: State COMPLETED + Git PR
```

---

## 2. State Machine Execution Steps

### Step 1: State Init & Root-Cause Analysis
1. **Initialize State**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=init --task=hotfix/<slug> --complexity=SMALL
   ```
2. **Context Policy**: Read error stack trace / bug description + exact defective file.
3. **Action**: Pinpoint root cause using line slice reads (`view_file` with line range).
4. **Output**: `.agent-work/hotfix/<slug>/HOTFIX_CONTEXT.md`.
5. **Transition**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=transition --task=hotfix/<slug> --to=node_hotfix_implementer
   ```

---

### Step 2: Hotfix Implementation (Surgical Patch)
1. **Context Policy**: Read `STATE.json`, `HOTFIX_CONTEXT.md`, and exact defective file.
2. **Action**:
   - Draft `.agent-work/hotfix/<slug>/HOTFIX_PLAN.md` (exact lines to touch).
   - Apply smallest surgical fix possible (no unrequested refactoring).
   - Review `git diff`.
3. **Output**: `HOTFIX_REPORT.md`.
4. **Transition**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=transition --task=hotfix/<slug> --to=node_adversarial_diff_check
   ```

---

### Step 3: Adversarial Diff Review
1. **Context Policy**: Read `git diff` + `.agents/memory/conventions.md`.
2. **Action**: Verify patch does not cause regressions, introduce concurrency risks, or break tenant isolation.
3. **Output**: `CODE_REVIEW.md` (`CODE_REVIEW_STATUS: PASS | FAIL`).
4. **Conditional Edge**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=set-verdict --task=hotfix/<slug> --target=review --verdict=<PASS|FAIL>
   ```

---

### Step 4: Targeted QA Verification
1. **Context Policy**: Read `git diff` + affected test file.
2. **Action**: Run targeted test command: `npm run build`.
3. **Output**: `QA_REPORT.md` (with short Manual Verification Checklist).
4. **Conditional Edge**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=set-verdict --task=hotfix/<slug> --target=qa --verdict=<PASS|FAIL>
   ```

---

### Step 5: User Emergency Gate
1. **Action**: Present minimal diff and verification steps to user.
2. **PAUSE AND WAIT** for user confirmation (`approved`, `complete`, `ship it`).
3. **Transition**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=transition --task=hotfix/<slug> --to=node_hotfix_release
   ```

---

### Step 6: Hotfix Release
1. **Action**:
   - Append entry to `MEMORY_ARCHIVE.md` and pointer row to `MEMORY.md`.
   - Create hotfix commit: `fix(<scope>): <concise description>`.
   - Create pull request to target base branch (`dev (development), main (production)`).
2. **State Complete**:
   ```bash
   python3 .agents/scripts/manage-state.py --action=transition --task=hotfix/<slug> --to=completed --status=COMPLETED
   ```


## Skyserver execution contract

- Role files live under `.agents/agents/<role>/agent.md`; no custom slash commands or extra orchestration dependencies are installed.
- Check `.agents/CONTEXT_POLICY.md` for graph-first discovery and delegation evidence. SMALL tasks run directly; MEDIUM adds architecture and review; LARGE uses the full pipeline. QA applies to every tier.
- Use `python` on Windows and `python3` on Debian. Python 3.10+ is an agent-helper prerequisite only.
- No app test runner is installed. `npm run build` verifies compilation; add local HTTP/manual checks appropriate to the change and clearly report any unverified behavior.
- The catalog helper inventories files in bounded Nuxt scopes; it is not a TypeScript AST parser or database introspector. Inspect source/graph evidence for signatures and relationships.
- The state helper records decisions for a single orchestrator. It does not obtain human approval, coordinate concurrent writers, or execute agents. Never mark a human gate APPROVED without the user's actual authorization.
- After user approval, record `--action=set-verdict --target=gate_0_scope --verdict=APPROVED`, `gate_1_architecture` when applicable, and `gate_6_final_verdict` before entering release. Do not ask again when that same decision was already explicitly authorized.
- Both review and QA failures escalate on the third failure. Preserve state/history when restarting a task.
- No commit, push, PR, or deployment is implied by completing bootstrap or a local validation check.

#!/usr/bin/env python3
"""Exercise agent helpers in a temporary, isolated repository (Python 3.10+)."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skyserver-agent-smoke-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for relative in ('.agents/scripts', '.agents/master-templates/memory'):
            shutil.copytree(ROOT / relative, self.root / relative)

    def run_helper(self, name, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.root / '.agents/scripts' / name), *args],
            cwd=self.root, capture_output=True, text=True, encoding='utf-8',
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def state(self, task='feat/example'):
        return json.loads((self.root / '.agent-work' / task / 'STATE.json').read_text(encoding='utf-8'))

    def init(self, task='feat/example'):
        self.run_helper('manage-state.py', '--action=init', f'--task={task}', '--complexity=SMALL')

    def verdict(self, target, verdict):
        self.run_helper('manage-state.py', '--action=set-verdict', '--task=feat/example',
                        f'--target={target}', f'--verdict={verdict}')

    def test_existing_state_survives_init(self):
        self.init()
        self.verdict('gate_0_scope', 'APPROVED')
        before = self.state()
        self.init()
        self.assertEqual(before, self.state())

    def test_rejects_escaped_or_absolute_task_paths(self):
        for task in ('../escape', '/tmp/escape', 'C:/escape', 'feat/../../escape'):
            self.run_helper('manage-state.py', '--action=init', f'--task={task}', success=False)
        self.assertFalse((self.root / 'escape').exists())

    def test_unknown_task_status_does_not_create_a_task(self):
        self.run_helper('manage-state.py', '--action=status', '--task=missing', success=False)
        self.assertFalse((self.root / '.agent-work/missing').exists())

    def test_corrupt_state_is_preserved_and_reported(self):
        self.init()
        path = self.root / '.agent-work/feat/example/STATE.json'
        path.write_text('corrupt', encoding='utf-8')
        self.run_helper('manage-state.py', '--action=init', '--task=feat/example', success=False)
        self.assertEqual(path.read_text(encoding='utf-8'), 'corrupt')

    def test_release_requires_qa_and_human_approval(self):
        self.init()
        args = ('--action=transition', '--task=feat/example', '--to=node_5_release_manager')
        self.run_helper('manage-state.py', *args, success=False)
        self.verdict('qa', 'PASS')
        self.run_helper('manage-state.py', *args, success=False)
        self.verdict('gate_6_final_verdict', 'APPROVED')
        self.run_helper('manage-state.py', *args)
        self.assertEqual(self.state()['current_node'], 'node_5_release_manager')

    def test_review_and_qa_escalate_after_three_failures(self):
        self.init()
        for target in ('review', 'qa'):
            for _ in range(3):
                self.verdict(target, 'FAIL')
            self.assertEqual(self.state()['status'], 'CIRCUIT_BREAKER_ESCALATED')
            self.assertEqual(self.state()[f'{target}_cycles'], 3)

    def test_unknown_verdict_is_rejected_without_mutation(self):
        self.init()
        before = self.state()
        self.run_helper('manage-state.py', '--action=set-verdict', '--task=feat/example',
                        '--target=gate_6_final_verdict', '--verdict=PASS', success=False)
        self.assertEqual(before, self.state())

    def test_artifact_validation_accepts_and_rejects_real_inputs(self):
        artifact = self.root / 'TASK_CONTEXT.md'
        artifact.write_text('TASK_ID: feat/example\n## Feature\nSetup\n## Business Goal\nConsistency\n'
                            '## Actors\nDeveloper\n## Requirements\nSetup\n## Constraints\nNo app edits\n', encoding='utf-8')
        self.run_helper('validate-artifact.py', f'--file={artifact}', '--type=task_context')
        artifact.write_text('Unstructured note', encoding='utf-8')
        self.run_helper('validate-artifact.py', f'--file={artifact}', '--type=task_context', success=False)

    def test_catalog_detects_addition_and_removal_without_inventing_classes(self):
        self.run_helper('sync-catalogs.py')
        catalog = self.root / '.agents/memory/catalogs/services.md'
        self.assertIn('No source candidates', catalog.read_text(encoding='utf-8'))
        source = self.root / 'app/composables/useExample.ts'
        source.parent.mkdir(parents=True)
        source.write_text('export const useExample = () => true\n', encoding='utf-8')
        self.run_helper('sync-catalogs.py')
        self.assertIn('app/composables/useExample.ts', catalog.read_text(encoding='utf-8'))
        source.unlink()
        self.run_helper('sync-catalogs.py')
        self.assertNotIn('app/composables/useExample.ts', catalog.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

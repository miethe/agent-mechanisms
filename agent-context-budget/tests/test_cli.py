import json
import importlib.util
import subprocess
import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1] / 'src'


def run(root, *args):
    # Exercise an installed distribution when available; repository-wide tests
    # otherwise run the standalone package directly from its src layout.
    cwd = root if importlib.util.find_spec('agent_context_budget') else SOURCE_ROOT
    return subprocess.run([sys.executable, '-m', 'agent_context_budget', str(root), '--cap', '64', '--root-cap', '64', '--prefix', '32', *args], cwd=cwd, capture_output=True, text=True)


def test_clean_and_truncated_chain(tmp_path):
    (tmp_path / 'AGENTS.md').write_text('required\n')
    nested = tmp_path / 'nested'
    nested.mkdir()
    (nested / 'AGENTS.md').write_text('child\n')
    result = run(tmp_path, '--anchor', 'required', '--json')
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report['chains'][-1]['bytes'] == 15
    (nested / 'AGENTS.md').write_text('x' * 60)
    result = run(tmp_path)
    assert result.returncode == 1 and 'chain 69 bytes exceeds cap' in result.stdout


def test_root_and_anchor_controls(tmp_path):
    (tmp_path / 'AGENTS.md').write_text('x' * 70 + 'required')
    result = run(tmp_path, '--anchor', 'required')
    assert result.returncode == 1
    assert 'root cap' in result.stdout and 'anchor' in result.stdout
    assert run(tmp_path, '--anchor', 'absent').returncode == 1


def test_missing_and_malformed(tmp_path):
    assert run(tmp_path).returncode == 2
    (tmp_path / 'AGENTS.md').write_text('ok')
    baseline = tmp_path / 'baseline.json'
    baseline.write_text('{')
    result = run(tmp_path, '--baseline', str(baseline))
    assert result.returncode == 2 and result.stderr.startswith('error:')
    baseline.write_text('{"total_bytes": 1}')
    result = run(tmp_path, '--baseline', str(baseline), '--json')
    assert json.loads(result.stdout)['delta_bytes'] == 1

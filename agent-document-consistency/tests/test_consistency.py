import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from document_consistency import missing, stale, main

PATTERN = r'^Rule: (?P<fact>.+)$'

def test_missing_and_allow():
    assert missing('Rule: alpha\nRule: beta', 'Rule: alpha', PATTERN) == ['beta']
    assert missing('Rule: alpha\nRule: beta', 'Rule: alpha', PATTERN, ['beta']) == []

def test_stale_reports_lines():
    assert stale('Rule: old\nRule: new', PATTERN, {'new'}) == [(1, 'old')]

def test_cli_detects_drift(tmp_path, capsys):
    a, b = tmp_path / 'a', tmp_path / 'b'
    a.write_text('Rule: alpha'); b.write_text('Rule: beta')
    assert main([str(a), str(b), '--pattern', PATTERN]) == 1
    assert capsys.readouterr().out == 'missing: alpha\n'

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from small_hooks import added_handoffs, unquoted_text, main

def test_reword_and_duplicate():
    old = '[old](handoff-example.md)'
    assert added_handoffs(old, '[new](handoff-example.md)') == []
    assert added_handoffs(old, old + '\n[[handoff-example]]') == ['example']

def test_quoted_content_removed():
    assert unquoted_text('real\n> quoted\n```\ncode\n```\n"words"').strip() == 'real'

def test_cli(tmp_path):
    old, new = tmp_path / 'old', tmp_path / 'new'
    old.write_text(''); new.write_text('[x](handoff-example.md)')
    assert main([str(old), str(new)]) == 1

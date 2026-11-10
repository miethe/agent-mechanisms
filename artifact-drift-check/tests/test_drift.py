import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from artifact_drift import compare, main

def test_missing_sides(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    assert compare(a, b) == ['missing upstream']
    a.write_text('a')
    assert compare(a, b) == ['missing deployment']

def test_nested_and_content(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    a.mkdir(); b.mkdir()
    (a / 'same').write_text('a'); (b / 'same').write_text('b')
    (a / 'up').write_text('x'); (b / 'down').write_text('x')
    assert compare(a, b) == ['only in deployment: down', 'differs: same', 'only in upstream: up']
    (b / 'same').write_text('a'); (a / 'up').unlink(); (b / 'down').unlink()
    assert main([str(a), str(b)]) == 0

def test_type_mismatch(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    a.mkdir(); b.write_text('x')
    assert compare(a, b) == ['type mismatch: .']

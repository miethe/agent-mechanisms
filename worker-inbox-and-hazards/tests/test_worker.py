import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from worker_hazards import send, consume, matching, transition

def test_claim_once(tmp_path):
    send(tmp_path, 'a', 'hello')
    assert consume(tmp_path) == [('a', 'hello')]
    assert consume(tmp_path) == []

def test_active_matching_latest():
    events = [{'key': 'x', 'status': 'active', 'pattern': 'slow'}, {'key': 'x', 'status': 'fixed', 'pattern': 'slow'}, {'key': 'y', 'status': 'active', 'pattern': 'slow'}]
    assert [x['key'] for x in matching(events, 'SLOW task')] == ['y']

def test_validation_requires_distinct_evidence():
    fixed = transition({'key': 'x', 'status': 'active'}, 'fixed', fix_evidence='fix')
    with pytest.raises(ValueError): transition(fixed, 'validated', validation_proof='fix')
    assert transition(fixed, 'validated', validation_proof='check')['status'] == 'validated'
    with pytest.raises(ValueError): transition(fixed, 'archived')

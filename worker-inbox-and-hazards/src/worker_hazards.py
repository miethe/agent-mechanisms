"""Claim local inbox messages and match active hazards against work text."""
import json
import re
from pathlib import Path
import local_maildir


def send(root, key, text):
    return local_maildir.deliver(Path(root), key, json.dumps({'text': text}).encode())


def consume(root):
    rows = []
    for key in local_maildir.list_pending(Path(root)):
        claim = local_maildir.claim(Path(root), key)
        if claim.claimed:
            rows.append((key, json.loads(local_maildir.read(claim.path))['text']))
    return rows


def latest(events):
    return {event['key']: event for event in events}


def matching(events, text):
    return [event for event in latest(events).values() if event['status'] == 'active'
            and event.get('pattern') and re.search(event['pattern'], text, re.I | re.M)]


def transition(event, status, *, fix_evidence=None, validation_proof=None):
    allowed = {'active': {'fixed'}, 'fixed': {'active', 'validated'},
               'validated': {'active', 'archived'}, 'archived': {'active'}}
    if status not in allowed.get(event['status'], set()):
        raise ValueError('invalid transition')
    result = dict(event, status=status)
    if status == 'fixed':
        if not fix_evidence:
            raise ValueError('fix evidence required')
        result.update(fix_evidence=fix_evidence, validation_proof=None)
    if status == 'validated':
        if not validation_proof or validation_proof == event.get('fix_evidence'):
            raise ValueError('independent validation proof required')
        result['validation_proof'] = validation_proof
    return result

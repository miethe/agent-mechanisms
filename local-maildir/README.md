# Local maildir

Experimental filesystem mailbox primitives for delivering and claiming byte messages. Requires Python 3.10 or newer and a filesystem supporting hard links.

Delivery and claim use an advisory mailbox lock; every writer must use this library. Requires POSIX advisory locks and hard links on one local filesystem. The mailbox does not make downstream effects transactional: a crash after claim requires a separate effect ledger. Directory entries are not fsynced, so power-loss durability is not guaranteed.

Run tests with `python -m pytest -q`.

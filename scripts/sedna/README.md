# SEDNA Forensic Tracking

Tracks all operations for reproducibility with automatic sanitization.

## Quick Start

```python
from scripts.sedna import tracker

tracker.track("action_name")
tracker.track("with_files", files=["config.yml"])
tracker.track("with_metadata", gpu_count=2, cuda="12.1")
```

## How It Works

1. **Tracks to two files simultaneously:**
   - `provenance/chain.jsonl` - Real hostnames (gitignored)
   - `provenance/chain_clean.jsonl` - Sanitized (committed)

2. **Auto-sanitizes:**
   - Hostnames → node-001, node-002
   - Usernames → examprep

## Install

```bash
pip install -e .
```

## Test

```bash
python scripts/sedna/test_tracking.py
```

## Verify Files

```python
from scripts.sedna import verifier
verifier.verify_files()  # Checks all tracked files match their hashes
```

## What to Track

- Lab starts/completions
- Configuration changes
- Errors and fixes
- Job submissions
- Any reproducible step
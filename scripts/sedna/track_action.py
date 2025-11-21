#!/usr/bin/env python3
"""Basic action tracking - Phase 1"""

import json
from datetime import datetime
from pathlib import Path

def track_action(action):
    """Log action with timestamp"""
    provenance_dir = Path.cwd() / 'provenance'
    provenance_dir.mkdir(exist_ok=True)
    
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action
    }
    
    chain_file = provenance_dir / 'chain.jsonl'
    with open(chain_file, 'a') as f:
        json.dump(entry, f)
        f.write('\n')
    
    print(f"✓ Tracked: {action}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python track_action.py <action>")
        sys.exit(1)
    
    action = " ".join(sys.argv[1:])
    track_action(action)
#!/usr/bin/env python3
"""Action tracking with context - Phase 2"""

import json
import platform
import getpass
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.sedna import CHAIN_FILE

def track_action(action):
    """Log action with timestamp and context"""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "context": {
            "hostname": platform.node(),
            "user": getpass.getuser(),
            "platform": platform.system(),
            "python": platform.python_version()
        }
    }
    
    with open(CHAIN_FILE, 'a') as f:
        json.dump(entry, f)
        f.write('\n')
    
    print(f"✓ Tracked: {action} [{platform.node()}]")
    return entry

def test_tracking():
    """Test function"""
    result = track_action("test_action")
    assert "timestamp" in result
    assert "action" in result
    assert "context" in result
    assert result["context"]["hostname"] == platform.node()
    print("✓ Tests passed")

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python track_action.py <action>")
        sys.exit(1)
    
    action = " ".join(sys.argv[1:])
    track_action(action)

if __name__ == "__main__":
    if "--test" in sys.argv:
        test_tracking()
    else:
        main()
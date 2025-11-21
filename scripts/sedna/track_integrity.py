#!/usr/bin/env python3
"""Action tracking with file integrity - Phase 3"""

import json
import platform
import getpass
import hashlib
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.sedna import CHAIN_FILE

def calculate_hash(filepath):
    """Calculate SHA256 hash of file"""
    if not Path(filepath).exists():
        return None
    
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def track_action(action, files=None):
    """Log action with context and file hashes"""
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
    
    if files:
        entry["files"] = {}
        for filepath in files:
            hash_val = calculate_hash(filepath)
            if hash_val:
                entry["files"][str(filepath)] = hash_val
    
    with open(CHAIN_FILE, 'a') as f:
        json.dump(entry, f)
        f.write('\n')
    
    print(f"✓ Tracked: {action} [{platform.node()}]")
    if files:
        print(f"  Files hashed: {len(entry.get('files', {}))}")
    return entry

def test_tracking():
    """Test function"""
    # Create test file
    test_file = Path("test.txt")
    test_file.write_text("test content")
    
    result = track_action("test_with_files", [test_file])
    assert "files" in result
    assert str(test_file) in result["files"]
    
    test_file.unlink()
    print("✓ Tests passed")

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python track_integrity.py <action> [file1 file2 ...]")
        sys.exit(1)
    
    action = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else None
    track_action(action, files)

if __name__ == "__main__":
    if "--test" in sys.argv:
        test_tracking()
    else:
        main()
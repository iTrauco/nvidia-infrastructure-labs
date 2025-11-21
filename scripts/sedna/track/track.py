#!/usr/bin/env python3
"""Unified tracking with auto-sanitization"""
import json
import hashlib
import platform
import getpass
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from scripts.sedna import REPO_ROOT
from scripts.sedna.sanitize.sanitize import Sanitizer


class Tracker:
    def __init__(self):
        self.chain_file = REPO_ROOT / "provenance" / "chain.jsonl"
        self.clean_file = REPO_ROOT / "provenance" / "chain_clean.jsonl"
        self.chain_file.parent.mkdir(exist_ok=True)
        self.sanitizer = Sanitizer()
    
    def track(self, action, files=None, **metadata):
        """Track action with optional file hashes"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "host": platform.node(),
            "user": getpass.getuser(),
        }
        
        # Add file hashes
        if files:
            entry["files"] = {}
            for filepath in files:
                hash_val = self._hash_file(filepath)
                if hash_val:
                    entry["files"][str(filepath)] = hash_val
        
        # Add metadata
        if metadata:
            entry.update(metadata)
        
        # Write raw
        with open(self.chain_file, "a") as f:
            json.dump(entry, f)
            f.write("\n")
        
        # Write sanitized
        clean_entry = self.sanitizer.sanitize_entry(entry)
        with open(self.clean_file, "a") as f:
            json.dump(clean_entry, f)
            f.write("\n")
        
        print(f"✓ Tracked: {action}")
        return entry
    
    def _hash_file(self, filepath):
        """SHA256 hash of file"""
        path = Path(filepath)
        if not path.exists():
            return None
        
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()


# Test
if __name__ == "__main__":
    tracker = Tracker()
    tracker.track("test_action", files=["README.md"], test_data="hello")
    print("Check provenance/chain.jsonl and provenance/chain_clean.jsonl")
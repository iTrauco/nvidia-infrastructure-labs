#!/usr/bin/env python3
"""Unified tracking with auto-sanitization"""
import json
import platform
import getpass
from pathlib import Path
from datetime import datetime


class Tracker:
    def __init__(self):
        self.chain_file = Path("provenance/chain.jsonl")
        self.clean_file = Path("provenance/chain_clean.jsonl")
        self.chain_file.parent.mkdir(exist_ok=True)
    
    def track(self, action, **metadata):
        """Track action - writes to both raw and clean chains"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "host": platform.node(),
            "user": getpass.getuser(),
        }
        
        if metadata:
            entry.update(metadata)
        
        # Write raw
        with open(self.chain_file, "a") as f:
            json.dump(entry, f)
            f.write("\n")
        
        # Write sanitized
        clean_entry = self._sanitize(entry)
        with open(self.clean_file, "a") as f:
            json.dump(clean_entry, f)
            f.write("\n")
        
        print(f"✓ Tracked: {action}")
        return entry
    
    def _sanitize(self, entry):
        """Auto-sanitize hostnames and users"""
        clean = entry.copy()
        
        # Map hostnames to generic
        hostname = clean.get("host", "").lower()
        if "w32445" in hostname or "zenon" in hostname:
            clean["host"] = "node-001"
        elif "w52445" in hostname or "gemini" in hostname:
            clean["host"] = "node-002"
        else:
            clean["host"] = "node-003"
        
        # Sanitize username
        clean["user"] = "user"
        
        return clean


# Test it
if __name__ == "__main__":
    tracker = Tracker()
    tracker.track("test_action", test_data="hello")
    print("Check provenance/chain.jsonl and provenance/chain_clean.jsonl")
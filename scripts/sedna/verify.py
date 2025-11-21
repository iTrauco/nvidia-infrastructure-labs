#!/usr/bin/env python3
"""Verify file integrity from chain - Phase 4"""

import json
import hashlib
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

def verify_chain():
    """Verify all files in chain match their hashes"""
    if not CHAIN_FILE.exists():
        print("No chain.jsonl to verify")
        return False
    
    passed = 0
    failed = 0
    missing = 0
    
    with open(CHAIN_FILE, 'r') as f:
        for line_num, line in enumerate(f, 1):
            entry = json.loads(line)
            
            if 'files' not in entry:
                continue
            
            for filepath, expected_hash in entry['files'].items():
                path = Path(filepath)
                
                if not path.exists():
                    print(f"✗ Missing: {filepath}")
                    missing += 1
                    continue
                
                actual_hash = calculate_hash(filepath)
                if actual_hash == expected_hash:
                    passed += 1
                else:
                    print(f"✗ Changed: {filepath}")
                    failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed, {missing} missing")
    return failed == 0 and missing == 0

def main():
    """CLI entry point"""
    success = verify_chain()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
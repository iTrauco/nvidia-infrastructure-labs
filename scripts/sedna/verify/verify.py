#!/usr/bin/env python3
"""File integrity verification"""
import json
import hashlib
from pathlib import Path


class Verifier:
    def __init__(self, chain_file="provenance/chain.jsonl"):
        self.chain_file = Path(chain_file)
    
    def hash_file(self, filepath):
        """Calculate SHA256 hash of file"""
        path = Path(filepath)
        if not path.exists():
            return None
        
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def verify_files(self):
        """Verify all files in chain match their hashes"""
        if not self.chain_file.exists():
            print("No chain file found")
            return False
        
        passed = 0
        failed = 0
        missing = 0
        
        with open(self.chain_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                
                # Skip entries without files
                if "files" not in entry:
                    continue
                
                # Check each file
                for filepath, expected_hash in entry["files"].items():
                    path = Path(filepath)
                    
                    if not path.exists():
                        print(f"✗ Missing: {filepath}")
                        missing += 1
                        continue
                    
                    actual_hash = self.hash_file(filepath)
                    if actual_hash == expected_hash:
                        passed += 1
                    else:
                        print(f"✗ Changed: {filepath}")
                        failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed, {missing} missing")
        return failed == 0 and missing == 0


# Test
if __name__ == "__main__":
    verifier = Verifier()
    
    # Create test file
    test_file = Path("test.txt")
    test_file.write_text("test content")
    
    # Test hashing
    hash_val = verifier.hash_file("test.txt")
    print(f"Hash of test.txt: {hash_val[:16]}...")
    
    # Verify chain
    verifier.verify_files()
    
    # Cleanup
    test_file.unlink()
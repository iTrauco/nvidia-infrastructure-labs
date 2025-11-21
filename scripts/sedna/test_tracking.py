#!/usr/bin/env python3
"""Test SEDNA tracking - shows all usage patterns"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.sedna.track.track import Tracker
from scripts.sedna.verify.verify import Verifier

def test_basic_tracking():
    """Basic action tracking"""
    print("\n=== TEST: Basic Tracking ===")
    tracker = Tracker()
    
    # Simple action
    tracker.track("started_session")
    
    # Action with metadata
    tracker.track("configured_gpu", gpu_count=2, cuda_version="12.1")
    
    # Action with files
    tracker.track("created_config", files=["README.md"])
    
    print("✓ Basic tracking works")

def test_lab_workflow():
    """Example lab workflow tracking"""
    print("\n=== TEST: Lab Workflow ===")
    tracker = Tracker()
    
    # Track a complete lab
    tracker.track("lab_01_slurm_started")
    tracker.track("installed_packages", packages=["slurm", "munge"])
    tracker.track("configured_slurm", files=["configs/slurm.conf"])
    tracker.track("submitted_job", job_id="12345", nodes=2)
    tracker.track("job_completed", runtime_seconds=45.2)
    tracker.track("lab_01_slurm_completed", score=95)
    
    print("✓ Lab workflow tracked")

def test_error_tracking():
    """Track errors and fixes"""
    print("\n=== TEST: Error Tracking ===")
    tracker = Tracker()
    
    tracker.track("error_occurred", 
                  error="CUDA out of memory",
                  script="train.py",
                  batch_size=256)
    
    tracker.track("applied_fix",
                  fix="reduced batch size",
                  new_batch_size=128)
    
    tracker.track("fix_confirmed", success=True)
    
    print("✓ Error tracking works")

def test_verification():
    """Test file verification"""
    print("\n=== TEST: File Verification ===")
    
    # Create test file
    test_file = Path("test_config.yml")
    test_file.write_text("test: data")
    
    # Track it
    tracker = Tracker()
    tracker.track("created_test_file", files=["test_config.yml"])
    
    # Verify
    verifier = Verifier()
    result = verifier.verify_files()
    
    # Clean up
    test_file.unlink()
    
    print(f"✓ Verification tested")

def check_output():
    """Show what was created"""
    print("\n=== OUTPUT CHECK ===")
    repo_root = Path(__file__).parent.parent.parent
    chain_file = repo_root / "provenance" / "chain.jsonl"
    clean_file = repo_root / "provenance" / "chain_clean.jsonl"
    
    if chain_file.exists():
        with open(chain_file) as f:
            lines = f.readlines()
        print(f"Raw chain: {len(lines)} entries")
        print(f"Latest: {lines[-1][:100]}...")
    
    if clean_file.exists():
        with open(clean_file) as f:
            lines = f.readlines()
        print(f"Clean chain: {len(lines)} entries")
        print(f"Latest (sanitized): {lines[-1][:100]}...")

if __name__ == "__main__":
    print("SEDNA TRACKING TESTS")
    print("=" * 50)
    
    test_basic_tracking()
    test_lab_workflow()
    test_error_tracking()
    test_verification()
    check_output()
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETE")
    print("\nUsage in notebooks:")
    print("  from scripts.sedna.track.track import Tracker")
    print("  tracker = Tracker()")
    print("  tracker.track('action', key=value, files=['file.txt'])")
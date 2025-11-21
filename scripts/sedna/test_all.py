#!/usr/bin/env python3
"""Test SEDNA components without polluting real chain"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_all():
    """Test all components using temp chain"""
    # Use temp directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_chain = Path(tmpdir) / 'test_chain.jsonl'
        
        # Mock the chain file for testing
        import scripts.sedna as sedna
        original_chain = sedna.CHAIN_FILE
        sedna.CHAIN_FILE = test_chain
        
        # Test tracking
        from scripts.sedna.track_integrity import track_action
        result = track_action("test_action", ["README.md"])
        assert "files" in result
        print("✓ Tracking works")
        
        # Test verification
        from scripts.sedna.verify import verify_chain
        verify_chain()
        print("✓ Verification works")
        
        # Restore original chain
        sedna.CHAIN_FILE = original_chain
        print("\n✓ All tests passed (no pollution to real chain)")

if __name__ == "__main__":
    test_all()
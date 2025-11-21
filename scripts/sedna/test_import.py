#!/usr/bin/env python3
"""Test module imports"""
import sys
from pathlib import Path

# Test import from parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts import REPO_ROOT
from scripts.sedna import CHAIN_FILE, PROVENANCE_DIR

print(f"✓ REPO_ROOT: {REPO_ROOT}")
print(f"✓ PROVENANCE_DIR: {PROVENANCE_DIR}")
print(f"✓ CHAIN_FILE: {CHAIN_FILE}")
print("✓ All imports working")
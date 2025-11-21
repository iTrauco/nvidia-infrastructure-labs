"""SEDNA - Simple imports"""
from pathlib import Path

# Define here, don't import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROVENANCE_DIR = REPO_ROOT / 'provenance'
CHAIN_FILE = PROVENANCE_DIR / 'chain.jsonl'
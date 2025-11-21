"""SEDNA forensic tracking framework"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROVENANCE_DIR = REPO_ROOT / 'provenance'
CHAIN_FILE = PROVENANCE_DIR / 'chain.jsonl'

# Ensure provenance directory exists
PROVENANCE_DIR.mkdir(exist_ok=True)
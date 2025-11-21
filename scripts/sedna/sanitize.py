#!/usr/bin/env python3
"""Sanitize chain.jsonl for public commits"""

import json
import sys
import os
import socket
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.sedna import CHAIN_FILE, PROVENANCE_DIR

def get_node_id():
    """Map current hostname to clean node ID"""
    hostname = socket.gethostname().lower()
    
    # Map hostnames to clean IDs
    if 'w32445' in hostname or 'zenon' in hostname:
        return 'node-001'
    elif 'w52445' in hostname or 'gemini' in hostname:
        return 'node-002'
    elif 'control' in hostname:
        return 'control'
    else:
        # Unknown host - use first 4 chars of hostname
        return f"node-{hostname[:4]}"

def load_env():
    env_file = Path.cwd() / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def sanitize_chain():
    """Remove sensitive data from chain"""
    load_env()
    
    if not CHAIN_FILE.exists():
        print("No chain.jsonl to sanitize")
        return
    
    clean_file = PROVENANCE_DIR / 'chain_clean.jsonl'
    
    # Use env override or map from hostname
    sanitize_host = os.getenv('SANITIZE_HOSTNAME') or get_node_id()
    sanitize_user = os.getenv('SANITIZE_USER', 'examprep')
    
    with open(CHAIN_FILE, 'r') as f_in, open(clean_file, 'w') as f_out:
        for line in f_in:
            entry = json.loads(line)
            
            # Sanitize context if present
            if 'context' in entry:
                entry['context']['hostname'] = sanitize_host
                entry['context']['user'] = sanitize_user
            
            # Files field passes through unchanged (already just hashes)
            
            json.dump(entry, f_out)
            f_out.write('\n')
    
    print(f"✓ Sanitized: {clean_file} (as {sanitize_host})")
    return clean_file

if __name__ == "__main__":
    sanitize_chain()
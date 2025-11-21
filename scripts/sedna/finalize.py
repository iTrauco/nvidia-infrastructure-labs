#!/usr/bin/env python3
"""Create forensic package - Phase 5"""

import json
import hashlib
import tarfile
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.sedna import CHAIN_FILE, PROVENANCE_DIR, REPO_ROOT

def create_manifest():
    """Generate SHA256 manifest of all project files"""
    manifest_dir = PROVENANCE_DIR / '.integrity'
    manifest_dir.mkdir(exist_ok=True)
    manifest_file = manifest_dir / 'manifest.sha256'
    
    files_to_hash = []
    for pattern in ['**/*.py', '**/*.yml', '**/*.md', '**/*.yaml']:
        files_to_hash.extend(REPO_ROOT.glob(pattern))
    
    # Exclude .git and provenance
    files_to_hash = [f for f in files_to_hash 
                     if '.git' not in f.parts 
                     and 'provenance' not in f.parts]
    
    with open(manifest_file, 'w') as f:
        for filepath in sorted(files_to_hash):
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as fh:
                for chunk in iter(lambda: fh.read(4096), b''):
                    sha256.update(chunk)
            rel_path = filepath.relative_to(REPO_ROOT)
            f.write(f"{sha256.hexdigest()}  {rel_path}\n")
    
    print(f"✓ Manifest created: {len(files_to_hash)} files")
    return manifest_file

def sign_manifest(manifest_file):
    """Create signature of manifest"""
    sig_file = manifest_file.parent / 'manifest.sig'
    sha256 = hashlib.sha256()
    with open(manifest_file, 'rb') as f:
        sha256.update(f.read())
    sig_file.write_text(sha256.hexdigest())
    print(f"✓ Signature: {sha256.hexdigest()[:32]}...")
    return sig_file

def create_archive():
    """Create forensic archive"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    archive_name = PROVENANCE_DIR / f'forensic_{timestamp}.tar.gz'
    
    with tarfile.open(archive_name, 'w:gz') as tar:
        # Add sanitized chain
        clean_chain = PROVENANCE_DIR / 'chain_clean.jsonl'
        if clean_chain.exists():
            tar.add(clean_chain, arcname='chain_clean.jsonl')
        
        # Add manifest
        manifest = PROVENANCE_DIR / '.integrity' / 'manifest.sha256'
        if manifest.exists():
            tar.add(manifest, arcname='manifest.sha256')
        
        # Add signature
        sig = PROVENANCE_DIR / '.integrity' / 'manifest.sig'
        if sig.exists():
            tar.add(sig, arcname='manifest.sig')
    
    print(f"✓ Archive: {archive_name}")
    return archive_name

def finalize():
    """Create complete forensic package"""
    print("🔐 Creating forensic package...")
    
    # Run sanitize first
    from scripts.sedna.sanitize import sanitize_chain
    sanitize_chain()
    
    # Create manifest
    manifest = create_manifest()
    
    # Sign it
    sign_manifest(manifest)
    
    # Create archive
    archive = create_archive()
    
    print("\n📦 Forensic package ready for:")
    print("  • Exam documentation")
    print("  • Reproducibility verification")
    print("  • Archival storage")

if __name__ == "__main__":
    finalize()
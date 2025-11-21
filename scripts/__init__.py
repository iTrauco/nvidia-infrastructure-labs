"""Scripts package root"""
from pathlib import Path

def get_repo_root():
    """Find repo root - never fails"""
    current = Path(__file__).resolve().parent.parent
    
    # Try 1: Look for .git
    if (current / '.git').exists():
        return current
    
    # Try 2: Look for provenance dir
    if (current / 'provenance').exists():
        return current
    
    # Fallback
    return current

REPO_ROOT = get_repo_root()

__all__ = ['REPO_ROOT']
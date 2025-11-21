"""SEDNA - Forensic tracking for NVIDIA infrastructure"""
from pathlib import Path

# For package use
try:
    from sedna.track.track import Tracker
    from sedna.verify.verify import Verifier
    from sedna.sanitize.sanitize import Sanitizer
except ImportError:
    # For local development
    from scripts.sedna.track.track import Tracker
    from scripts.sedna.verify.verify import Verifier
    from scripts.sedna.sanitize.sanitize import Sanitizer

# Global instances
tracker = Tracker()
verifier = Verifier()

__version__ = "0.1.0"
__all__ = ["tracker", "verifier", "Tracker", "Verifier", "Sanitizer"]
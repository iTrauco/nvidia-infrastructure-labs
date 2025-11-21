#!/usr/bin/env python3
"""CLI entry points for SEDNA"""
import sys
import argparse
from sedna.track.track import Tracker
from sedna.verify.verify import Verifier

def track_cli():
    """Command-line tracking"""
    parser = argparse.ArgumentParser(description="Track action to chain")
    parser.add_argument("action", help="Action to track")
    parser.add_argument("--files", nargs="*", help="Files to hash")
    parser.add_argument("--metadata", nargs="*", help="key=value pairs")
    
    args = parser.parse_args()
    
    # Parse metadata
    metadata = {}
    if args.metadata:
        for item in args.metadata:
            if "=" in item:
                key, value = item.split("=", 1)
                metadata[key] = value
    
    tracker = Tracker()
    tracker.track(args.action, files=args.files, **metadata)

def verify_cli():
    """Command-line verification"""
    verifier = Verifier()
    success = verifier.verify_files()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    track_cli()
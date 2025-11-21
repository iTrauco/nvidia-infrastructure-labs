#!/usr/bin/env python3
"""Setup for SEDNA tracking package"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README if it exists
readme = Path("README.md")
long_description = readme.read_text() if readme.exists() else ""

setup(
    name="sedna-tracker",
    version="0.1.0",
    description="Forensic tracking for NVIDIA infrastructure operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/itrauco/nvidia-infrastructure-labs",
    
    # Find packages under scripts/
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    
    # No dependencies - pure Python
    install_requires=[],
    
    # Python 3.8+ for pathlib
    python_requires=">=3.8",
    
    # CLI scripts
    entry_points={
        "console_scripts": [
            "sedna-track=sedna.cli:track_cli",
            "sedna-verify=sedna.cli:verify_cli",
            "sedna-test=sedna.test_tracking:main",
        ],
    },
    
    # Include data files
    package_data={
        "sedna": ["*.json", "*.jsonl"],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
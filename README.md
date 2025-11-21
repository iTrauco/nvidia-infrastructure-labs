# NVIDIA NCP-AIO Professional Exam Preparation Lab

Hands-on lab environment for NVIDIA Certified Professional - AI Operations exam preparation with reproducibility-first approach and SEDNA forensic framework.

## Core Principle: Complete Reproducibility

Every operation tracked, every environment captured, every result verifiable. Using conda environments and forensic provenance to ensure complete reproducibility across all nodes and configurations.

## Project Status: Clean Rebuild

Building forensic chain of custody through incremental implementation of SEDNA framework components alongside exam preparation labs.

## Implementation Approach

**Note:** Due to enterprise SLAs required for select NVIDIA services (Base Command Manager, Fleet Command, Run:ai, UFM Enterprise), this lab implements open-source alternatives that directly apply the patterns, architecture, and design standards of NVIDIA's enterprise suite. All tools used are freely available without licensing requirements.

## Quick Start

```bash
git clone https://github.com/itrauco/nvidia-infrastructure-labs.git
cd nvidia-infrastructure-labs

# Create reproducible conda environment
conda env create -f environment.yml
conda activate nvidia-labs

# Initialize tracking and setup
./setup.sh
```

## Reproducibility Framework

- **Conda Environments**: Exact package versions across all nodes
- **SEDNA Tracking**: Complete audit trail of all operations
- **Config Versioning**: All configurations in git
- **State Snapshots**: Hourly exports of environment state
- **Verification**: Cryptographic validation of all components

## Structure

- `notebooks/` - Interactive labs for each exam topic
- `ansible/` - Automated cluster deployment
- `configs/` - Service configurations  
- `docs/` - Architecture and exam mapping
- `provenance/` - Audit trail (chain.jsonl)
- `scripts/sedna/` - Tracking framework

## Topics Covered

- Slurm job scheduling
- Kubernetes GPU management
- NGC container workflows
- GPU monitoring with DCGM
- Distributed training
- Storage and networking concepts
- Troubleshooting

## Requirements

- Ubuntu 24.04 LTS
- NVIDIA GPU(s)
- Docker + NVIDIA Container Toolkit
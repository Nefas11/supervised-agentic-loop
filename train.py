#!/usr/bin/env python3
"""Dummy training script for SAL testing."""
import sys
import json

# Simulate a metric value (SAL parses with --parser val_bpb)
metric = 0.85  # Start value
print(f"Validation BPB: {metric}")
sys.exit(0)

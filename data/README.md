# Data Directory

This directory contains scripts and data for generating and managing SIEM alert datasets.

## Files

- `generate_sample_data.py`: Python script to generate 150 realistic security alerts
- `siem_alerts_raw.json`: Generated raw alert data (created by running the script)
- `ground_truth_labels.csv`: Human-labeled severity and threat classification (created by running the script)

## Usage

```bash
# Generate fresh dataset
python data/generate_sample_data.py

# This will create:
# - data/siem_alerts_raw.json (150 alerts)
# - data/ground_truth_labels.csv (answer key)

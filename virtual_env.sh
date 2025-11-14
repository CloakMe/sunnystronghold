#!/bin/bash

# Create virtual environment named virt_sun if it doesn't exist
if [ ! -d "sunnystronghold" ]; then
  python3.8 -m venv sunnystronghold
fi

# Activate the virtual environment
source sunnystronghold/bin/activate

# Install guidedlda package
pip install guidedlda

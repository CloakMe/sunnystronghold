#!/bin/bash

# Create virtual environment named virt_sun if it doesn't exist
if [ ! -d "virtual_python37" ]; then
  python3.7 -m venv virtual_python37
  python3.6 -m venv virtual_python36
fi

# Activate the virtual environment
source virtual_python37/bin/activate

# Download get-pip.py
curl -O https://bootstrap.pypa.io/pip/3.7/get-pip.py
curl -O https://bootstrap.pypa.io/pip/3.6/get-pip.py
# Run get-pip.py with your venv's python
python virtual_python37/bin/python3.7 get-pip.py
./virtual_python36/bin/python3.6 get-pip.py

# Install guidedlda package
./virtual_python37/bin/pip install guidedlda

cd virtual_python36/bin
python3.6 -m pip install guidedlda

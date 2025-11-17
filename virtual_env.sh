#!/bin/bash

# Create virtual environment named virt_sun if it doesn't exist
if [ ! -d "virtual_python37" ]; then
  python3.7 -m venv virtual_python37
  python3.6 -m venv virtual_python36
  python3.6 -m venv --without-pip virtual_python36
fi

# Activate the virtual environment
source virtual_python37/bin/activate
source virtual_python36/bin/activate

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

install guidedlda:
sudo apt-get install build-essential python3-dev cython3 libssl-dev libbz2-dev libsqlite3-dev libffi-dev libncurses5-dev libreadline-dev tk-dev liblzma-dev libgdbm-dev libncursesw5-dev

create symbolic link for cython3 (also check installation path if true)
which cython3
sudo ln -s /usr/bin/cython3 /usr/local/bin/cython

git clone https://github.com/vi3k6i5/GuidedLDA.git
cd GuidedLDA

Edit setup.cfg to remove or comment out deprecated lines, especially the pre-hook.sdist_pre_hook option under [sdist].

sudo chmod 775 build_dist.sh
edit build_dist to use python3 instead of python

sudo ./build_dist.sh
sudo pip install -e . --break-system-packages

python3.11

Try importing GuidedLDA:

python
import guidedlda
import numpy as np

model = guidedlda.GuidedLDA(n_topics=5, n_iter=10, random_state=7)
print(model)

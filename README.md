# CARLA Playground: Hack the Road

This repository provides a guide for running CARLA on Ubuntu 22.xx, covering setup, dependencies, and quick launch instructions. CARLA, developed by the CVC group at the Universitat Autònoma de Barcelona (UAB), is a flexible open-source simulator for autonomous driving research. This guide builds on their work and aims to make CARLA accessible for experimentation and learning.

---

## Quick Launch

To quickly launch CARLA with the RaceTrack map in server mode at 30 FPS, run the following:

```sh
./CarlaUE4.sh /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=30
```

For detailed options and advanced configurations, refer to the [official CARLA documentation](http://carla.readthedocs.io).

---

## Ubuntu 22.xx Setup Guide

This guide assumes a non-fresh install of Ubuntu 22.xx. It is designed to set up the necessary environment for running CARLA effectively. If you spot any errors or omissions, feel free to submit a pull request.

### Step 1: Install Python 3.6.15

CARLA requires Python 3.6.x, which is not the default on Ubuntu 22.xx. Begin by updating your system and installing essential libraries:

```sh
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
    libgdbm-dev libnss3-dev libedit-dev libc6-dev \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev \
    libsdl1.2-dev libsmpeg-dev libportmidi-dev ffmpeg libswscale-dev \
    libavformat-dev libavcodec-dev libfreetype6-dev \
    libatlas-base-dev gfortran
```

Next, download and compile Python 3.6.15:

```sh
cd /opt
sudo curl -O https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz
sudo tar -xzf Python-3.6.15.tgz
cd Python-3.6.15/
sudo ./configure --enable-optimizations
sudo make altinstall
```

Verify the installation:

```sh
python3.6 -V
# Output: Python 3.6.15
```

### Step 2: Install pip for Python 3.6

Install `pip` for Python 3.6:

```sh
python3.6 -m ensurepip --default-pip
which pip3.6
pip3.6 -V
```

### Step 3: Create a Virtual Environment

Set up a workspace and a virtual environment for CARLA:

```sh
cd $HOME/
mkdir -p workspace
cd workspace
python3.6 -m venv .venv
```

Activate the virtual environment:

```sh
source .venv/bin/activate
```

### Step 4: Install CARLA Dependencies

Install the required Python packages for CARLA. Installing them in the order shown is important to avoid dependency conflicts:

```sh
pip install --upgrade pip setuptools wheel
pip install pyyaml jinja2 typeguard
pip install scipy==1.5.4
pip install numpy==1.14.5
pip install matplotlib==2.2.2
pip install pillow==3.1.2
pip install pygame==1.9.4
pip install future==0.16.0
pip install protobuf==3.6.0
```

---

## Acknowledgments

This guide and much of the underlying work in this repository are based on the CARLA simulator, developed by the [CVC group at the Universitat Autònoma de Barcelona (UAB)](https://www.uab.cat). The flexibility and open-source nature of CARLA have made it a cornerstone for research in autonomous driving and simulation.

For more details about CARLA and its development, visit the [official CARLA GitHub repository](https://github.com/carla-simulator/carla). 

---

## Contribute

This guide is a work in progress. If you encounter issues or have suggestions, contributions are welcome via pull requests. Let’s make CARLA accessible to everyone—on and off the road. 🚗

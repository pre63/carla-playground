# CARLA Playground: Hack the Road

Welcome to the CARLA Playground. Here's how to get it running and take it for a spin.

## Quick Launch

```sh
./CarlaUE4.sh /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=30
```

For the nitty-gritty details and extra options, check out the [online documentation](http://carla.readthedocs.io).

## Ubuntu 22.xx Setup Guide

Started from a non-fresh install? No worries, this guide has you covered. Found a mistake? Drop a PR!

### Step 1: Install Python 3.6.15

First, update your system and get all the essentials:

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

Download and compile Python 3.6.15:

```sh
cd /opt
sudo curl -O https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz
sudo tar -xzf Python-3.6.15.tgz
cd Python-3.6.15/
sudo ./configure --enable-optimizations
sudo make altinstall
```

Check if the installation was successful:

```sh
python3.6 -V
# Should output: Python 3.6.15
```

### Step 2: Install pip

Get `pip` up and running:

```sh
python3.6 -m ensurepip --default-pip
which pip3.6
pip3.6 -V
```

### Step 3: Create a Virtual Environment

Set up a workspace and a virtual environment:

```sh
cd $HOME/
mkdir -p workspace
cd workspace
python3.6 -m venv .venv
```

### Step 4: Install Dependencies

Install necessary Python packages. One at a time, it matters.

```sh
cd $HOME/workspace

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

You’re all set! Enjoy the ride with CARLA. If you hit any bumps, remember, PRs are welcome!
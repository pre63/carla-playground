# CARLA Simulator

Thanks for downloading CARLA!

Execute "CarlaUE4.sh" to launch CARLA.

For more details and running options please refer to our online documentation

http://carla.readthedocs.io

# Ubuntu 22.xx

I dind't start with a fresh install so feel free to PR the mistakes you find.

## Install Python 3.6.15

```sh
sudo apt-get update

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev  curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
    libgdbm-dev libnss3-dev libedit-dev libc6-dev

sudo apt-get install -y libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev \
    libsdl1.2-dev libsmpeg-dev libportmidi-dev ffmpeg libswscale-dev \
    libavformat-dev libavcodec-dev libfreetype6-dev

sudo apt-get install -y  libatlas-base-dev gfortran

cd /opt

sudo curl -0 https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz

sudo tar -xzf Python-3.6.15.tgz

cd Python-3.6.15/

sudo ./configure --enable-optimizations

sudo make altinstall
```

Might exit with erros but check if it works before abandoning.

To check the installed version, execute the command:

```sh
python3.6 -V
```

```sh
> Python 3.6.15
```

## Install pip

```
python -m ensurepip --default-pip
which pip3.6
pip3.6 -V
```

## Ceate a virtual environment

```sh

cd $HOME/
mkdir workspace
cd workspace
python3.6 -m venv .venv
```

## Install deps
Got to do it one at a time... Becuase reasons.

`scipy` will not install see minimise implementation

```
cd $HOME/workspace

pip install pyyaml jinja2 typeguard
pip install --upgrade pip setuptools wheel

pip install numpy==1.14.5
pip install matplotlib==2.2.2
pip install pillow==3.1.2
pip install pygame==1.9.4
pip install future==0.16.0
pip install protobuf==3.6.0

```

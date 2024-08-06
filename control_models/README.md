# Self-Driving Cars

This simulation  is a simple implmentation of a linear and longitudinal model for a self-driving car. The simulation runs in a 2D space and the car is controlled by a PID controller. We use CARLA as the simulation environment. It's base on the [Self-Driving Cars Specialization](https://www.coursera.org/specializations/self-driving-cars) from Coursera.

# Setup

```
python3.6 -m venv .venv
source .venv/bin/activate
```

### Running the simulation

```
set PYTHONPATH (pwd)
./CarlaUE4.sh /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=30
python simulation.py
```
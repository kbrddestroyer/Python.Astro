# Python.Astro

![Simulation window](https://github.com/user-attachments/assets/0b35ba48-3540-47d1-bdcb-a590008a3eff)


## Repo health

> status checks will be here

## About this repo

Astro is python-based mathematical simulation of Newtonian gravity between multiple physical objects in 2D space.

Overview:

## Some math background 

It's pretty obvious, that gravitational pull between two objects is equal to:

![Gravitational Force](https://latex.codecogs.com/svg.latex?F%20=%20G%20%5Cfrac%7Bm_1%20m_2%7D%7Br%5E2%7D)

## Code logic

- Universe - singleton class, that's capable of most calculations and kinetics acceleration
- Kinetic - object that has physical parameters, such as mass, acceleration and velocity. It's also used in visualization, converting own parameters to display self in pygame window.
- Universe Utils file specifies global mathematical operations, such as distance calculating, force between two kinetics and universe-to-display convertations
- Simulation - controls tickrate and Universe update rate. Parameters can be tweaked to achieve different simulation speed.

Universe yses leapfrog integration for kinetic position and velocity calculations.

> Graphics and visuals will be added soon

## Installing

1. Fetch the dependencies. `pip install -e .`

## Usage

### 1. Tweaking start parameters

There's single `unifile.py` module, that contains start parameters of the simulation. Kinetics can be added here along with start velocity/acceleration/force appliance. 

Simulation parameters can be changed in `simulation.py` module.

Most physical parameters, such as unit size, can be tweaked inside universe utils module.

Asteriod spawn params can be changed inside kinetic module in `AsteroidSpawner` and `Asteroid` classes

### 2. Running

Simply run `python src/main.py`

## Testing

> Currently there's no tests. This must be changed asap


> This file will change soon. 

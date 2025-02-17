# Python.Astro

![Simulation window](https://github.com/user-attachments/assets/0b35ba48-3540-47d1-bdcb-a590008a3eff)


## Repo health

> status checks will be here

## About this repo

Astro is python-based mathematical simulation of Newtonian gravity between multiple physical objects in 2D space.

Overview:

## Some basic physics 

If we have N objects interacting in Newtonian space, gravitational pull for each object will be:

$$
\begin{align}
\mod{\overrightarrow{F_{ab}}} = G \frac{m M}{r^2} \\
\overrightarrow{F} = \sum^N_{i=1}\overrightarrow{F_i} \\
\end{align}
$$

The magnitude of $ \overrightarrow{F} $ vector will remain the same for each different object, but not it's direction. Now we can calculate the acceleration, velocity and shift by ∆t time.

$$
\begin{align}
\vec{a} = \frac{\vec{f}}{m} \\
\vec{v} = \vec{a} \Delta t \\
\end{align}
$$

## Integration algorithms 

Now when we have current velocity, we need the way of shift precise calculation. The most obvious way is to use Euler's integration, but then we'll face an issue, that this way is highly dependent on simulation's tickrate (∆t). Fortunately, there's plenty of methods. We'll use **leapfrog** algorithm.

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

# Python.Astro

![Simulation window](https://github.com/user-attachments/assets/0b35ba48-3540-47d1-bdcb-a590008a3eff)


## Repo health

[![Pylint](https://github.com/kbrddestroyer/Python.Astro/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/kbrddestroyer/Python.Astro/actions/workflows/pylint.yml)
[![Pytest](https://github.com/kbrddestroyer/Python.Astro/actions/workflows/pytest.yml/badge.svg?branch=main&event=push)](https://github.com/kbrddestroyer/Python.Astro/actions/workflows/pytest.yml)

## About this repo

Astro is python-based mathematical simulation of Newtonian gravity between multiple physical objects in 2D space.

> Please, open an issue if you see any errors in this repository.

## Some basic physics 

If we have N objects interacting in Newtonian space, gravitational pull for each object will be:

$$
\begin{align}
\mod{\overrightarrow{F_{ab}}} = G \frac{m M}{r^2} \\
\overrightarrow{F} = \sum^N_{i=1}\overrightarrow{F_i} \\
\end{align}
$$

The magnitude of $` \overrightarrow{F} `$ vector will remain the same for each different object, but not it's direction. Now we can calculate the acceleration, velocity and shift by ∆t time.

$$
\begin{align}
\vec{a} = \frac{\vec{f}}{m} \\
\vec{v} = \vec{a} \Delta t \\
\end{align}
$$

## Integration algorithms 

$$
\begin{align}
\Delta r = \vec v_1\Delta t_1 + \vec v_2\Delta t_2 + ... + \vec v_n\Delta t_n \\
\Delta r = \lim_{\Delta t \to 0} \sum^n_{i=1}v_i\Delta t_i \\
\Delta r = \int^{t_1}_{t_0} v(t)dt \\
\end{align}
$$

Now when we have current velocity, we need the way of shift precise calculation. 
The most obvious way is to use Euler's integration, but then we'll face an issue, that this way is highly dependent on 
simulation's refresh rate and ∆t between ticks. Fortunately, there's plenty of methods we can use instead.
I've used [leapfrog algorithm](https://en.wikipedia.org/wiki/Leapfrog_integration).

## Code logic

- Universe - singleton class, that's capable of most calculations and kinetics acceleration
- Kinetic - object that has physical parameters, such as mass, acceleration and velocity. It's also used in visualization, converting own parameters to display self in pygame window. Also it can break into fragments if the external forces are much greater than it's own gravity.
- Spawner can be added into unifile. Spawnables must contain no parameters in constructor.
- Universe Utils file specifies global mathematical operations, such as distance calculating, force between two kinetics and universe-to-display convertations
- Simulation - controls tick rate and Universe update rate. Parameters can be tweaked to achieve different simulation speed.

## Installing

1. Fetch the dependencies. `pip install -e .`
2. Optionally install Jupiter and Notebook with `pip install jupiter notebook`

## Usage

### 1. Tweaking start parameters

There's single `unifile.py` module, that contains start parameters of the simulation. Kinetics can be added here along with start velocity/acceleration/force appliance. 

Simulation parameters can be changed in `simulation.py` module.

Most physical parameters, such as unit size, can be tweaked inside universe utils module.

Asteriod spawn params can be changed inside kinetic module in `AsteroidSpawner` and `Asteroid` classes

> Global configuration is in config module

### 2. Running

Simply run `python src/main.py` to launch your `unifile.py` simulation

### 3. Testing

Jupiter notebook contains some basic computing and graphic plotting. It shows orbit parameters, speed and energy drift of a kinetic object.

Codestyle checks are performed with `pylint`, simply run `pylint src`

### 4. Jupiter graphics

- Launch Jupiter with `jupiter notebook` command
- Open `README.ipynb` file
- Launch the notebook

class Configuration:
    # region SIMULATION

    TIME_UNIT = 1.0
    TIME_MULTIPLIER = 3

    DELTA_TIME = TIME_UNIT * TIME_MULTIPLIER

    # endregion

    # region UNIVERSE

    G_CONST = 6.6743e-11
    UNIT_SIZE = 2e6

    # endregion

    # region ASTEROIDS

    MASS = (1e9, 1.e12)
    POSITION = (10, 1600, 10, 1000)
    BASE_VELOCITY_MUL = 1e6
    DENSITY = 5.6e12

    # endregion
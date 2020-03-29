COLORS = {
    0: (0, 0, 255),  # blue                   HEALTHY
    1: (255, 0, 0),  # red                    INFECTED
    2: (255, 255, 0),  # yellow               ASYMPOMATIC
    3: (255, 255, 255),  # white              IMMUNE
    4: (0, 255, 0),  # green
    5: (0, 255, 255),  # cyan
    6: (255, 0, 255),  # magenta
    7: (0, 0, 0),  # black
    8: (128, 128, 128) # gray
}



RADIUS = 3
MAX_VEL = 3
MAX_ACCEL = 0.5

START_WIDTH = 800
START_HEIGHT = 600
START_PERSONS = 100

START_PERCEPTION = 35
START_STEERING = 0.2

START_RAD_I = 20
START_RATE_I = 0.2

RANDOM_ACCEL_COE = 3 # higher is less random
ACCEL_DECAY = 0.8    # lower is more decay

SHOW_VELOCITY = 0


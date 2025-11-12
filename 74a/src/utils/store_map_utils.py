import random
from utils.q_map_utils import q_comparison


def get_next_direction(status):
    next_direction = random.randint(0, 7)
    is_random_walk = random.random() < status.epsilon

    if is_random_walk == False:
        next_direction = q_comparison(status, next_direction)
    return next_direction


def get_next_x_y(status, direction):
    next_x = 0
    next_y = 0

    if direction == 0:
        next_x = status.position.x - 1
        next_y = status.position.y
    elif direction == 1:
        next_x = status.position.x - 1
        next_y = status.position.y + 1
    elif direction == 2:
        next_x = status.position.x
        next_y = status.position.y + 1
    elif direction == 3:
        next_x = status.position.x + 1
        next_y = status.position.y + 1
    elif direction == 4:
        next_x = status.position.x + 1
        next_y = status.position.y
    elif direction == 5:
        next_x = status.position.x + 1
        next_y = status.position.y - 1
    elif direction == 6:
        next_x = status.position.x
        next_y = status.position.y - 1
    elif direction == 7:
        next_x = status.position.x - 1
        next_y = status.position.y - 1
    return next_x, next_y

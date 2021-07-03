import arcade
import math
import random
import threading
from abc import ABC, abstractmethod
from arcade import sprite

# These are Global constants to use throughout the game
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_FIRE_RATE = .5

SHOOTER_RADIUS = 5
SHOOTER_SPEED = 5
SHOOTER_SIZE = 50
START_LIVES = 3

TARGET_SPAWN_RATE = 1
TARGET_RADIUS = 13
TARGET_SPEED = -2
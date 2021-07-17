# From constants import all
from game.constants import *
# From director import InstructionView
from game.director import InstructionView
# Imports arcade library
import arcade
# Imports pygame library
import pygame

# Play music
pygame.init()
music = pygame.mixer.music.load("sound/background.wav")
pygame.mixer.music.play(-1)

# Creates the game and starts it
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Street Shooter")
start_view = InstructionView()
window.show_view(start_view)
arcade.run()


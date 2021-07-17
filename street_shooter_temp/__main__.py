# From contastants import all
from game.constants import *
# From director import InstructionView
from game.director import InstructionView
# Imports arcade library
import arcade

# Creates the game and starts it
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Street Shooter")
start_view = InstructionView()
window.show_view(start_view)
arcade.run()

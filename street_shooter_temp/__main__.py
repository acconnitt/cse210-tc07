from game.constants import *
from game.screens import *
import arcade

# Creates the game and starts it
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Street Shooter")
start_view = InstructionView()
window.show_view(start_view)
arcade.run()

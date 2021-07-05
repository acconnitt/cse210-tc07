
from game import constants
from game.shooter import Shooter
from game.flying_object import Flying_Object
from game.bullet import Bullet
from game.target import Target
import arcade

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

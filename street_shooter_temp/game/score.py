# Imports arcade library
import arcade
# From constants import all
from game.constants import *


class Score():
    """Keep track of score"""

    def __init__(self):
        # Starts at zero
        self.score = 0

    def draw(self):
        # Display score
        arcade.draw_text(
            f"Score: {self.score}", 15, SCREEN_HEIGHT * .95, arcade.color.DUTCH_WHITE, 20)

    def update_score(self):
        # Update score
        self.score += 1

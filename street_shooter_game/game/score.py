import arcade
from game.constants import *

class Score():
    def __init__(self):
        self.score = 0

    def draw(self):
        arcade.draw_text(f"Score: {self.score}", 15, SCREEN_HEIGHT* .95, arcade.color.DUTCH_WHITE, 20)

    def update_score(self):
        self.score += 1
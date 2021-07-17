# Imports arcade library
import arcade
# Imports random library
import random
# From arcade library import color
from arcade.color import RED
# From contastants import all
from game.constants import *
# Import flying_object imports Flying_Object
from game.flying_object import Flying_Object


class Target(Flying_Object):
    """A target that falls down from the top of the screen. The target loses a
    life each time it is hit by a bullet, and the target is removed when lives = 0."""

    def __init__(self):
        """Target characteristics. """
        super().__init__()
        self.radius = TARGET_RADIUS
        self.velocity.dy = TARGET_SPEED
        self.velocity.dx = 0
        self.lives = 1

    def draw(self):
        """draws the targets"""
        img = "assets/crate.png"
        texture = arcade.load_texture(img)

        width = texture.width // 6
        height = texture.height // 6
        alpha = 255

        # Target angles
        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(
            x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide(self, score, shooter):
        """Updates amount of lives when target is hit.
        Kills target when lives are gone."""
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            self.alive = False

    def generate_lives(self, score, shooter):
        """Assigns a random amount of lives for each new target that is created. 
        Lives can increase as the score increases"""
        self.lives = random.randint(1, (score.score * shooter.damage // 4 + 1))


class RedTarget(Target):
    """A target that, when hit, adds a life to the shooter."""

    def __init__(self):
        super().__init__()

    def draw(self):

        img = "assets/crate-red.png"
        texture = arcade.load_texture(img)

        width = texture.width // 6
        height = texture.height // 6
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(
            x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide(self, score, shooter):
        """target is hit and loses a life"""
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            if shooter.lives < MAX_LIVES:
                """shooter gets more power to damage when it destroys target"""
                shooter.lives += 1
            self.alive = False


class PurpleTarget(Target):

    """A target that, when hit, gives the shooter power to do more damage."""

    def __init__(self):
        super().__init__()

    def draw(self):
        img = "assets/crate-blue.png"
        texture = arcade.load_texture(img)

        width = texture.width // 6
        height = texture.height // 6
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(
            x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide(self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            """shooter gets more power to damage when it destroys target"""
            shooter.damage += 1
            self.alive = False


class GreenTarget(Target):
    """A target that, when hit, makes the shooter shoot faster."""

    def __init__(self):
        super().__init__()

    def draw(self):
        img = "assets/crate-green.png"
        texture = arcade.load_texture(img)

        width = texture.width // 6
        height = texture.height // 6
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(
            x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide(self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            if shooter.fire_rate > MAX_FIRE_RATE:
                """increase rate of shooting"""
                shooter.fire_rate = shooter.fire_rate / 1.1
            self.alive = False

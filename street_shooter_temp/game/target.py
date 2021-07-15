import arcade
import random

from arcade.color import RED
from game.constants import *
from game.flying_object import Flying_Object

class Target(Flying_Object):

    def __init__(self):
        super().__init__()
        self.radius = TARGET_RADIUS
        self.velocity.dy = TARGET_SPEED
        self.velocity.dx = 0
        self.lives = 1

    def draw(self):
        """ """
        
        img = "assets/crate.png"
        texture = arcade.load_texture(img)
        
        width = texture.width // 6
        height = texture.height // 6
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide (self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            self.alive = False

    def generate_lives(self, score, shooter):
        self.lives = random.randint(1, (score.score * shooter.damage + 1))

class RedTarget(Target):

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

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide (self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            if shooter.lives < MAX_LIVES:
                shooter.lives += 1
            self.alive = False

class BlueTarget(Target):

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

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide (self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            shooter.damage += 1
            self.alive = False
            
class GreenTarget(Target):

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

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        arcade.draw_text(str(self.lives),
                         self.center.x, self.center.y, arcade.color.WHITE, 20, width=100, align="center", anchor_x="center", anchor_y="center")

    def collide (self, score, shooter):
        self.lives -= shooter.damage
        if self.lives <= 0:
            score.update_score()
            if shooter.fire_rate > MAX_FIRE_RATE:
                shooter.fire_rate = shooter.fire_rate / 1.1
            self.alive = False
            

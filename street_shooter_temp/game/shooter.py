import arcade
from game.constants import *
from game.flying_object import Flying_Object


class Shooter(Flying_Object):
    """ """

    def __init__(self):
        super().__init__()
        
        self.radius = SHOOTER_RADIUS
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = 0 + SHOOTER_SIZE
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.fire_rate = BULLET_FIRE_RATE
        self.lives = START_LIVES

    def move_right(self):
        if self.center.x < SCREEN_WIDTH - SHOOTER_SIZE / 2:
            self.velocity.dx = 1 * SHOOTER_SPEED
        else:
            self.center.x = SCREEN_WIDTH - SHOOTER_SIZE / 2

    def move_left(self):
        if self.center.x > 0 + SHOOTER_SIZE / 2:
            self.velocity.dx = -1 * SHOOTER_SPEED
        else:
            self.center.x = 0 + SHOOTER_SIZE / 2

    def collide(self):
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
  
    def draw(self):
        """ """

        img = "assets/alive_shooter.png"
        texture = arcade.load_texture(img)
        img_hit = "assets/dead_shooter.png"
        texture2 = arcade.load_texture(img_hit)

        width = texture.width / 8
        height = texture.height / 8
        alpha = 255
        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_text(f"Lives: {self.lives}", 15, SCREEN_HEIGHT*.9, arcade.color.RED, 20)
        if self.alive:
            arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

        else:
            arcade.draw_texture_rectangle(x + 10, y+5, 50, 50, texture2, angle, alpha)


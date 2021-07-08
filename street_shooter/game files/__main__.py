import arcade
import math
import random
import threading
from abc import ABC, abstractmethod

from arcade import sprite
from pyglet.libs.win32.constants import WHITEONBLACK

# These are Global constants to use throughout the game
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_FIRE_RATE = .5

SHOOTER_RADIUS = 40
SHOOTER_SPEED = 5
SHOOTER_SIZE = 50
START_LIVES = 3

TARGET_SPAWN_RATE = 1
TARGET_RADIUS = 13
TARGET_SPEED = -2




"""-------------------------In-Game Object Classes----------------------------------"""


class Point():
    """Stores a x and y coordinate."""
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        


class Velocity():
    """Stores a vertical and horizontal velocity"""  
    def __init__(self):
        self.dx = 1
        self.dy = 1
        


class Flying_Object():
    """Creates an object with a center point, velocity, and radius. Also stores a variable that tells if it should remain on the
       board after being hit, or when to remove an object when it is offscreen."""
    def __init__(self):    
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 1.0
        self.alive = True
        self.angle = 0
        self.speed = 0
        
    def advance(self):
        """Changes object location by adding velocity to the Point Coordinates"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy 
        
    def is_off_screen(self, screen_width, screen_height, radius):
        """Determines if object off screen"""
        if (self.center.x > screen_width + radius):
            self.center.x = 0 - radius
        
        if (self.center.x < 0 - radius):
            self.center.x = screen_width + radius


        if (self.center.y > screen_height + radius):
            self.center.y = 0 - radius
            
        if (self.center.y < 0 - radius):
            self.center.y = screen_height + radius

    def collide (self):
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
       
                
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def collide(self):
        pass


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
            self.alive =False


 

  
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


class Score():
    def __init__(self):
        self.score = 0

    def draw(self):
        arcade.draw_text(f"Score: {self.score}", 15, SCREEN_HEIGHT* .95, arcade.color.DUTCH_WHITE, 20)

    def update_score(self):
        self.score += 1



    
            
        
              

"""-------PowerUps---------"""



"""----------Bullets-------------"""
        
class Bullet(Flying_Object):
    """Standard Bullet that fires from the ship location, and can only collide with asteroids. Is removed after
       a set distance. """
    
    def __init__(self):
        super().__init__()
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.velocity.dy = BULLET_SPEED
        self.velocity.dx = 0
        
    def draw(self, shooter):
        """draws the bullet sprite. """
        img = "assets/laserBlue01.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90
        

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        

class Target(Flying_Object):

    def __init__(self):
        super().__init__()
        self.radius=  TARGET_RADIUS
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


    def collide (self, score):
        self.lives -= 1
        if self.lives <= 0:
            score.update_score()
            self.alive = False

    def generate_lives(self, score):
        self.lives = random.randint(1, score.score // 2 + 1)
    
    

"""
------------------------------------------------------
-------------------------------------------------------
-------------Actual Game Object-----------------------
-------------------------------------------------------
------------------------------------------------------
"""
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        self.shooter = Shooter()
        self.targets = []
        self.score = Score()
        self.load_targets()
        
        
        

        self.held_keys = set()
        self.bullets = []
        self.load_magazine()



        # TODO: declare anything here you need the game class to track
       
        arcade.set_background_color(arcade.color.CADET_GREY)
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        # TODO: draw each object
        
        
        for bullet in self.bullets:
            bullet.draw(self.shooter)
        

        for target in self.targets:
            target.draw()

        self.shooter.draw()
        self.score.draw()



    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        #self.check_keys()
        
        #self.check_off_screen()
        
        self.cleanup_zombies()
        self.check_collisions()

        # TODO: Tell everything to advance or move forward one step in time
        self.shooter.advance()

        for bullet in self.bullets:
            if bullet.center.y > SCREEN_HEIGHT:
                bullet.alive = False
            bullet.advance()

        for target in self.targets:
            if target.center.y < 0:
               target.alive = False
            target.advance()


        
            
        
        

        
            
        self.check_keys()
        
    def check_off_screen(self):
        """Checks to see if an object is offscreen, and wraps the value of
            the object"""

            
        self.shooter.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT, self.shooter.radius * 2)
        
    
                            
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.shooter.move_left()
        

        if arcade.key.RIGHT in self.held_keys:
            self.shooter.move_right()

        if arcade.key.UP in self.held_keys:
            pass
        else:
            pass
            

        if arcade.key.DOWN in self.held_keys:
            pass
        else:
            pass

    def load_magazine(self):
        if self.shooter.alive:
            bullet = Bullet()
            bullet.center.x = self.shooter.center.x + 6
            bullet.center.y = SHOOTER_SIZE + BULLET_RADIUS *1.5
            self.bullets.append(bullet)
            t = threading.Timer(self.shooter.fire_rate, self.load_magazine)
            t.start()


    def load_targets(self):
        crate_wall = random.randint (1,5)
        
        if crate_wall != 1:
            target = Target()
            target.generate_lives(self.score)
            target.center.x =  random.randint(0, SCREEN_WIDTH)
            target.center.y = SCREEN_HEIGHT + target.radius

            self.targets.append(target)
            t = threading.Timer(TARGET_SPAWN_RATE, self.load_targets)
            t.start()

        else:
            target_location = 45
            for _ in range(6):
                target = Target()
                target.generate_lives(self.score)
                target.center.x = target_location
                target.center.y = SCREEN_HEIGHT + target.radius
                self.targets.append(target) 
                target_location += 90  
            t = threading.Timer(TARGET_SPAWN_RATE, self.load_targets)
            t.start()

        


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.shooter.alive:
            self.held_keys.add(key)

            

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            self.shooter.velocity.dx = 0
            
            
    def cleanup_zombies(self):
        """
        Removes any dead bullets, powerups, or asteroids from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets: 
            if not target.alive: 
                self.targets.remove(target)


    def check_collisions(self):
        """Contains logic of collisions."""
        
        for target in self.targets:  
            if self.shooter.alive and target.alive:
                too_close = self.shooter.radius + target.radius

                if (abs(self.shooter.center.x - target.center.x) < too_close and abs(self.shooter.center.y - target.center.y) < too_close):
                    self.shooter.collide()
                    target.alive = False
                    
        
        for bullet in self.bullets:
            for target in self.targets:
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        target.collide(self.score)
                        bullet.alive = False
                        
                
                



# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

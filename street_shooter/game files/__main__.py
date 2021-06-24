
import arcade
import math
import random
import threading
from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_FIRE_RATE = .5


SHOOTER_SPEED = 5
SHOOTER_SIZE = 50





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
        
        self.radius = 1
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = 0 + SHOOTER_SIZE
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.fire_rate = BULLET_FIRE_RATE

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

 

  
    def draw(self):
        """ """
        
        img = "W10/alive_shooter.png"
        texture = arcade.load_texture(img)
        img_hit = "w10/dead_shooter.png"
        texture2 = arcade.load_texture(img_hit)

        width = texture.width / 8
        height = texture.height / 8
        alpha = 255
        x = self.center.x
        y = self.center.y
        angle = self.angle + 90
        

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        '''if self.hit:
            arcade.draw_texture_rectangle(x + 10, y+5, 50, 50, texture2, angle, alpha)'''
            
        
              

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
        img = "W10/laserBlue01.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height
        alpha = 255

        x = self.center.x
        y = self.center.y
        angle = self.angle + 90
        

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        



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
        self.shooter.draw()
        for bullet in self.bullets:
            bullet.draw(self.shooter)
        
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        #self.check_keys()
        
        #self.check_off_screen()
        
        self.cleanup_zombies()
        #self.check_collisions()

        # TODO: Tell everything to advance or move forward one step in time
        self.shooter.advance()

        for bullet in self.bullets:
            if bullet.center.y > SCREEN_HEIGHT:
                bullet.alive = False
            bullet.advance()

       
        

        
            
        self.check_keys()
        
    def check_off_screen(self):
        """Checks to see if an object is offscreen, and wraps the value of
            the object"""

            
        self.shooter.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT, self.shooter.radius * 2)
        
    def check_collisions(self):
        """Contains logic of collisions.

           Asteroids collide with the ship and bullets
           Bullets collide only with asteroids
           The ship collides with bullets, asteroids, and powerups
           Powerups collide only with the ship."""
        
        for asteroid in self.asteroids:  
            if self.ship.alive and asteroid.alive:
                too_close = self.ship.radius + asteroid.radius

                if (abs(self.ship.center.x - asteroid.center.x) < too_close and abs(self.ship.center.y - asteroid.center.y) < too_close):
                    if self.ship.radius > 0:
                        self.ship.collide(self.shields)
                        asteroid.collide(self.asteroids)
                    
        
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        asteroid.collide(self.asteroids)
                
                        bullet.alive = False
                        
                        
        for powerup in self.powerups:
            if self.ship.alive and powerup.alive:
                too_close = SHIP_RADIUS + powerup.radius

                if (abs(self.ship.center.x - powerup.center.x) < too_close and abs(self.ship.center.y - powerup.center.y) < too_close):
                    if SHIP_RADIUS > 0:
                        powerup.collide(self.ship, self.shields)
                            
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
        bullet = Bullet()
        bullet.center.x = self.shooter.center.x + 6
        bullet.center.y = SHOOTER_SIZE + BULLET_RADIUS *1.5
        self.bullets.append(bullet)
        t = threading.Timer(self.shooter.fire_rate, self.load_magazine)
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
                
                



# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

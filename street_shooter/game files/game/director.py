from game import constants
from game.shooter import Shooter
from game.flying_object import Flying_Object
from game.bullet import Bullet
from game.target import Target
import arcade



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
        self.load_targets()
        self.held_keys = set()
        self.bullets = []
        self.load_magazine()

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
        

        for target in self.targets:
            target.draw()


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
        bullet = Bullet()
        bullet.center.x = self.shooter.center.x + 6
        bullet.center.y = SHOOTER_SIZE + BULLET_RADIUS *1.5
        self.bullets.append(bullet)
        t = threading.Timer(self.shooter.fire_rate, self.load_magazine)
        t.start()


    def load_targets(self):
        crate_wall = random.randint (1,5)
        
        if crate_wall != 1:
            target = Target();
            target.center.x =  random.randint(0, SCREEN_WIDTH)
            target.center.y = SCREEN_HEIGHT + target.radius

            self.targets.append(target)
            t = threading.Timer(TARGET_SPAWN_RATE, self.load_targets)
            t.start()

        else:
            target_location = 45
            for _ in range(6):
                target = Target()
                
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
                    target.collide()
                    
        
        for bullet in self.bullets:
            for target in self.targets:
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        target.collide()
                        bullet.alive = False
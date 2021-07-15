import arcade
import random
import threading
from game.shooter import Shooter
from game.score import Score
from game.constants import *
from game.target import Target, RedTarget, BlueTarget, GreenTarget
from game.bullet import Bullet


class InstructionView(arcade.View):
    """ View to show instructions """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CADET_GREY)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.window.set_mouse_visible(True)
        arcade.draw_text("Street Shooter", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=60, anchor_x="center")
        arcade.draw_text("Use the left and right arrow keys to move.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click to start!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-125,
                         arcade.color.WHITE, font_size=25, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Game()
        self.window.show_view(game_view)

class GameOverView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.CADET_GREY)

    def on_draw(self):
        """ Draw this view """
        img_hit = "assets/dead_shooter.png"
        texture = arcade.load_texture(img_hit)
        alpha = 255
        angle = 90

        arcade.start_render()
        self.window.set_mouse_visible(True)
        arcade.draw_text("Game Over!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED, font_size=60, anchor_x="center")
        arcade.draw_text("Click to play again!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-50,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5, 100, 100, texture, angle, alpha)
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        instr_view = InstructionView()
        self.window.show_view(instr_view)


class Game(arcade.View):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()
        arcade.set_background_color(arcade.color.CADET_GREY)
        self.window.set_mouse_visible(False)
        self.shooter = Shooter()
        self.targets = []
        self.score = Score()
        self.load_targets()
        self.held_keys = set()
        self.bullets = []
        self.load_magazine()

        # TODO: declare anything here you need the game class to track
       
        
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

        if self.shooter.alive == False:
            gameOver = GameOverView()
            self.window.show_view(gameOver)

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
            
    def create_target(self):
        selection = random.randint(1, 100)
        if selection < 80:
            target = Target()
        elif selection < 88:
            target = RedTarget()    
        elif selection < 95:
            target = BlueTarget()
        else:
            target = GreenTarget()

        target.generate_lives(self.score, self.shooter)
        target.center.x =  random.randint(0, SCREEN_WIDTH)
        target.center.y = SCREEN_HEIGHT + target.radius
        return target

    def load_targets(self):
        crate_wall = random.randint (1,11)
        
        if crate_wall != 1:
            target = self.create_target()
            self.targets.append(target)
            t = threading.Timer(TARGET_SPAWN_RATE, self.load_targets)
            t.start()

        else:
            target_location = 45
            for _ in range(6):
                target = self.create_target()
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
                        target.collide(self.score, self.shooter)
                        bullet.alive = False

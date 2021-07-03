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
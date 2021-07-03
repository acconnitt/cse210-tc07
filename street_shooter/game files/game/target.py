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


    def collide (self):
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
    
    
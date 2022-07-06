import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    def __init__(self,ai_game,width=0,height=0):
        """Initialize the ship and set its starting position."""
        super().__init__()
       
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image and get its rect
        # self.image = pg.image.load('image\ship3 (1).bmp')
        self.image = pg.image.load('image\ship211.bmp') 
        if not (width and height) == 0:
            self.resize_ship(1,width,height)
        self.image.set_colorkey((0, 0, 0))
        self.rect  = self.image.get_rect()
        

    
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
 
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
    
        
        
    def update(self):
        """Update the ship's position based on the movement flag."""
        # if self.moving_right: #old
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.x += 1
            self.x +=  self.settings.ship_speed
        # if self.moving_left:4 #old
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x
        
        

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image,self.rect)
    

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    def resize_ship(self,num=0,height=60,width=60):
        if num == 1:
            self.image = pg.transform.smoothscale(self.image, (width,height)) 
        elif num == 0:
            self.image = pg.image.load('image\ship211.bmp')
            self.image.set_colorkey((0, 0, 0))
            self.rect  = self.image.get_rect()


import pygame

from Constants import *
from helpers import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image, flip = None):
        super(Platform, self).__init__()
        self.image = load_image(image)
        if flip:
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])
        # Create mask
        self.mask = pygame.Mask((20, 10))
        self.mask.fill() # This totally works
        
        self.rect = pygame.Rect(x, y, 20, 10)

    def draw(self, screen):
        self.image.set_colorkey(BLACK)
        screen.blit(self.image, self.rect)

    def move(self, player = None):
        pass # Don't do anything!

class MovingPlatform(Platform):
    def __init__(self, x, y, image, xspeed, yspeed, xbounds, ybounds, pause = 0, flip = None):
        """
        Pause is in milliseconds.
        """
        super(MovingPlatform, self).__init__(x, y, image, flip)
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.xbounds = xbounds
        self.ybounds = ybounds
        if self.xbounds[0] > self.xbounds[1]:
            self.xbounds = (self.xbounds[1], self.xbounds[0])
        if self.ybounds[0] > self.ybounds[1]:
            self.ybounds = (self.ybounds[1], self.ybounds[0])
        self.pause = pause
        self.xlast = pygame.time.get_ticks() - self.pause
        self.ylast = pygame.time.get_ticks() - self.pause
        self.xmove = True
        self.ymove = True

    def move(self, player = None):
        if (pygame.time.get_ticks() - self.xlast) > self.pause:
            self.xmove = True
            self.rect[0] += self.xspeed
            if player:
                player.rect[0] += self.xspeed * 1.5
        if (pygame.time.get_ticks() - self.ylast) > self.pause:
            self.ymove = True
            self.rect[1] += self.yspeed
            if player:
                player.rect[1] += self.yspeed * 1.5
        if (self.rect[0] < self.xbounds[0] or self.rect[0] > self.xbounds[1]) and self.xmove:
            self.xspeed *= -1
            self.rect[0] += self.xspeed
            if player:
                player.rect[0] += self.xspeed * 1.5
            self.xmove = False
            self.xlast = pygame.time.get_ticks()
        if (self.rect[1] < self.ybounds[0] or self.rect[1] > self.ybounds[1]) and self.ymove:           
            self.yspeed *= -1
            self.rect[1] += self.yspeed
            if player:
                player.rect[1] += self.yspeed * 1.5
            self.ymove = False
            self.ylast = pygame.time.get_ticks()
            
class MovablePlatform(Platform):
    def __init__(self, x, y, image, keyID = None, unlockImage = None, flip = None):
        super(MovablePlatform, self).__init__(x, y, image, flip)
        self.x = x
        self.y = y

        self.keyID = keyID
        self.unlockImage = unlockImage
        self.originImage = self.image

    def move(self, player = None):
        if player:
            if self.keyID in player.keys:
                self.image = load_image(self.unlockImage) # It's unlocked!
            else:
                self.image = self.originImage
        if abs(self.rect[0] - self.x) > 1:
            self.rect[0] += (self.x - self.rect[0]) / 2.0
        else:
            self.rect[0] = self.x
        if abs(self.rect[1] - self.y) > 1:
            self.rect[1] += (self.y - self.rect[1]) / 2.0
        else:
            self.rect[1] = self.y

class Key(Platform): # I know a key isn't really a platform, but this works in terms of abstraction.
    def __init__(self, x, y, image, keyID):
        super(Key, self).__init__(x, y, image)

        self.hide = False
        self.keyID = keyID

    def draw(self, screen):
        self.image.set_colorkey(BLACK)
        if not self.hide:
            screen.blit(self.image, self.rect)

class Button(Platform):
    def __init__(self, x, y, upImage, downImage, keyID):
        super(Button, self).__init__(x, y, upImage)

        self.upImage = upImage
        self.downImage = downImage

        self.up = True

        self.keyID = keyID

class Door(Platform): # Takes you to the Next Level!
    def __init__(self, x, y, lockImage, unlockImage, levelID, keyID = None):
        super(Door, self).__init__(x, y, lockImage)

        self.lockImage = lockImage
        self.unlockImage = unlockImage

        self.locked = True

        # Recreate the rect and mask because it's a different size
        self.mask = pygame.Mask((40, 80))
        self.mask.fill()
        
        self.rect = pygame.Rect(x, y, 40, 80)

        self.levelID = levelID
        self.keyID = keyID

    def move(self, player):
        if (not self.keyID) or (self.keyID in player.keys):
            self.image = load_image(self.unlockImage)
            self.locked = False
        else:
            self.image = load_image(self.lockImage)
            self.locked = True

    def draw(self, screen):
        self.image.set_colorkey(BLACK)
        screen.blit(self.image, self.rect)
            
class Box(Platform):
    def __init__(self, x, y, image):
        super(Box, self).__init__(x, y, image)
        
        self.mask = pygame.Mask((20, 20))
        self.mask.fill()

        self.rect = pygame.Rect(x, y, 20, 20)

        self.x = x
        self.y = y

        self.mv = 0
        self.vel = 0

    def move(self, player = None):
        if self.rect[1] > 500 + SIZE or self.rect[1] < 0 or self.rect[0] < 0 - SIZE or self.rect[0] > 500 + SIZE:
            self.rect[0] = self.x
            self.rect[1] = self.y
            self.vel = 0
            self.mv = 0
        self.rect[1] -= self.vel
        self.rect[0] += self.mv


# An enemy IS a platform. That's all it is! The only reason this class exists is for abstraction purposes.
# (And to change the mask size.)
class Enemy(Platform):
    def __init__(self, x, y, image):
        super(Enemy, self).__init__(x, y, image)

        self.mask = pygame.Mask((10, 20))
        self.mask.fill()

        self.rect = pygame.Rect(x, y, 10, 20)
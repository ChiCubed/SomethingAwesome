import pygame

from Level import Level
from Constants import *
from Platform import *
from helpers import *

class Player(pygame.sprite.Sprite):
    """
    This class controls the player.
    """
    def __init__(self):
        super(Player, self).__init__()
        self.images = []
        self.images.append(load_image('Sprite/idle.png'))
        self.images.append(load_image('Sprite/jump.png'))
        self.images.append(load_image('Sprite/jog.png'))
        self.image = self.images[IDLE]

        self.rect = pygame.Rect(0, 0, SIZE, SIZE)

        # Create mask
        self.mask = self.create_mask()

        # Create key set
        self.keys = set()

        # Create levels
        self.levels = []
        for i in range(NUM_LEVELS):
            self.levels.append(Level([], [], None))

        # Create levelID
        self.levelID = 0

        # Create rect
        # self.rect = self.mask.get_bounding_rects()[0].unionall(self.mask.get_bounding_rects())

        # self.x = 0
        # self.y = 0
        
        self.onGround = False

    def create_mask(self):
        temp = pygame.Surface((SIZE, SIZE)).convert()
        temp.set_colorkey(BLACK)
        temp.fill(BLACK)
        temp.blit(self.image, (0, 0))
        temp.set_alpha(255)
        return pygame.mask.from_surface(temp)

    def update(self, image, direction, movestate = -1):
        """
        Image contains the image number (defined by constants)
        Direction contains the direction the player is facing (LEFT or RIGHT)
        Movestate is optional and contains the frame the player is currently moving in.
        """
        self.image = self.images[image]
        
        if movestate != -1:
            self.image = pygame.Surface((64, 64))
            self.image.blit(self.images[image], (0, 0), (SIZE * movestate, 0, 64, 64))

        if direction == LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = self.create_mask()

        self.image.set_colorkey(BLACK)
        
        # x = self.rect[0]
        # y = self.rect[1]
        # self.rect = self.mask.get_bounding_rects()[0]
        # self.rect[0] = x
        # self.rect[1] = y

    def move(self, x, y):
        self.rect[0] += x
        self.rect[1] += y
        # self.x += x
        # self.y += y

    def draw(self, screen):
        # Fill the screen!
        # screen.fill(BLACK)
        screen.blit(self.levels[self.levelID].background, pygame.Rect(0, 0, 500, 500))
        screen.blit(self.image, self.rect) # pygame.Rect(self.x, self.y, SIZE, SIZE))
        
        # Draw the bounding rect!
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        
        # Draw the mask!
        # pygame.draw.polygon(screen, (255, 255, 255), self.mask.outline(), 1)
        
        # Tick that clock!
        pygame.time.Clock().tick(FPS)

    def collide(self, moving, jumping, direction, velocity, objects, second = False):
        collisions = []

        boxes = [] # Stores boxes for button collisions

        for p in objects:
            if isinstance(p, Box):
                boxes.append(p)
                didCollide = False
                for o in objects: # Get box collisions
                    if isinstance(o, Button): # If it's a button
                        if pygame.sprite.collide_mask(p, o):
                            didCollide = True
                            p.vel = 0
                            p.rect[1] = o.rect[1] - 14
                    elif isinstance(o, MovablePlatform) and o.keyID in self.keys:
                        if pygame.sprite.collide_mask(p, o):
                            didCollide = True
                            if p.mv > 0:
                                o.rect.left = p.rect.right
                            elif p.mv < 0:
                                o.rect.right = p.rect.left
                            elif p.vel > 0:
                                o.rect.bottom = p.rect.top
                            elif p.vel <= 0:
                                o.rect.top = p.rect.bottom
                            else:
                                # Impossible!
                                pass
                    elif isinstance(o, Platform) and not o == p:
                        if pygame.sprite.collide_mask(p, o):
                            didCollide = True
                            if p.vel <= 0:
                                p.rect.bottom = o.rect.top
                                p.vel = 0
                            elif p.vel > 0:
                                p.rect.top = o.rect.bottom
                                p.vel = 0
                            elif p.mv >= 0:
                                p.rect.right = o.rect.left
                            elif p.mv < 0:
                                p.rect.left = o.rect.right
                if not didCollide:
                    if p.vel > -30:
                        p.vel -= 1
                if p.mv != 0:
                    x = p.mv / abs(p.mv)
                    p.mv = abs(p.mv)
                    p.mv /= 2
                    p.mv *= x
            
        
        anyCollisions = False
        for p in objects:
            if pygame.sprite.collide_mask(self, p):
                anyCollisions = True
                collisions.append(p)
                if isinstance(p, Box):
                    # Like a MovablePlatform, but not springy.
                    if direction == RIGHT and moving:
                        p.mv = 10
                    elif direction == LEFT and moving:
                        p.mv = -10
                    elif velocity > 0:
                        p.rect.bottom = self.rect.top
                        p.vel = velocity
                    elif velocity <= 0:
                        p.rect.top = self.rect.bottom
                        p.vel = velocity
                        self.onGround = True
                    else:
                        # Impossible!
                        pass
                elif isinstance(p, Button):
                    p.up = False
                    p.image = load_image(p.downImage)
                    if p.keyID not in self.keys:
                        self.keys.add(p.keyID)
                elif isinstance(p, Enemy):
                    # You died :'(
                    self.reset(objects)
                elif isinstance(p, Key):
                    p.hide = True
                    self.keys.add(p.keyID)
                elif isinstance(p, Door):
                    if p.keyID in self.keys and not p.locked:
                        self.level(p.levelID, objects)
                elif isinstance(p, MovablePlatform):
                    if not p.keyID or p.keyID in self.keys:
                        if direction == RIGHT and moving:
                            p.rect.left = self.rect.right
                        elif direction == LEFT and moving:
                            p.rect.right = self.rect.left
                        elif velocity > 0:
                            p.rect.bottom = self.rect.top
                            velocity = 0
                        elif velocity <= 0:
                            p.rect.top = self.rect.bottom
                            self.onGround = True
                        else:
                            # Impossible!
                            pass
                    else:
                        # Pretend it's a regular platform
                        if velocity > 0:
                            self.rect.top = p.rect.bottom
                            velocity = 0
                        elif velocity <= 0:
                            self.rect.bottom = p.rect.top
                            self.onGround = True
                            velocity = 0
                        elif direction == RIGHT and moving:
                            self.rect.right = p.rect.left
                            moving = False
                        elif direction == LEFT and moving:
                            self.rect.left = p.rect.right
                            moving = False
                        else:
                            # Impossible!
                            pass                                         
                elif isinstance(p, Platform):
                    if velocity > 0:
                        self.rect.top = p.rect.bottom
                        velocity = 0
                    elif velocity <= 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        velocity = 0
                    elif direction == RIGHT and moving:
                        self.rect.right = p.rect.left
                        moving = False
                    elif direction == LEFT and moving:
                        self.rect.left = p.rect.right
                        moving = False
                    else:
                        # Impossible!
                        pass
                else:
                    pass # U banana
            else:
                if isinstance(p, Button):
                    p.up = True
                    p.image = load_image(p.upImage)
                    if p.keyID in self.keys:
                        self.keys.remove(p.keyID)
                    for o in boxes: # Button collisions!
                        if pygame.sprite.collide_mask(p, o):
                            p.up = False
                            p.image = load_image(p.downImage)
                            if p.keyID not in self.keys:
                                self.keys.add(p.keyID)
                            break
        if self.rect[1] > 500 + SIZE or self.rect[1] < 0 or self.rect[0] < 0 - SIZE or self.rect[0] > 500 + SIZE:
            self.reset(objects)
            moving = False
            jumping = False
            direction = RIGHT
        if not anyCollisions and not second:
            self.onGround = False
        return [moving, jumping, direction, velocity, collisions]

    def reset(self, objects):
        self.rect[0] = 0
        self.rect[1] = 0
        self.keys = set()
        for obj in objects:
            if isinstance(obj, Key):
                obj.hide = False
            elif isinstance(obj, Box):
                obj.rect[0] = obj.x
                obj.rect[1] = obj.y
                obj.vel = 0
                obj.mv = 0

    def level(self, levelID, objects):
        # Go to level levelID
        self.levelID = levelID
        
        # Always safe to reset
        self.reset(objects)

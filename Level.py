import pygame

from Platform import *

class Level(object):
    def __init__(self, platforms, keys, door):
        self.platforms = platforms
        self.keys = keys
        self.door = door

    def levelFromArray(self, level, background, levelID):
        """
        Level is a 50 tall by 25 wide array.
        Components of Level:
        [-1]        Empty
        [0 - 4]     Door
        [5 - 9]     Platform
        [10 - 14]   Moving Platform - Start and End points
        [15 - 19]   Movable Platform - Number is KeyID + 14
        [20 - 24]   Key - Number is KeyID + 19
        [25 - 29]   Enemy - Number is type
        [30 - 34]   Button - Number is KeyID + 29
        [35 - 39]   Box
        """
        # Store start and end points of moving platforms
        movingStart = [None, None, None, None, None]
        movingEnd   = [None, None, None, None, None]

        # Clear the current level
        self.platforms = []
        self.keys = []
        self.door = None

        self.background = background

        # Iterate through level
        for i in range(50):
            for j in range(25):
                if level[i][j] == -1:
                    # Nothing to see here
                    pass
                elif level[i][j] < 5:
                    # Make door with keyID
                    if not self.door:
                        self.door = Door(j * 20, i * 10, "Tiles/Doors/door1close.png", "Tiles/Doors/door1open.png", levelID + 1, level[i][j] + 1)
                elif level[i][j] < 10:
                    # Make platform with style!
                    self.platforms.append(Platform(j * 20, i * 10, "Tiles/Platform/metal" + str(level[i][j] - 4) + ".png"))
                elif level[i][j] < 15:
                    if movingStart[level[i][j] - 10]:
                        movingEnd[level[i][j] - 10] = (j * 20, i * 10)
                    else:
                        movingStart[level[i][j] - 10] = (j * 20, i * 10)
                elif level[i][j] < 20:
                    self.platforms.append(MovablePlatform(j * 20, i * 10, "Tiles/Platform/brick1.png", level[i][j] - 14, "Tiles/Platform/move1.png"))
                elif level[i][j] < 25:
                    self.keys.append(Key(j * 20, i * 10, "Tiles/Misc/key1.png", level[i][j] - 19))
                elif level[i][j] == 25:
                    self.platforms.append(Enemy(j * 20, i * 10, "Tiles/Enemy/rift.png"))
                elif level[i][j] < 35:
                    self.platforms.append(Button(j * 20, i * 10, "Tiles/Misc/button1up.png", "Tiles/Misc/button1down.png", level[i][j] - 29))
                elif level[i][j] < 40:
                    self.platforms.append(Box(j * 20, i * 10 - 10, "Tiles/Platform/box" + str(level[i][j] - 34) + ".png"))

        for i in range(5):
            if movingStart[i] and movingEnd[i]:
                self.platforms.append(MovingPlatform(movingStart[i][0], movingStart[i][1], "Tiles/Platform/move2.png", 5 * (movingStart[i][0] != movingEnd[i][0]), 5 * (movingStart[i][1] != movingEnd[i][1]), (movingStart[i][0], movingEnd[i][0]), (movingStart[i][1], movingEnd[i][1]), 500))
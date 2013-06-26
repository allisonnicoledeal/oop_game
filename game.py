import core
import pyglet
from pyglet.clock import schedule_interval
from pyglet.window import key
from core import GameElement
import sys
from random import randint


#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####

class Key(GameElement):
    IMAGE = 'Key'
    SOLID = False

    def interact(self,player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! Maybe you can open a door with it.")
        has_key = True

        # door.IMAGE = "DoorOpen"

        GAME_BOARD.set_el(7,2, door)
        # print has_key
        print player.inventory

class Door(GameElement):
    IMAGE = 'DoorClosed'
    SOLID = True

    def interact(self, player):
        if (self.IMAGE == 'DoorClosed'):
            GAME_BOARD.del_el(self.x, self.y)
            open_door = Door()
            open_door.IMAGE = 'DoorOpen'
            open_door.SOLID = True
            GAME_BOARD.register(open_door)
            GAME_BOARD.set_el(self.x, self.y, open_door)
            # print engine.board.width
        elif (self.IMAGE == 'DoorOpen'):
            boy_positions = [
                (3,2),
                (8,3),
                (4,4),
                (1,5),
                ]

            boys = []
            for pos in boy_positions:
                boy = Boy()
                GAME_BOARD.register(boy)
                GAME_BOARD.set_el(pos[0], pos[1], boy)
                boys.append(boy)

            tree_positions = [
                (0,2),
                (9,8),
                (1,5),
                (9,5),
                ]

            tall_trees = []
            for pos in tree_positions:
                tree = Tree()
                GAME_BOARD.register(tree)
                GAME_BOARD.set_el(pos[0], pos[1], tree)
                tall_trees.append(tree)

class Tree(GameElement):
    IMAGE = 'TallTree'
    SOLID = True

class Rock(GameElement):
    IMAGE = 'Rock'
    SOLID = True

class Character(GameElement):
    IMAGE = "Cat"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if (has_key == True):
            if (PLAYER.x == 7) and (PLAYER.y == 2):
                door = Door()
                GAME_BOARD.register(door)
                GAME_BOARD.set_el(7, 2, door)
        if direction == "up":
            if self.y-1 < 0:
                return (self.x, self.y)
            else:
                return (self.x, self.y-1)
        elif direction == "down":
            if self.y+1 >= GAME_HEIGHT: #out of bounds
                return (self.x, self.y)
            else:
                return (self.x, self.y+1)
        elif direction == "left":
            if self.x-1 < 0: #out of bounds
                return (self.x, self.y)
            else:
                return (self.x-1, self.y)
        elif direction == "right":
            if self.x+1 >= GAME_WIDTH: #out of bounds
                return (self.x, self.y)
            else:
                return (self.x+1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self,player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = False

    def interact(self,player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a boy! You have %d items!" % (len(player.inventory)))

####   End class definitions    ####

def more_gems(seconds):
    more_gems_positions = [
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9))
        ]

    more_gems_list = []
    for pos in more_gems_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        more_gems_list.append(gem)


def more_rocks(seconds):
    more_rocks_positions = [
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9)),
        (randint(0,9),randint(0,9))
        ]

    more_rocks_list = []
    for pos in more_rocks_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        more_rocks_list.append(rock)


def initialize():
    """Put game initialization code here"""

    pyglet.clock.schedule_interval(more_gems, 3)
    pyglet.clock.schedule_interval(more_rocks, 4)

    rock_positions = [
            (2,1),
            (2,7),
            (6,5),
            (1,9),
            ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("The adventures of catgirl!")


    gem_positions = [
            (1,3),
            (4,7),
            (8,5),
            (9,2),
            ]

    gems = []
    for pos in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(9, 9, key)

    global door
    door = Door()
    GAME_BOARD.register(door)

    global has_key 
    has_key = False

def keyboard_handler():

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
#   elif KEYBOARD[key.SPACE]:
#       GAME_BOARD.erase_msg()

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)








import core
import pyglet
from pyglet.clock import schedule_interval
from pyglet.window import key
from core import GameElement
import sys
from random import randint

#freesound.org

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

#game board dimentions
GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####

#Key class
class Key(GameElement):
    IMAGE = 'Key'
    SOLID = False

    def interact(self,player):
        player.key_inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! Maybe you can open a door with it.")
        # make the closed door appear at a random place
        GAME_BOARD.set_el(randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1), door)

        print player.key_inventory

# Door class
class Door(GameElement):
    IMAGE = 'DoorClosed'
    SOLID = True

    def interact(self, player):
        # checks to see if door has been opened yet (default is closed)
        if (self.IMAGE == 'DoorClosed'):
            # deletes closed door
            GAME_BOARD.del_el(self.x, self.y)
            # creates new open door
            open_door = Door()
            open_door.IMAGE = 'DoorOpen'
            open_door.SOLID = True
            GAME_BOARD.register(open_door)
            GAME_BOARD.set_el(self.x, self.y, open_door)
        #if door has been opened, adds more boys to gameboard
        elif (self.IMAGE == 'DoorOpen'):
            boy_positions = [
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1))
                ]

            boys = []
            for pos in boy_positions:
                existing_el = GAME_BOARD.get_el(pos[0], pos[1])
                # only places boys on empty coordinates, otherwise does nothing
                if not existing_el:
                    boy = Boy()
                    GAME_BOARD.register(boy)
                    GAME_BOARD.set_el(pos[0], pos[1], boy)
                    #adds boy item to boys list
                    boys.append(boy)

            # sets tree positions
            tree_positions = [
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1))
                ]

            tall_trees = []
            for pos in tree_positions:
                existing_el = GAME_BOARD.get_el(pos[0], pos[1])
                 # only places trees on empty coordinates, otherwise does nothing
                if not existing_el:
                    tree = Tree()
                    GAME_BOARD.register(tree)
                    GAME_BOARD.set_el(pos[0], pos[1], tree)
                    #adds tree item to tall_trees list
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
        self.key_inventory = []
        self.boy_inventory = []
        self.gem_inventory = []

    def next_pos(self, direction):
        #checks character coordinate movements to prevent her from going off board
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
    # adds gem to gem_inventory when player interacts w gem
    def interact(self,player):
        player.gem_inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems and %d boys!" % (len(player.gem_inventory), len(player.boy_inventory)))

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = False

    def interact(self,player):
    # adds boy to boy_inventory when player interacts w boy
        player.boy_inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems and %d boys!" % (len(player.gem_inventory), len(player.boy_inventory)))

####   End class definitions    ####

#generates raining gems 
def more_gems(seconds):
    more_gems_positions = [
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1))
        ]

    more_gems_list = []
    for pos in more_gems_positions:
        existing_el = GAME_BOARD.get_el(pos[0], pos[1])
        if not existing_el:
            gem = Gem()
            GAME_BOARD.register(gem)
            GAME_BOARD.set_el(pos[0], pos[1], gem)
            more_gems_list.append(gem)

#generates raining rocks
def more_rocks(seconds):
    more_rocks_positions = [
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1)),
        (randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1))
        ]

    more_rocks_list = []
    for pos in more_rocks_positions:
        existing_el = GAME_BOARD.get_el(pos[0], pos[1])
        if (not existing_el) or (type(existing_el) == Gem):
            rock = Rock()
            GAME_BOARD.register(rock)
            GAME_BOARD.set_el(pos[0], pos[1], rock)
            more_rocks_list.append(rock)

def avalanche_check(seconds):
    # get player location coordinates
    check_x = PLAYER.x
    check_y = PLAYER.y

    # up, left, down, right = None, None, None, None
    # try:
    #     up = GAME_BOARD.get_el(check_x, check_y-1)
    # except:
    #     pass
    # try:
    #     down = GAME_BOARD.get_el(check_x, check_y+1)
    # except:
    #     pass
    # try:
    #     right = GAME_BOARD.get_el(check_x+1, check_y)
    # except:
    #     pass
    # try:
    #     left = GAME_BOARD.get_el(check_x-1, check_y)
    # except:
    #     pass

    # surroundings = [up, down, left, right]
    # object_types = [type(obj) for obj in surroundings]
    # print object_type
    

    # if ("<type 'NoneType'>" in object_types): # or Gem in object_types: 
    #         GAME_BOARD.draw_msg("none")
    #     # if Gem in object_types:
    #     #     GAME_BOARD.draw_msg("not surounded")
    # else:
    #     GAME_BOARD.draw_msg("Oh no, an avalanche! You're trapped. Game over.")


    if PLAYER.y != 0:
        existing_above = GAME_BOARD.get_el(check_x, check_y-1)
    else:
        existing_above = None

    if PLAYER.y != GAME_HEIGHT-1:
        existing_below = GAME_BOARD.get_el(check_x, check_y+1)
    else:
        existing_below = None

    if PLAYER.x != GAME_WIDTH-1:
        existing_right = GAME_BOARD.get_el(check_x+1, check_y)
    else:
        existing_right = None

    if PLAYER.x != 0:
        existing_left = GAME_BOARD.get_el(check_x-1, check_y)
    else:
        existing_left = None

    if (existing_above != None and existing_above.SOLID == True) or (PLAYER.y == 0):
        print "solid above!"
        if (existing_below != None and existing_below.SOLID == True) or (PLAYER.y == GAME_HEIGHT-1):
            if (existing_right != None and existing_right.SOLID == True) or (PLAYER.x == GAME_WIDTH-1):
                if (existing_left != None and existing_left.SOLID == True) or (PLAYER.x == 0):
                    GAME_BOARD.draw_msg("Oh no, an avalanche! You're trapped. Game over.")



def initialize():
    """Put game initialization code here"""
    # http://code.google.com/p/pyglet/issues/detail?id=203
    #create media Player
    radio = pyglet.media.Player()
    #load sound source file
    music = pyglet.media.load('./music/music.wav')
    #loop sound
    # music.EOS_LOOP = "loop"
    radio.queue(music)
    # radio.eos_action = pyglet.media.Player.EOS_LOOP
    radio.volume = 0.4
    radio.play()

    #gems/rocks rain schedule
    pyglet.clock.schedule_interval(more_gems, 2)
    pyglet.clock.schedule_interval(more_rocks, 2)

    # schedule for avalanche check
    pyglet.clock.schedule_interval(avalanche_check, .5)

    # adds initial rocks and gems to game board
    more_rocks(1)
    more_gems(1)

    #initial game message
    GAME_BOARD.draw_msg("The Adventures of Catgirl! How many items can you get before you get trapped by rocks?")

    #create and register initial instance of key
    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1), key)

    #create and register player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(randint(0,GAME_WIDTH-1),randint(0,GAME_HEIGHT-1), PLAYER)
    print PLAYER

    #create and register door
    #why can't we do these three lines in interact method of Key class??
    global door
    door = Door()
    GAME_BOARD.register(door)


def keyboard_handler():

    direction = None
    # reads keyboard input and stores as direction
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

    #if player has pressed a direction key, call next_pos function to update char location
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        #gets element, if any, at the position where the player is moving to
        existing_el = GAME_BOARD.get_el(next_x, next_y)

        #if there is an element, call that element's interact method
        if existing_el:
            existing_el.interact(PLAYER)

        # if there is not an element (in pos to be moved to) or if there is a non-solid 
        #element, move player
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)








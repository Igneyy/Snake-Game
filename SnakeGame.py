from designer import *
import random
import time
import pygame
from cisc108 import assert_equal

SNAKE_SPEED_HORIZONTAL = 11.2
SNAKE_SPEED_VERTICAL = 11.24
inputs_list = []
timed = []
counter = []
slowmotion_duration = []
regenerating_slowmotion = []

World = {'snake': [DesignerObject],
         'snake_speed_horizontal': int,
         'snake_speed_vertical': int,
         'food': DesignerObject,
         'border': DesignerObject,
         'score': int,
         'counter': DesignerObject,
         'shield': DesignerObject,
         'shielded': bool,
         'shieldicon': DesignerObject,
         'slowmotion': bool,
         'slowmotion_icon': DesignerObject,
         'slowmotion_time_left': int,
         'slowmotion_timer': DesignerObject,
         'instructions': [DesignerObject],
         'obstacles': [DesignerObject],
         'invisible_box': DesignerObject
}

def create_world() -> World:
    '''
    creates a world with a snake segment as the head, snake vertical and horizontal speeds, a food for the snake,
    the border fo the game, score, and a counter. 
    
    Args:
        None
    
    Returns:
        World: A World with a snake, snake speeds, food, border, score and a counter
    '''
    return {'snake': [create_snake()],
            'snake_speed_horizontal': SNAKE_SPEED_HORIZONTAL,
            'snake_speed_vertical': SNAKE_SPEED_VERTICAL,
            'food': create_food(),
            'border': rectangle('black', 784, 562, get_width()/2, get_height()/2, border = 10),
            'score': 0,
            'counter': text('black', '', 20, get_width()/2, 10),
            'shield': None,
            'shielded': False,
            'shieldicon': None,
            'slowmotion': False,
            'slowmotion_icon': create_slowmotion_icon(),
            'slowmotion_time_left': 4,
            'slowmotion_timer': text('black', '4', 20, 625, 10),
            'instructions': [text('black', 'Press WASD or Arrow Keys to move.',20, get_width()/2, 150),
                             text('black', 'Press Space for Slowmotion.', 20, get_width()/2, 175)],
            'obstacles': [],
            'invisible_box': create_invisible_box()
            }

def create_snake() -> DesignerObject:
    '''
    creates a snake segment
    
    Args:
        None
    
    Returns:
        DesignerObject: An image of a snake segment
    '''
    snake = image('red square.jpeg')
    snake['scale_x'] = .02
    snake['scale_y'] = .02
    snake['anchor'] = 'center'
    return snake

def create_invisible_box() -> DesignerObject:
    '''
    creates a box that is not visible
    
    Args:
        None
    
    Returns:
        DesignerObject: A not visile box
    '''
    box = rectangle('green', 125, 125)
    box['visible'] = False
    return box
        
def moving_snake(world: World):
    '''
    causes the snake to move constantly, controls the invisible box to move constantly,
    will enable slowmotion if world['slowmotion'] == True
    
    Args:
        world(World): A World
    
    Returns:
        None
    '''
    if not world['slowmotion']:
        if world['snake_speed_vertical'] == 0:
            world['snake'][0]['x'] += world['snake_speed_horizontal']
            world['invisible_box']['x'] += world['snake_speed_horizontal']
        if world['snake_speed_horizontal'] == 0:
            world['snake'][0]['y'] += world['snake_speed_vertical']
            world['invisible_box']['y'] += world['snake_speed_vertical']
    elif world['slowmotion'] and len(timed)%2 == 0:
        if world['snake_speed_vertical'] == 0:
            world['snake'][0]['x'] += world['snake_speed_horizontal']
            world['invisible_box']['x'] += world['snake_speed_horizontal']
        if world['snake_speed_horizontal'] == 0:
            world['snake'][0]['y'] += world['snake_speed_vertical']
            world['invisible_box']['y'] += world['snake_speed_vertical']

def head_up(world: World):
    '''
    causes the snake to move upwards at the speed -snake_speed_vertical
    
    Args:
        world(World): A World
    
    Returns:
        None
    '''
    world['snake_speed_vertical'] = -SNAKE_SPEED_VERTICAL
    world['snake_speed_horizontal'] = 0

def head_down(world: World):
    '''
    causes the snake to move downwards at the speed snake_speed_vertical
    
    Args:
        world(World): A World
    
    Returns:
        None
    '''
    world['snake_speed_vertical'] = SNAKE_SPEED_VERTICAL
    world['snake_speed_horizontal'] = 0
    
def head_left(world: World):
    '''
    causes the snake to move left at the speed -snake_speed_horizontal
    
    Args:
        world(World): A World
    
    Returns:
        None
    '''
    world['snake_speed_horizontal'] = -SNAKE_SPEED_HORIZONTAL
    world['snake_speed_vertical'] = 0

def head_right(world: World):
    '''
    causes the snake to move right at the speed snake_speed_horizontal
    
    Args:
        world(World): A World
    
    Returns:
        None
    '''
    world['snake_speed_vertical'] = 0
    world['snake_speed_horizontal'] = SNAKE_SPEED_HORIZONTAL

def control_snake(world: World, key: str):
    '''
    controls the snake to move in the direction inputted on the keyboard using the arrow keys
    or WASD, also adds to a list to determine what inputs were made, and removes the instructions
    after an input.
    
    Args:
        world(World): A World
        
        key(str): A string key inputted when typing
    
    Returns:
        None
    '''
    if key == "W" or key == "up":
        if not inputs_list:
            head_up(world)
            inputs_list.append(1)
            world['instructions'].clear()
        elif world['snake_speed_vertical'] == 0:
            head_up(world)
            inputs_list.append(1)
    elif key == "A" or key == "left":
        if not inputs_list:
            head_left(world)
            inputs_list.append(2)
            world['instructions'].clear()
        elif world['snake_speed_horizontal'] == 0:
            head_left(world)
            inputs_list.append(2)
    elif key == "S" or key == "down":
        if not inputs_list:
            head_down(world)
            inputs_list.append(3)
            world['instructions'].clear()
        elif world['snake_speed_vertical'] == 0:
            head_down(world)
            inputs_list.append(3)
    elif key == "D" or key == "right":
        if not inputs_list:
            head_right(world)
            inputs_list.append(3)
            world['instructions'].clear()
        elif world['snake_speed_horizontal'] == 0:
            head_right(world)
            inputs_list.append(4)

def create_food() -> DesignerObject:
    '''
    creates a food DesignerObject
    
    Args:
        None
        
    Returns:
        DesignerObject: the image of a food
    '''
    food = image('red square.jpeg')
    food['scale_x'] = .025
    food['scale_y'] = .025
    food['anchor'] = 'topleft'
    food['x'] = random.randint(get_width()-784, 772)
    food['y'] = random.randint(get_height()-562, 560)
    return food

def teleport_food_new_segments_new_obstacles(world: World):
    '''
    teleports food after a food is eaten, adds 4 new segments behind the snake head and
    creates an obstacle 50% of the time after a food is eaten
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    world['food']['anchor'] = 'topleft'
    if colliding(world['snake'][0], world['food']):
        new_segment = create_snake()
        move_behind(new_segment, world['snake'][-1])
        new_segment2 = create_snake()
        move_behind(new_segment2, new_segment)
        new_segment3 = create_snake()
        move_behind(new_segment3, new_segment2)
        new_segment2
        new_segment4 = create_snake()
        move_behind(new_segment4, new_segment3)
        world['snake'].append(new_segment)
        world['snake'].append(new_segment2)
        world['snake'].append(new_segment3)
        world['snake'].append(new_segment4)
        obstacle_creator = random.randint(0,1)
        if obstacle_creator == 0 and random.randint(0,1) == 1:
            world['obstacles'].append(create_obstacle1())
            while colliding_with_snake(world, world['obstacles'][-1]):
                world['obstacles'][-1]['x'] = random.randint(get_width()-780, 765)
                world['obstacles'][-1]['y'] = random.randint(get_height()-555, 545)
        if obstacle_creator == 1 and random.randint(0,1) == 1:
            world['obstacles'].append(create_obstacle2())
            while colliding_with_snake(world, world['obstacles'][-1]):
                world['obstacles'][-1]['x'] = random.randint(get_width()-780, 765)
                world['obstacles'][-1]['y'] = random.randint(get_height()-555, 545)      
        while colliding_with_snake(world, world['food']):
            world['food']['x'] = random.randint(get_width()-784, 772)
            world['food']['y'] = random.randint(get_height()-562, 550)


def move_behind(snake_tail: DesignerObject, snake_head: DesignerObject):
    '''
    moves the snake tail (a new segment) behind the segment before it the snake_head
    
    Args:
        snake_tail(DesignerObject): the segment you want to move behind the previous one
    
        snake_head(DesignerObject): the segment in front of the segment you want to be placed behind
    
    Returns:
        None
    '''
    if inputs_list:
        if inputs_list[-1] == 1:
            snake_tail['y'] = snake_head['y'] + snake_head['height']
            snake_tail['x'] = snake_head['x']
        elif inputs_list[-1] == 2:
            snake_tail['y'] = snake_head['y']
            snake_tail['x'] = snake_head['x'] + snake_head['width']
        elif inputs_list[-1] == 3:
            snake_tail['y'] = snake_head['y'] - snake_head['height']
            snake_tail['x'] = snake_head['x']
        elif inputs_list[-1] == 4:
            snake_tail['y'] = snake_head['y']
            snake_tail['x'] = snake_head['x'] - snake_head['width']

def move_snake_segments(world: World):
    '''
    Takes the snake segment's location and moves the snake segment behind it into its own position
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    snake_segments = world['snake']
    index = range(len(snake_segments))
    listx = []
    listy = []
    for segment in snake_segments:
        listx.append(segment['x'])
        listy.append(segment['y'])
    if not world['slowmotion']:
        for i in index:
            if i > 0:
                snake_segments[i]['x'] = listx[i-1]
                snake_segments[i]['y'] = listy[i-1]
    elif world['slowmotion'] and len(timed)%2 == 0:
        for i in index:
            if i > 0:
                snake_segments[i]['x'] = listx[i-1]
                snake_segments[i]['y'] = listy[i-1]

def timer():
    '''
    appends to a list for every update (30 in a second) and will clear out the the timer and inputs_list lists
    every 1/3 second (after 10 updates) leaving the inputs_list only with the last directional input
    
    Args:
        None
        
    Returns:
        None
    '''
    if inputs_list:
        timed.append(1)
        last_input = inputs_list[-1]
    if len(timed)%10 == 0 and inputs_list:
        inputs_list.clear()
        inputs_list.append(last_input)
        timed.clear()

def snake_hits_border(world: World) -> bool:
    '''
    checks if the snake head has collided with the border of the world
    
    Args:
        world(World): A world
    
    Returns:
        bool: whether the snake collided with the border or not
    '''
    collided = False
    snake_head = world['snake'][0]
    if snake_head['x'] > 772 or snake_head['x'] < get_width()-772 or snake_head['y'] > 562 or snake_head['y'] < get_height()-562:
        collided = True
    return collided

def snake_hits_self(world: World) -> bool:
    '''
    checks if the snake has collided with any of its segments, if the snake is shielded the snake will
    pass through a single segment and lose the shield
    
    Args:
        world(World): A world
    
    Returns:
        bool: whether the snake collided or not with itself
    '''
    collided = False
    snake_segments = world['snake']
    snake_head = snake_segments[0]
    for i in range(len(snake_segments)):
        if i > 0 and i > 1:
            if colliding(snake_head, snake_segments[i]):
                if not world['shielded']:
                    collided = True
                elif world['shielded']:
                    world['shieldicon']['scale'] = 0
                    world['shielded'] = False
    return collided

def snake_hits_obstacle(world: World) -> bool:
    '''
    checks to see if the snake head has collided with an obstacle, if the snake is shielded
    the obstacle is removed and the snake loses its shield
    
    Args:
        world(World): A world
        
    Returns:
        bool: Whether the snake collided or not with an obstacle
    '''
    collided = False
    obstacle_list = world['obstacles']
    for i in range(len(obstacle_list)):
        hit_obstacle = obstacle_list[i]
        if colliding(world['snake'][0], hit_obstacle):
            if not world['shielded']:
                collided = True
            elif world['shielded']:
                world['shieldicon']['scale'] = 0
                world['shielded'] = False
                obstacle_list[i] = None
    return collided

def score_counter(world: World):
    '''
    counts the score for every second that passes
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    counter.append(1)
    if len(counter)%30 == 0 and inputs_list:
        world['score'] = world['score'] + 1
        counter.clear()

def update_score(world: World):
    '''
    updates the score coaunter in world['counter'] with the score for the time and
    total length of the snake
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    world['counter']['text'] = 'Time: ' + str(world['score']) + '         Length: ' + str(len(world['snake']))
    
def create_shield_powerup() -> DesignerObject:
    '''
    creates a shield powerup
    
    Args:
        None
    
    Returns
        DesignerObject: image of a shield
    '''
    shield = image('shield.png')
    shield['scale_x'] = .02
    shield['scale_y'] = .02
    return shield

def generate_shield(world: World):
    '''
    creates a shield in a random location with a 1/1500 chance that is rolled 30 times a second as long
    as the snake is not shielded and a shield doesn't currently exist
    
    Args:
        world(World): A world
        
    Returns:
        None
    '''
    if random.randint(0,1500) == 0 and not world['shielded'] and not world['shield'] and inputs_list:
        shield = create_shield_powerup()
        world['shield'] = shield
        world['shield']['x'] = random.randint(get_width()-784, 772)
        world['shield']['y'] = random.randint(get_height()-562, 560)
        while colliding_with_snake(world, world['shield']):
            world['shield']['x'] = random.randint(get_width()-784, 772)
            world['shield']['y'] = random.randint(get_height()-562, 560)

def create_shieldicon() -> DesignerObject:
    '''
    creates a shield icon at the top right ish area of the screen
    
    Args:
        None
    
    Returns:
        DesignerObject: A shield image at the top right ish area of the screen
    '''
    shieldicon = image('shield.png')
    shieldicon['scale_x'] = .03
    shieldicon['scale_y'] = .03
    shieldicon['x'] = 600
    shieldicon['y'] = 10
    return shieldicon

def shielded_snake(world: World):
    '''
    If the snake is shielded the shield icon will appear at the top right ish area of the screen
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    if colliding(world['snake'][0], world['shield']):
        world['shielded'] = True
        world['shield'] = None
        world['shieldicon'] = create_shieldicon()
    
def create_slowmotion_icon() -> DesignerObject:
    '''
    creates an icon for the slowmotion timer
    
    Args:
        None
    
    Returns:
        DesignerObject: Image of the slowmotion clock icon
    '''
    slowmotion_icon = image('slow.png')
    slowmotion_icon['scale'] = .05
    slowmotion_icon['x'] = 625
    slowmotion_icon['y'] = 10
    return slowmotion_icon

def space_is_held(world: World) -> bool:
    '''
    determines if space is being held down
    
    Args:
        world(World): A world
    
    Returns:
        bool: Whether space is being held or not
    '''
    keys = pygame.key.get_pressed()
    return keys[pygame.K_SPACE]

def space_is_released(world: World) -> bool:
    '''
    determines if space is being released
    
    Args:
        world(World): A world
    
    Returns:
        bool: Whether space is being released or not
    '''
    keys = pygame.key.get_pressed()
    return not keys[pygame.K_SPACE]

def run_when_space_held(world: World):
    '''
    when space is being held down the list of the cooldown for the slowmtion will be cleared, a number will be appended
    to the slowmotion duration list, if the list length is between 0-30 the duration is 4 seconds , 30-60, 3 seconds, 60-90,
    2 seconds, 90-119, 1 second, and 120, 0.
    If the list reaches 120 slowmtion ends.
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    regenerating_slowmotion.clear()
    if world['slowmotion_time_left'] > 0 and len(slowmotion_duration) < 120:
        world['slowmotion'] = True
        slowmotion_duration.append(1)
        if len(slowmotion_duration) > 0 and len(slowmotion_duration) < 30:
            world['slowmotion_time_left'] = 4
            world['slowmotion_timer']['text'] = world['slowmotion_time_left']
        if len(slowmotion_duration) >= 30 and len(slowmotion_duration) < 60:
            world['slowmotion_time_left'] = 3
            world['slowmotion_timer']['text'] = world['slowmotion_time_left']
        if len(slowmotion_duration) >= 60 and len(slowmotion_duration) < 90:
            world['slowmotion_time_left'] = 2
            world['slowmotion_timer']['text'] = world['slowmotion_time_left']
        if len(slowmotion_duration) >= 90 and len(slowmotion_duration) < 120:
            world['slowmotion_time_left'] = 1
            world['slowmotion_timer']['text'] = world['slowmotion_time_left']
    elif len(slowmotion_duration) >= 120:
        world['slowmotion'] = False
        world['slowmotion_time_left'] = 0
        world['slowmotion_timer']['text'] = world['slowmotion_time_left']

def run_when_space_released(world: World):
    '''
    when space is released slowmotion is not active and if slowmotion is used the regenerating list will have a number added to it.
    If the regenerating slowmotion list reaches a length of 300 (takes 5 seconds) the slowmotion duration list will start to decrease.
    If slowmotion duration was 120 slowmotion will become useable again and eventually reach "4" which is full duration. If slowmotion
    is used after regenerating starts 5 seconds must be waited for slowmotion to begin regenerating again.
    
    Args:
        world(World): A world
    
    Returns:
        None
    '''
    world['slowmotion'] = False
    if slowmotion_duration:
        if len(regenerating_slowmotion) < 150:
            regenerating_slowmotion.append(1)
        if len(regenerating_slowmotion) == 150:
            del slowmotion_duration[-1]
            if len(slowmotion_duration) > 0 and len(slowmotion_duration) < 15:
                world['slowmotion_time_left'] = 4
                world['slowmotion_timer']['text'] = world['slowmotion_time_left']
            if len(slowmotion_duration) >= 15 and len(slowmotion_duration) < 30:
                world['slowmotion_time_left'] = 3
                world['slowmotion_timer']['text'] = world['slowmotion_time_left']
            if len(slowmotion_duration) >= 30 and len(slowmotion_duration) < 60:
                world['slowmotion_time_left'] = 2
                world['slowmotion_timer']['text'] = world['slowmotion_time_left']
            if len(slowmotion_duration) >= 60 and len(slowmotion_duration) <= 90:
                world['slowmotion_time_left'] = 1
                world['slowmotion_timer']['text'] = world['slowmotion_time_left']

def colliding_with_snake(world: World, designerobject: DesignerObject) -> bool:
    '''
    tests if a designerobject is colliding with an object in the world, including a snake segment
    an obstacle and the invisible box.
    
    Args:
        world(World): A world
        
        designerobject: A DesignerObject
    
    Returns:
        bool: if the DesignerObject was colliding with a snake segment, an obstacle, or the invisible box
    '''
    collided = False
    for segment in world['snake']:
        if colliding(designerobject, segment):
            collided = True
    if not designerobject in world['obstacles']:
        for obstacle in world['obstacles']:
            if colliding(designerobject, obstacle):
                collided = True
    if colliding(designerobject, world['invisible_box']):
        collided = True
    return collided
                
def create_obstacle1() -> DesignerObject:
    '''
    creates an obstacle that is wide
    
    Args:
        None
    
    Returns:
        DesignerObject: A wide obstacle
    '''
    obstacle = rectangle('black', 10, 30)
    obstacle['x'] = random.randint(get_width()-784, 772)
    obstacle['y'] = random.randint(get_height()-562, 550)
    return obstacle

def create_obstacle2() -> DesignerObject:
    '''
    creates a tall obstacle
    
    Args:
        None
        
    Returns:
        DesignerObject: A tall obstacle
    '''
    obstacle = rectangle('black', 30, 10)
    obstacle['x'] = random.randint(get_width()-784, 772)
    obstacle['y'] = random.randint(get_height()-562, 550)
    return obstacle

    
    
when('starting', create_world)
when('updating', moving_snake)
when('typing', control_snake)
when('updating', teleport_food_new_segments_new_obstacles)
when('updating', move_snake_segments)
when('updating', timer)
when('updating', score_counter)
when('updating', update_score)
when('updating', generate_shield)
when('updating', shielded_snake)
when(space_is_held, run_when_space_held)
when(space_is_released, run_when_space_released)
when(snake_hits_border, pause)
when(snake_hits_self, pause)
when(snake_hits_obstacle, pause)
start()
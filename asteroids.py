# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

rock_group = set([])
missile_group = set([])
explosion_group = set([])
total_rocks = 0 # total number of rocks in the game
total_rock_collisions = 0
total_missiles = 0 # total number of missiles in the game
total_missile_collisions = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# helper function to find distance between two objects
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    # return Ship's position
    def get_position(self):
        return self.pos
    
    # return Ship's radius
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        # draw ship with thrusters
        if self.thrust:
            self.image_center[0] = 135 # 135 is horizontal pos of ship w/ thrust
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        # draw ship WITHOUT thrusters
        else:
            self.image_center[0] = 45 # 45 is horizontal pos of ship w/out thrust
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        # Position Update including wall "wrapping"
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        
        # Angular Velocity Update (come back to this?)
        self.angle += self.angle_vel
        
        # calculate the forward vector
        forward = angle_to_vector(self.angle)
       
        # accelerate the ship in the direction of its
        # forward vector - to infinity and beyond!
        if self.thrust:
            self.vel[0] += (forward[0] * .1) 
            self.vel[1] += (forward[1] * .1)
        
        # add in some friction so the ship doesn't
        # accelerate too fast
        self.vel[0] *= .99
        self.vel[1] *= .99
        
    # turn on/off the thrusters!
    def thrusters(self, thrusting):
        self.thrust = thrusting
        
        if thrusting:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
        
    # rotates the ship left when "left" key is pressed
    def turn_left(self):
        self.angle_vel = .09
    
    # rotates the ship right when "right" key is pressed
    def turn_right(self):
        self.angle_vel = -.09
        
    # stop ship's rotation
    def turn_stop(self):
        self.angle_vel = 0
        
    # missile method
    def shoot(self):
        global missile_group
        
        fwd_vector = angle_to_vector(self.angle) # ship's forward vector
        missile_velocity = [self.vel[0] + 5 * fwd_vector[0], # x-cord for missile vel
                            self.vel[1] + 5 * fwd_vector[1]] # y-cord for missile vel
        
        missile_pos = [self.pos[0] + fwd_vector[0] * self.radius, # x-cord for missile pos
                       self.pos[1] + fwd_vector[1] * self.radius] # y-cord for missile pos
        
        new_missile = Sprite(missile_pos, missile_velocity, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(new_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
     
    # return the Sprite object's position
    def get_position(self):
        return self.pos
    
    # return the Sprite object's position
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        global time
        explosion_dim = 24 # num of explosion tiles in explosion image
        
        # handle the drawing for explosions
        if self.animated:
            explosion_index = (time % explosion_dim) # calculate index of explosion image_center relative to time
            explosion_center = [self.image_center[0] + explosion_index * self.image_size[0], self.image_center[1]] # determine the center of the explosion image
            canvas.draw_image(self.image, explosion_center, self.image_size, self.pos, self.image_size, self.angle)
            time += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
           
    def update(self):
        # make the Sprite rotate
        self.angle += self.angle_vel        
        
        # give the asteroid a velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
        # increment the age of the Sprite (missile)
        # so we don't have missiles sticking 
        # around forever
        self.age += 1
        
        # the logic for checking if the time has come
        # to remove a missile from the screen
        if self.age >= self.lifespan:
            return True
        elif self.age < self.lifespan:
            return False
        
    def collide(self, an_object):
        distance = dist(self.get_position(), an_object.get_position())
        if distance > self.get_radius() + an_object.get_radius():
            return False
        else:
            return True
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
def draw(canvas):
    global time, score, lives, started, total_rocks
    global rock_group, missile_group
    global soundtrack
    
    # draw UI and animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    # draw splash screen if not started
    if not started:
        lives = 3
        score = 0
        rock_group = set([])
        missile_group = set([])
        total_rocks = 0
        soundtrack.rewind()
        soundtrack.play()
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        my_ship.angle = 0
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    else:    
        my_ship.draw(canvas)
        my_ship.update()
        # draw/update rocks and missiles
        process_sprite_group(rock_group, canvas) # draw asteroids
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        # handle collision between rock and ship
        if group_collide(rock_group, my_ship) > 0:
            lives -= 1
            
        # handle collision between rock and missile    
        if group_group_collide(rock_group, missile_group) > 0:
            score += 10
            
        # if player has lost all 3 lives, restart game
        if lives == 0:
            started = False
            
    
    #draw score and lives
    canvas.draw_text("Lives", [50, 50], 28, "White")
    canvas.draw_text("Score", [680, 50], 28, "White")
    canvas.draw_text(str(lives), [50, 80], 28, "White")
    canvas.draw_text(str(score), [680, 80], 28, "White")
    
# helper function to check collision between a group and an object
def group_collide(group, other_object):
    global total_rocks
    global explosion_group
    
    removed_rocks = set([])
    collision = 0
    
    # loop through the group and check if any of it's
    # elements collide with another object    
    for i in group:
        if i.collide(other_object):
            removed_rocks.add(i)
            explosion_group.add(Sprite(i.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            collision += 1
            total_rocks -= 1  
        group.difference_update(removed_rocks)
    return collision
    
# helper function to check collision between two groups
def group_group_collide(rocks, missiles):
    global total_rocks
    collision = 0
    new_rock_group = set([])
    
    # loop through rock_group and check if any of it's
    # elements collide with the elements in missile_group
    for i in rocks:
        if group_collide(missiles, i):
            new_rock_group.add(i)
            collision += 1
        rocks.difference_update(new_rock_group)
    return collision
    
# key handler when button is pressed down
def key_down(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_left()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn_right()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters(True)
    elif key == simplegui.KEY_MAP["space"]: # shoot missile!
        my_ship.shoot()

# key handler when button is released
def key_up(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_stop()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn_stop()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters(False)
                
# timer handler that spawns a rock    
def rock_spawner():
        
    global rock_group, total_rocks, score
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * random.choice([1, -1]) * .01 * score, 
                random.random() * random.choice([1, -1]) * .01 * score]
    rock_avel = random.random() * .2 - .1
    new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        
    # limit the total number of asteroids at any given time to < 12 
    if total_rocks < 12:
        # don't spawn a rock if it is too close to the ship
        if dist(rock_pos, my_ship.pos) > my_ship.radius * 4: 
            rock_group.add(new_rock)
            total_rocks += 1 
            
# helper function to draw and update asteroid/missile groups
def process_sprite_group(some_set, canvas):
    for i in some_set:
        i.draw(canvas)
        i.update()
    
    removed_missiles = set([])
    for i in some_set:
        if i.update() == True:
            removed_missiles.add(i)
        some_set.difference_update(removed_missiles)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

"""
Base code for ball bouncing 
"""

import pygame
import pymunk
import math
import colorsys
import time

### CONSTANTS ###
# Physics Properties
MASS_OF_BALL = 1
ELASTICITY_OF_BALL = 1
INIT_X_VEL_OF_BALL = 200
INIT_Y_VEL_OF_BALL = 200
SPACE_GRAVITY_PYMUNK = (0, -900)

# Position and Sizes
WIDTH_OF_PYGAME = 1000
HEIGHT_OF_PYGAME = 800
STARTING_POS_OF_BALL = 500, 400 # relative to the center
RADIUS_OF_BALL = 10

# Circle Properties
STARTING_POS_OF_CIRCLE = (500, 250) # relative to the center 
RADIUS_OF_CIRCLE = 200
SEGEMENTS_OF_CIRCLE = 500

# Special Growth Property
GROWTH_COOLDOWN_THRESHOLD = 10 # Number of frames to wait before allowing growth again
INC_RATE = 1

# Game Variables
SPACE_STEP_PYMUNK = 1/100.0 # change this if ball starts going through circle default is 60
CLOCK_TICK = 60
MAX_TRAIL_LENGTH = 100
TRAIL_GROWTH_RATE = 1

def to_pygame(p):
    """ Convert Pymunk coordinates to Pygame coordinates. """
    return int(p[0]), int(600 - p[1])

def create_circle_boundary(space, center, radius, segments):
    """ Create a circular boundary using line segments. """
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = center
    space.add(body)

    points = []
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        points.append((x, y))

    for i in range(segments):
        shape = pymunk.Segment(body, points[i], points[i + 1], 0)
        shape.elasticity = 1.0
        space.add(shape)

def get_next_color(hue, saturation=1, value=1):
    """Get the next color in the HSV spectrum."""
    hue = (hue + 0.01) % 1  # Increment hue and loop around if it exceeds 1
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)

# Collision handler
def collision_handler(arbiter, space, data):
    global ball_color, current_hue, ball_radius, growth_cooldown
    ball_color = get_next_color(current_hue)
    current_hue = (current_hue + 0.01) % 1

    # Increase ball size only if cooldown has passed
    if growth_cooldown >= growth_cooldown_threshold:
        ball_radius += INC_RATE  # Increment the radius
        resize_ball(ball_body, ball_radius)
        growth_cooldown = 0  # Reset cooldown

    return True

def resize_ball(ball_body, new_radius):
    """ Resize the ball and update its physical properties. """
    global ball_shape
    space.remove(ball_shape)  # Remove the old shape

    # Recalculate moment of inertia for the new radius
    moment = pymunk.moment_for_circle(ball_mass, 0, new_radius)
    ball_body.moment = moment

    ball_shape = pymunk.Circle(ball_body, new_radius)
    ball_shape.elasticity = ball_elasticity
    ball_shape.collision_type = ball_shape.collision_type  # Set collision type
    space.add(ball_shape)

# Initialize Pygame
pygame.init()
width = WIDTH_OF_PYGAME
height = HEIGHT_OF_PYGAME
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball Inside a Circle")
clock = pygame.time.Clock()

# Initialize Pymunk Space
space = pymunk.Space()
space.gravity = SPACE_GRAVITY_PYMUNK

# Create the Ball
ball_mass = MASS_OF_BALL
ball_radius = RADIUS_OF_BALL
ball_elasticity = ELASTICITY_OF_BALL
ball_body = pymunk.Body(ball_mass, pymunk.moment_for_circle(ball_mass, 0, ball_radius))
ball_body.position = STARTING_POS_OF_BALL
initial_velocity_x = INIT_X_VEL_OF_BALL  # Adjust this value as needed
initial_velocity_y = INIT_Y_VEL_OF_BALL  # Adjust this value as needed
ball_body.velocity = (initial_velocity_x, initial_velocity_y)
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = ball_elasticity
space.add(ball_body, ball_shape)
ball_color = (255, 0, 0)
current_hue = 0

# Create the Circular Boundary
circ_center = STARTING_POS_OF_CIRCLE
circ_radius = RADIUS_OF_CIRCLE
circ_segments = SEGEMENTS_OF_CIRCLE # Increase for a smoother circle
create_circle_boundary(space, circ_center, circ_radius, circ_segments)

# Collision Handling
handler = space.add_collision_handler(ball_shape.collision_type, 0)  # Assuming 0 is the collision type for the boundary
handler.begin = collision_handler

# Initialize cooldown counter for ball growth
growth_cooldown = 0
growth_cooldown_threshold = GROWTH_COOLDOWN_THRESHOLD  # Number of frames to wait before allowing growth again
    
# Trail effect
trail_positions = []
frame_count = 0
# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update physics
    space.step(SPACE_STEP_PYMUNK)    
    
    # Increment growth cooldown
    growth_cooldown += 1

    # Add the ball's position to the trail every 10 frames
    frame_count += TRAIL_GROWTH_RATE
    if frame_count % 5 == 0:
        trail_positions.append((to_pygame(ball_body.position), ball_color, ball_radius))
        if len(trail_positions) > MAX_TRAIL_LENGTH:  # Limit trail length
            trail_positions.pop(0)

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the trail
    for pos, color, rad in trail_positions:
        pygame.draw.circle(screen, (255, 255, 255), pos, rad+2)  # Trail with a lighter shade
        pygame.draw.circle(screen, color, pos, rad)

    # Draw the ball
    ball_pos = to_pygame(ball_body.position)
    pygame.draw.circle(screen, (255, 255, 255), ball_pos, ball_radius + 2)
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Draw the circular boundary
    for segment in space.shapes:
        if isinstance(segment, pymunk.Segment):
            p1 = to_pygame(segment.a + segment.body.position)
            p2 = to_pygame(segment.b + segment.body.position)
            pygame.draw.lines(screen, (255, 255, 255), False, [p1, p2], 2)

    pygame.display.flip()
    clock.tick(CLOCK_TICK)

pygame.quit()
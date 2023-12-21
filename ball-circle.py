import pygame
import pymunk
import math
import colorsys

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

def to_pygame(p):
    """ Convert Pymunk coordinates to Pygame coordinates. """
    return int(p[0]), int(600 - p[1])

# Initialize Pygame
pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball Inside a Circle")
clock = pygame.time.Clock()

# Initialize Pymunk Space
space = pymunk.Space()
space.gravity = (0, -900)

# Create the Ball
ball_mass = 1
ball_radius = 10
ball_elasticity = 0.9
ball_body = pymunk.Body(ball_mass, pymunk.moment_for_circle(ball_mass, 0, ball_radius))
ball_body.position = 500, 400
initial_velocity_x = 100  # Adjust this value as needed
initial_velocity_y = 400  # Adjust this value as needed
ball_body.velocity = (initial_velocity_x, initial_velocity_y)

ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = ball_elasticity
space.add(ball_body, ball_shape)

# Create the Circular Boundary
circ_center = (500, 250)
circ_radius = 200
circ_segments = 500  # Increase for a smoother circle
create_circle_boundary(space, circ_center, circ_radius, circ_segments)

# Ball color and hue
ball_color = (255, 0, 0)
current_hue = 0

# Collision handler
def collision_handler(arbiter, space, data):
    global ball_color, current_hue
    ball_color = get_next_color(current_hue)
    current_hue = (current_hue + 0.01) % 1
    return True

handler = space.add_collision_handler(ball_shape.collision_type, 0)  # Assuming 0 is the collision type for the boundary
handler.begin = collision_handler

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
    space.step(1/70.0)

    # Add the ball's position to the trail every 10 frames
    frame_count += 1
    if frame_count % 5 == 0:
        trail_positions.append((to_pygame(ball_body.position), ball_color))
        if len(trail_positions) > 100:  # Limit trail length
            trail_positions.pop(0)

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the trail
    for pos, color in trail_positions:
        pygame.draw.circle(screen, (255, 255, 255), pos, ball_radius+2)  # Trail with a lighter shade
        pygame.draw.circle(screen, color, pos, ball_radius)

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
    clock.tick(60)

pygame.quit()

# Ball Bouncing Physics

@CodeCraftedPhysics makes these videos of "Every time the ball bounces it gets larger" and other properties on ball bouncing. However it costs $15 to get access to the code. I wanted to see if I could recreate it and make it open source.

# Setup

Install dependencies

```bash
pip install pygame
```
```bash
pip install pymunk
```

Thats it the code should now run.


# Configuration

Change the constants for different ball movements. Suggested variables to change:
```python
MASS_OF_BALL = 1
ELASTICITY_OF_BALL = .9 
INIT_X_VEL_OF_BALL = 200
INIT_Y_VEL_OF_BALL = -800
SPACE_GRAVITY_PYMUNK = (0, -900)
GROWTH_COOLDOWN_THRESHOLD = 10 
INC_RATE = 1
```
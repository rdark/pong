"""Game constants and configuration."""

# Display settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
PADDLE_OFFSET = 50  # Distance from edge of screen

# Ball settings
BALL_SIZE = 10
BALL_INITIAL_SPEED = 5
BALL_MAX_SPEED = 10
BALL_SPEED_INCREMENT = 0.5

# Game settings
WINNING_SCORE = 10
ANGLE_FACTOR = 0.05  # How much paddle hit position affects ball angle

# AI settings
AI_SPEED = 4  # Slightly slower than player
AI_REACTION_ZONE = 30  # Dead zone where AI doesn't move

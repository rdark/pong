"""Ball class for Pong game."""

import math
import random
import pygame
from pong.constants import (
    BALL_SIZE,
    BALL_INITIAL_SPEED,
    BALL_MAX_SPEED,
    BALL_SPEED_INCREMENT,
    WHITE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    ANGLE_FACTOR,
)
from pong.paddle import Paddle


class Ball:
    """Represents the ball in the game."""

    def __init__(self, x: int, y: int):
        """Initialize the ball.

        Args:
            x: X position of the ball
            y: Y position of the ball
        """
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.speed = BALL_INITIAL_SPEED
        self.vx = 0.0
        self.vy = 0.0
        self.reset_velocity()

    @property
    def rect(self) -> pygame.Rect:
        """Get the ball's rectangle for collision detection."""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def reset_velocity(self) -> None:
        """Reset ball velocity with random direction."""
        # Reset speed first
        self.speed = BALL_INITIAL_SPEED

        # Random angle between -45 and 45 degrees
        angle = random.uniform(-math.pi / 4, math.pi / 4)
        # Random direction (left or right)
        direction = random.choice([-1, 1])

        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def update(self) -> None:
        """Update the ball position."""
        self.x += self.vx
        self.y += self.vy

        # Bounce off top and bottom walls
        if self.y - self.size // 2 <= 0:
            self.y = self.size // 2
            self.vy = -self.vy
        elif self.y + self.size // 2 >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.size // 2
            self.vy = -self.vy

    def check_paddle_collision(self, paddle: Paddle) -> bool:
        """Check if ball collides with a paddle and handle the collision.

        Args:
            paddle: The paddle to check collision with

        Returns:
            True if collision occurred, False otherwise
        """
        if not self.rect.colliderect(paddle.rect):
            return False

        # Determine which side of the paddle was hit
        # This is crucial for proper collision when paddle moves horizontally
        ball_center_x = self.x
        paddle_left = paddle.x
        paddle_right = paddle.x + paddle.width
        paddle_center_x = paddle.center_x

        # Check if ball is hitting from left or right side
        hit_from_left = ball_center_x < paddle_center_x

        # Only process collision if ball is hitting the correct face of paddle
        # (prevents ball from "sticking" to paddle when paddle moves into ball)
        if hit_from_left and self.vx < 0:
            # Ball moving left but hit from left side - paddle caught up to ball
            # Don't register this as a valid hit
            return False
        if not hit_from_left and self.vx > 0:
            # Ball moving right but hit from right side - paddle caught up to ball
            # Don't register this as a valid hit
            return False

        # Calculate hit position relative to paddle center (-1 to 1)
        relative_hit = (self.y - paddle.center_y) / (paddle.height / 2)

        # Reverse horizontal direction
        self.vx = -self.vx

        # Adjust vertical velocity based on where the ball hit the paddle
        self.vy += relative_hit * self.speed * ANGLE_FACTOR * 10

        # Increase speed slightly, but don't exceed maximum
        new_speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        if new_speed > self.speed:
            self.speed = new_speed
            # Update velocities to maintain direction but increase magnitude
            current_angle = math.atan2(self.vy, abs(self.vx))
            direction = 1 if self.vx > 0 else -1
            self.vx = direction * self.speed * math.cos(current_angle)
            self.vy = self.speed * math.sin(current_angle)

        # Move ball away from paddle to prevent multiple collisions
        # Position ball just outside the paddle based on which side was hit
        if hit_from_left:
            # Ball hit left side of paddle, place it to the left
            self.x = paddle_left - self.size // 2 - 1
        else:
            # Ball hit right side of paddle, place it to the right
            self.x = paddle_right + self.size // 2 + 1

        return True

    def is_out_left(self) -> bool:
        """Check if ball went out on the left side.

        Returns:
            True if ball is out on the left
        """
        return self.x + self.size // 2 < 0

    def is_out_right(self) -> bool:
        """Check if ball went out on the right side.

        Returns:
            True if ball is out on the right
        """
        return self.x - self.size // 2 > WINDOW_WIDTH

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the ball on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        pygame.draw.rect(surface, WHITE, self.rect)

    def reset(self, x: int, y: int) -> None:
        """Reset the ball to a specific position with new velocity.

        Args:
            x: New X position
            y: New Y position
        """
        self.x = x
        self.y = y
        self.reset_velocity()

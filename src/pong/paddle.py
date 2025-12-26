"""Paddle class for Pong game."""

import pygame
from pong.constants import (
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    WHITE,
    WINDOW_HEIGHT,
)


class Paddle:
    """Represents a paddle in the game."""

    def __init__(self, x: int, y: int, speed: int = PADDLE_SPEED):
        """Initialize the paddle.

        Args:
            x: X position of the paddle
            y: Y position of the paddle
            speed: Movement speed of the paddle
        """
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = speed
        self.velocity = 0

    @property
    def rect(self) -> pygame.Rect:
        """Get the paddle's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def center_y(self) -> float:
        """Get the Y coordinate of the paddle's center."""
        return self.y + self.height / 2

    def move_up(self) -> None:
        """Move the paddle up."""
        self.velocity = -self.speed

    def move_down(self) -> None:
        """Move the paddle down."""
        self.velocity = self.speed

    def stop(self) -> None:
        """Stop the paddle movement."""
        self.velocity = 0

    def update(self) -> None:
        """Update the paddle position based on velocity."""
        self.y += self.velocity

        # Keep paddle within screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the paddle on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        pygame.draw.rect(surface, WHITE, self.rect)

    def reset(self, x: int, y: int) -> None:
        """Reset the paddle to a specific position.

        Args:
            x: New X position
            y: New Y position
        """
        self.x = x
        self.y = y
        self.velocity = 0

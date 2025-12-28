"""Paddle class for Pong game."""

import pygame
from pong.constants import (
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Paddle:
    """Represents a paddle in the game."""

    def __init__(
        self,
        x: int,
        y: int,
        speed: int = PADDLE_SPEED,
        min_x: int = 0,
        max_x: int | None = None,
    ):
        """Initialize the paddle.

        Args:
            x: X position of the paddle
            y: Y position of the paddle
            speed: Movement speed of the paddle
            min_x: Minimum X boundary (default: 0)
            max_x: Maximum X boundary (default: WINDOW_WIDTH)
        """
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = speed
        self.velocity_y = 0
        self.velocity_x = 0
        self.min_x = min_x
        self.max_x = max_x if max_x is not None else WINDOW_WIDTH

    @property
    def rect(self) -> pygame.Rect:
        """Get the paddle's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def center_y(self) -> float:
        """Get the Y coordinate of the paddle's center."""
        return self.y + self.height / 2

    @property
    def center_x(self) -> float:
        """Get the X coordinate of the paddle's center."""
        return self.x + self.width / 2

    def move_up(self) -> None:
        """Move the paddle up."""
        self.velocity_y = -self.speed

    def move_down(self) -> None:
        """Move the paddle down."""
        self.velocity_y = self.speed

    def move_left(self) -> None:
        """Move the paddle left."""
        self.velocity_x = -self.speed

    def move_right(self) -> None:
        """Move the paddle right."""
        self.velocity_x = self.speed

    def stop_y(self) -> None:
        """Stop the paddle Y movement."""
        self.velocity_y = 0

    def stop_x(self) -> None:
        """Stop the paddle X movement."""
        self.velocity_x = 0

    def stop(self) -> None:
        """Stop all paddle movement."""
        self.velocity_y = 0
        self.velocity_x = 0

    def update(self) -> None:
        """Update the paddle position based on velocity."""
        self.y += self.velocity_y
        self.x += self.velocity_x

        # Keep paddle within Y bounds
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height

        # Keep paddle within X bounds
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x + self.width > self.max_x:
            self.x = self.max_x - self.width

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
        self.velocity_y = 0
        self.velocity_x = 0

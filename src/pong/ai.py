"""AI player for Pong game."""

import random
from enum import Enum
from pong.paddle import Paddle
from pong.ball import Ball
from pong.constants import (
    AI_SPEED,
    AI_REACTION_ZONE,
    AI_AGGRESSIVE_OFFSET,
    AI_BALL_REACTIVE_FORWARD_OFFSET,
    AI_BALL_REACTIVE_BACK_OFFSET,
    WINDOW_WIDTH,
    DOUBLES_PADDLE_OFFSET_X,
    PADDLE_WIDTH,
)


class AIStrategy(Enum):
    """AI positioning strategies for doubles mode."""

    DEFENSIVE = "defensive"  # Stay back near goal
    BALANCED = "balanced"  # Stay in middle of half
    AGGRESSIVE = "aggressive"  # Move forward toward net
    BALL_REACTIVE = "ball_reactive"  # Adjust based on ball velocity


class AIPlayer:
    """AI player that controls a paddle."""

    def __init__(
        self,
        paddle: Paddle,
        difficulty: str = "medium",
        doubles_mode: bool = False,
        zone: str | None = None,
        zone_center_y: int | None = None,
    ):
        """Initialize the AI player.

        Args:
            paddle: The paddle controlled by the AI
            difficulty: Difficulty level ('easy', 'medium', 'hard')
            doubles_mode: Enable 2D movement for doubles mode
            zone: Defensive zone ('top' or 'bottom') for doubles mode
            zone_center_y: Y coordinate of the center of defensive zone
        """
        self.paddle = paddle
        self.difficulty = difficulty
        self.doubles_mode = doubles_mode
        self.zone = zone
        self.zone_center_y = zone_center_y
        self.strategy = AIStrategy.BALANCED  # Default strategy
        self._set_difficulty_params()

    def randomize_strategy(self) -> None:
        """Randomly select a new positioning strategy."""
        self.strategy = random.choice(list(AIStrategy))

    def _set_difficulty_params(self) -> None:
        """Set parameters based on difficulty level."""
        if self.difficulty == "easy":
            self.speed = AI_SPEED - 1
            self.reaction_zone = AI_REACTION_ZONE + 20
        elif self.difficulty == "hard":
            self.speed = AI_SPEED + 1
            self.reaction_zone = AI_REACTION_ZONE - 15
        else:  # medium
            self.speed = AI_SPEED
            self.reaction_zone = AI_REACTION_ZONE

    def update(self, ball: Ball) -> None:
        """Update AI paddle position based on ball position.

        Args:
            ball: The ball to track
        """
        if self.doubles_mode:
            # 2D movement for doubles mode with zone-based strategy
            # Y-axis movement - zone-based positioning
            if self.zone and self.zone_center_y is not None:
                # Determine target Y position based on ball and zone
                # If ball is in our zone, track it; otherwise, return to zone center
                zone_height = 150  # Height of defensive zone

                # Check if ball is in our zone
                if self.zone == "top":
                    in_zone = ball.y < self.zone_center_y + zone_height / 2
                else:  # bottom
                    in_zone = ball.y > self.zone_center_y - zone_height / 2

                if in_zone:
                    # Ball in our zone - track it aggressively
                    target_y = ball.y
                else:
                    # Ball in teammate's zone - return to zone center
                    target_y = self.zone_center_y

                diff_y = target_y - self.paddle.center_y
                if abs(diff_y) < self.reaction_zone:
                    self.paddle.stop_y()
                else:
                    if diff_y < 0:
                        self.paddle.velocity_y = -self.speed
                    else:
                        self.paddle.velocity_y = self.speed
            else:
                # No zone - track ball normally
                diff_y = ball.y - self.paddle.center_y
                if abs(diff_y) < self.reaction_zone:
                    self.paddle.stop_y()
                else:
                    if diff_y < 0:
                        self.paddle.velocity_y = -self.speed
                    else:
                        self.paddle.velocity_y = self.speed

            # X-axis movement - strategy-based positioning
            target_x = self._calculate_target_x(ball)
            diff_x = target_x - self.paddle.center_x
            if abs(diff_x) < self.reaction_zone:
                self.paddle.stop_x()
            else:
                if diff_x < 0:
                    self.paddle.velocity_x = -self.speed
                else:
                    self.paddle.velocity_x = self.speed
        else:
            # Standard 1D movement (Y-axis only)
            diff = ball.y - self.paddle.center_y

            # Stop paddle if within reaction zone
            if abs(diff) < self.reaction_zone:
                self.paddle.stop()
                return

            # Move paddle toward ball
            if diff < 0:
                self.paddle.velocity_y = -self.speed
            else:
                self.paddle.velocity_y = self.speed

    def _calculate_target_x(self, ball: Ball) -> float:
        """Calculate target X position based on current strategy.

        Args:
            ball: The ball to track

        Returns:
            Target X position for the paddle
        """
        # Determine if paddle is on right side (assumes right side for doubles)
        on_right_side = self.paddle.x > WINDOW_WIDTH // 2

        if self.strategy == AIStrategy.DEFENSIVE:
            # Stay back near goal
            if on_right_side:
                return WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH
            else:
                return DOUBLES_PADDLE_OFFSET_X

        elif self.strategy == AIStrategy.BALANCED:
            # Stay in middle of half
            if on_right_side:
                # Middle of right half
                return (WINDOW_WIDTH // 2 + WINDOW_WIDTH) // 2
            else:
                # Middle of left half
                return WINDOW_WIDTH // 4

        elif self.strategy == AIStrategy.AGGRESSIVE:
            # Move forward toward net
            if on_right_side:
                return WINDOW_WIDTH // 2 + AI_AGGRESSIVE_OFFSET
            else:
                return WINDOW_WIDTH // 2 - AI_AGGRESSIVE_OFFSET

        elif self.strategy == AIStrategy.BALL_REACTIVE:
            # Adjust based on ball velocity
            if on_right_side:
                # Ball moving toward AI (left)
                if ball.vx < 0:
                    return WINDOW_WIDTH // 2 + AI_BALL_REACTIVE_FORWARD_OFFSET
                # Ball moving away from AI (right)
                else:
                    return WINDOW_WIDTH - AI_BALL_REACTIVE_BACK_OFFSET
            else:
                # Ball moving toward AI (right)
                if ball.vx > 0:
                    return WINDOW_WIDTH // 2 - AI_BALL_REACTIVE_FORWARD_OFFSET
                # Ball moving away from AI (left)
                else:
                    return AI_BALL_REACTIVE_BACK_OFFSET

        # Default: track ball directly
        return ball.x

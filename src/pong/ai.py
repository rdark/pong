"""AI player for Pong game."""

from pong.paddle import Paddle
from pong.ball import Ball
from pong.constants import AI_SPEED, AI_REACTION_ZONE


class AIPlayer:
    """AI player that controls a paddle."""

    def __init__(self, paddle: Paddle, difficulty: str = "medium"):
        """Initialize the AI player.

        Args:
            paddle: The paddle controlled by the AI
            difficulty: Difficulty level ('easy', 'medium', 'hard')
        """
        self.paddle = paddle
        self.difficulty = difficulty
        self._set_difficulty_params()

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
        # Get the difference between ball and paddle center
        diff = ball.y - self.paddle.center_y

        # Stop paddle if within reaction zone
        if abs(diff) < self.reaction_zone:
            self.paddle.stop()
            return

        # Move paddle toward ball
        if diff < 0:
            self.paddle.velocity = -self.speed
        else:
            self.paddle.velocity = self.speed

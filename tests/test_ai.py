"""Tests for the AIPlayer class."""

import pygame
import pytest
from pong.ai import AIPlayer
from pong.paddle import Paddle
from pong.ball import Ball
from pong.constants import AI_SPEED, AI_REACTION_ZONE


@pytest.fixture
def paddle():
    """Create a test paddle."""
    pygame.init()
    return Paddle(x=750, y=250)


@pytest.fixture
def ball():
    """Create a test ball."""
    pygame.init()
    return Ball(x=400, y=300)


@pytest.fixture
def ai(paddle):
    """Create a test AI player."""
    return AIPlayer(paddle)


def test_ai_initialization(ai, paddle):
    """Test that AI initializes with correct attributes."""
    assert ai.paddle == paddle
    assert ai.difficulty == "medium"
    assert ai.speed == AI_SPEED
    assert ai.reaction_zone == AI_REACTION_ZONE


def test_ai_easy_difficulty(paddle):
    """Test that easy difficulty sets correct parameters."""
    ai = AIPlayer(paddle, difficulty="easy")
    assert ai.speed == AI_SPEED - 1
    assert ai.reaction_zone == AI_REACTION_ZONE + 20


def test_ai_medium_difficulty(paddle):
    """Test that medium difficulty sets correct parameters."""
    ai = AIPlayer(paddle, difficulty="medium")
    assert ai.speed == AI_SPEED
    assert ai.reaction_zone == AI_REACTION_ZONE


def test_ai_hard_difficulty(paddle):
    """Test that hard difficulty sets correct parameters."""
    ai = AIPlayer(paddle, difficulty="hard")
    assert ai.speed == AI_SPEED + 1
    assert ai.reaction_zone == AI_REACTION_ZONE - 15


def test_ai_moves_paddle_up_when_ball_above(ai, paddle, ball):
    """Test that AI moves paddle up when ball is above it."""
    paddle.y = 300
    ball.y = 100
    ai.update(ball)
    assert paddle.velocity_y < 0


def test_ai_moves_paddle_down_when_ball_below(ai, paddle, ball):
    """Test that AI moves paddle down when ball is below it."""
    paddle.y = 100
    ball.y = 300
    ai.update(ball)
    assert paddle.velocity_y > 0


def test_ai_stops_paddle_within_reaction_zone(ai, paddle, ball):
    """Test that AI stops paddle when ball is within reaction zone."""
    paddle.y = 250
    # Paddle center is at 250 + 50 = 300
    # Set ball within reaction zone (30 pixels)
    ball.y = 310  # 10 pixels from center, within 30 pixel zone
    ai.update(ball)
    assert paddle.velocity_y == 0


def test_ai_tracks_ball_movement(ai, paddle, ball):
    """Test that AI tracks the ball as it moves."""
    # Ball above paddle
    paddle.y = 300
    ball.y = 100
    ai.update(ball)
    assert paddle.velocity_y < 0

    # Ball moves below paddle
    ball.y = 400
    ai.update(ball)
    assert paddle.velocity_y > 0


def test_ai_uses_custom_speed(ai, paddle, ball):
    """Test that AI uses its configured speed."""
    paddle.y = 100
    ball.y = 400
    ai.update(ball)
    assert paddle.velocity_y == ai.speed


def test_ai_easy_has_larger_reaction_zone(paddle, ball):
    """Test that easy AI has larger reaction zone."""
    easy_ai = AIPlayer(paddle, difficulty="easy")
    medium_ai = AIPlayer(paddle, difficulty="medium")

    assert easy_ai.reaction_zone > medium_ai.reaction_zone


def test_ai_hard_has_smaller_reaction_zone(paddle, ball):
    """Test that hard AI has smaller reaction zone."""
    hard_ai = AIPlayer(paddle, difficulty="hard")
    medium_ai = AIPlayer(paddle, difficulty="medium")

    assert hard_ai.reaction_zone < medium_ai.reaction_zone


def test_ai_easy_is_slower(paddle):
    """Test that easy AI is slower."""
    easy_ai = AIPlayer(paddle, difficulty="easy")
    medium_ai = AIPlayer(paddle, difficulty="medium")

    assert easy_ai.speed < medium_ai.speed


def test_ai_hard_is_faster(paddle):
    """Test that hard AI is faster."""
    hard_ai = AIPlayer(paddle, difficulty="hard")
    medium_ai = AIPlayer(paddle, difficulty="medium")

    assert hard_ai.speed > medium_ai.speed


def test_ai_reaction_zone_boundary_upper(ai, paddle, ball):
    """Test AI stops exactly at reaction zone upper boundary."""
    paddle.y = 250
    ball.y = paddle.center_y - ai.reaction_zone + 1
    ai.update(ball)
    assert paddle.velocity_y == 0


def test_ai_reaction_zone_boundary_lower(ai, paddle, ball):
    """Test AI stops exactly at reaction zone lower boundary."""
    paddle.y = 250
    ball.y = paddle.center_y + ai.reaction_zone - 1
    ai.update(ball)
    assert paddle.velocity_y == 0


def test_ai_outside_reaction_zone_upper(ai, paddle, ball):
    """Test AI moves when ball is just outside reaction zone (above)."""
    paddle.y = 250
    ball.y = paddle.center_y - ai.reaction_zone - 1
    ai.update(ball)
    assert paddle.velocity_y < 0


def test_ai_outside_reaction_zone_lower(ai, paddle, ball):
    """Test AI moves when ball is just outside reaction zone (below)."""
    paddle.y = 250
    ball.y = paddle.center_y + ai.reaction_zone + 1
    ai.update(ball)
    assert paddle.velocity_y > 0


def test_ai_doubles_mode_initialization(paddle):
    """Test that AI can be initialized in doubles mode."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    assert ai.doubles_mode is True


def test_ai_doubles_mode_moves_y_axis(paddle, ball):
    """Test that AI in doubles mode moves on Y axis."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    paddle.y = 100
    ball.y = 400
    ball.x = 400
    ai.update(ball)
    assert paddle.velocity_y > 0


def test_ai_doubles_mode_moves_x_axis(paddle, ball):
    """Test that AI in doubles mode moves on X axis."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    paddle.x = 100
    ball.x = 400
    ball.y = paddle.center_y  # Within Y reaction zone
    ai.update(ball)
    assert paddle.velocity_x > 0


def test_ai_doubles_mode_stops_y_within_zone(paddle, ball):
    """Test that AI in doubles mode stops Y when within zone."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    paddle.y = 250
    ball.y = paddle.center_y + 10  # Within reaction zone
    ball.x = 400
    ai.update(ball)
    assert paddle.velocity_y == 0


def test_ai_doubles_mode_stops_x_within_zone(paddle, ball):
    """Test that AI in doubles mode stops X when at target position."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    # Position paddle at the balanced strategy target (3/4 of window width for right side)
    # Assuming WINDOW_WIDTH = 800, target is 600
    paddle.x = 595  # Close to target of 600
    ball.x = 400
    ball.y = 400
    ai.update(ball)
    # Should stop X movement when within reaction zone of target
    assert paddle.velocity_x == 0


def test_ai_doubles_mode_2d_tracking(paddle, ball):
    """Test that AI in doubles mode tracks ball in 2D."""
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    paddle.x = 100
    paddle.y = 100
    ball.x = 400
    ball.y = 400
    ai.update(ball)
    # Both velocities should be positive (moving right and down)
    assert paddle.velocity_x > 0
    assert paddle.velocity_y > 0


def test_ai_randomize_strategy(paddle):
    """Test that AI can randomize its strategy."""
    from pong.ai import AIStrategy
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    initial_strategy = ai.strategy
    # Randomize multiple times to ensure it changes
    strategies = set()
    for _ in range(20):
        ai.randomize_strategy()
        strategies.add(ai.strategy)
    # Should have multiple strategies after 20 randomizations
    assert len(strategies) > 1


def test_ai_defensive_strategy_positioning(paddle, ball):
    """Test that defensive strategy keeps AI back."""
    from pong.ai import AIStrategy
    from pong.constants import WINDOW_WIDTH, DOUBLES_PADDLE_OFFSET_X, PADDLE_WIDTH
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    ai.strategy = AIStrategy.DEFENSIVE
    paddle.x = 500  # Right side, forward position
    ball.x = 400
    ball.y = 300
    ai.update(ball)
    # Should move toward back of court (higher X)
    # Target is WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH = 800 - 60 - 10 = 730
    assert paddle.velocity_x > 0  # Moving right (back)


def test_ai_aggressive_strategy_positioning(paddle, ball):
    """Test that aggressive strategy moves AI forward."""
    from pong.ai import AIStrategy
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    ai.strategy = AIStrategy.AGGRESSIVE
    paddle.x = 700  # Right side, back position
    ball.x = 400
    ball.y = 300
    ai.update(ball)
    # Should move toward net (lower X)
    assert paddle.velocity_x < 0  # Moving left (forward)


def test_ai_balanced_strategy_positioning(paddle, ball):
    """Test that balanced strategy keeps AI in middle."""
    from pong.ai import AIStrategy
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    ai.strategy = AIStrategy.BALANCED
    # Position paddle far from balanced position (600 for right side)
    paddle.x = 450  # Right side, too far forward
    ball.x = 400
    ball.y = 300
    ai.update(ball)
    # Should move toward middle of right half (600)
    assert paddle.velocity_x > 0  # Moving right toward center


def test_ai_ball_reactive_strategy_forward(paddle, ball):
    """Test that ball-reactive strategy moves forward when ball approaches."""
    from pong.ai import AIStrategy
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    ai.strategy = AIStrategy.BALL_REACTIVE
    paddle.x = 700  # Right side, back position
    ball.x = 600
    ball.vx = -3  # Ball moving left (toward AI)
    ball.y = 300
    ai.update(ball)
    # Should move forward since ball is approaching
    assert paddle.velocity_x < 0  # Moving left (forward)


def test_ai_ball_reactive_strategy_back(paddle, ball):
    """Test that ball-reactive strategy stays back when ball moves away."""
    from pong.ai import AIStrategy
    ai = AIPlayer(paddle, difficulty="medium", doubles_mode=True)
    ai.strategy = AIStrategy.BALL_REACTIVE
    paddle.x = 500  # Right side, forward position
    ball.x = 600
    ball.vx = 3  # Ball moving right (away from AI)
    ball.y = 300
    ai.update(ball)
    # Should move back since ball is moving away
    assert paddle.velocity_x > 0  # Moving right (back)

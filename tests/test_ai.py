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
    assert paddle.velocity < 0


def test_ai_moves_paddle_down_when_ball_below(ai, paddle, ball):
    """Test that AI moves paddle down when ball is below it."""
    paddle.y = 100
    ball.y = 300
    ai.update(ball)
    assert paddle.velocity > 0


def test_ai_stops_paddle_within_reaction_zone(ai, paddle, ball):
    """Test that AI stops paddle when ball is within reaction zone."""
    paddle.y = 250
    # Paddle center is at 250 + 50 = 300
    # Set ball within reaction zone (30 pixels)
    ball.y = 310  # 10 pixels from center, within 30 pixel zone
    ai.update(ball)
    assert paddle.velocity == 0


def test_ai_tracks_ball_movement(ai, paddle, ball):
    """Test that AI tracks the ball as it moves."""
    # Ball above paddle
    paddle.y = 300
    ball.y = 100
    ai.update(ball)
    assert paddle.velocity < 0

    # Ball moves below paddle
    ball.y = 400
    ai.update(ball)
    assert paddle.velocity > 0


def test_ai_uses_custom_speed(ai, paddle, ball):
    """Test that AI uses its configured speed."""
    paddle.y = 100
    ball.y = 400
    ai.update(ball)
    assert paddle.velocity == ai.speed


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
    assert paddle.velocity == 0


def test_ai_reaction_zone_boundary_lower(ai, paddle, ball):
    """Test AI stops exactly at reaction zone lower boundary."""
    paddle.y = 250
    ball.y = paddle.center_y + ai.reaction_zone - 1
    ai.update(ball)
    assert paddle.velocity == 0


def test_ai_outside_reaction_zone_upper(ai, paddle, ball):
    """Test AI moves when ball is just outside reaction zone (above)."""
    paddle.y = 250
    ball.y = paddle.center_y - ai.reaction_zone - 1
    ai.update(ball)
    assert paddle.velocity < 0


def test_ai_outside_reaction_zone_lower(ai, paddle, ball):
    """Test AI moves when ball is just outside reaction zone (below)."""
    paddle.y = 250
    ball.y = paddle.center_y + ai.reaction_zone + 1
    ai.update(ball)
    assert paddle.velocity > 0

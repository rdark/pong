"""Tests for the Ball class."""

import math
import pygame
import pytest
from pong.ball import Ball
from pong.paddle import Paddle
from pong.constants import (
    BALL_SIZE,
    BALL_INITIAL_SPEED,
    BALL_MAX_SPEED,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


@pytest.fixture
def ball():
    """Create a test ball."""
    pygame.init()
    return Ball(x=400, y=300)


@pytest.fixture
def paddle():
    """Create a test paddle."""
    pygame.init()
    return Paddle(x=100, y=250)


def test_ball_initialization(ball):
    """Test that ball initializes with correct attributes."""
    assert ball.x == 400
    assert ball.y == 300
    assert ball.size == BALL_SIZE
    assert ball.speed == BALL_INITIAL_SPEED
    # Velocity should be set by reset_velocity
    assert ball.vx != 0
    assert abs(ball.vy) >= 0  # Can be 0 if angle is exactly 0


def test_ball_rect(ball):
    """Test that ball rect is correct."""
    rect = ball.rect
    assert rect.centerx == ball.x
    assert rect.centery == ball.y
    assert rect.width == BALL_SIZE
    assert rect.height == BALL_SIZE


def test_ball_reset_velocity(ball):
    """Test that reset_velocity sets velocity correctly."""
    ball.vx = 0
    ball.vy = 0
    ball.reset_velocity()
    # Should have non-zero horizontal velocity
    assert ball.vx != 0
    # Speed should be reset to initial
    assert ball.speed == BALL_INITIAL_SPEED
    # Check that velocity magnitude is approximately equal to speed
    magnitude = math.sqrt(ball.vx**2 + ball.vy**2)
    assert abs(magnitude - BALL_INITIAL_SPEED) < 0.1


def test_ball_update_moves_ball(ball):
    """Test that update moves the ball based on velocity."""
    initial_x = ball.x
    initial_y = ball.y
    vx, vy = ball.vx, ball.vy
    ball.update()
    assert ball.x == initial_x + vx
    assert ball.y == initial_y + vy


def test_ball_bounces_off_top_wall(ball):
    """Test that ball bounces off the top wall."""
    ball.y = 5
    ball.vy = -5
    ball.update()
    assert ball.y == BALL_SIZE // 2
    assert ball.vy == 5  # Should be positive now


def test_ball_bounces_off_bottom_wall(ball):
    """Test that ball bounces off the bottom wall."""
    ball.y = WINDOW_HEIGHT - 5
    ball.vy = 5
    ball.update()
    assert ball.y == WINDOW_HEIGHT - BALL_SIZE // 2
    assert ball.vy == -5  # Should be negative now


def test_ball_paddle_collision_detected(ball, paddle):
    """Test that paddle collision is detected."""
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height // 2
    ball.vx = -5
    collision = ball.check_paddle_collision(paddle)
    assert collision is True


def test_ball_paddle_collision_reverses_direction(ball, paddle):
    """Test that paddle collision reverses horizontal direction."""
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height // 2
    ball.vx = -5
    ball.check_paddle_collision(paddle)
    assert ball.vx > 0  # Should be moving right now


def test_ball_paddle_collision_increases_speed(ball, paddle):
    """Test that paddle collision increases ball speed."""
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height // 2
    ball.vx = -5
    initial_speed = ball.speed
    ball.check_paddle_collision(paddle)
    assert ball.speed > initial_speed


def test_ball_paddle_collision_max_speed(ball, paddle):
    """Test that ball speed doesn't exceed maximum."""
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height // 2
    ball.vx = -5
    ball.speed = BALL_MAX_SPEED - 0.1

    ball.check_paddle_collision(paddle)
    assert ball.speed <= BALL_MAX_SPEED


def test_ball_paddle_collision_affects_angle(ball, paddle):
    """Test that hit position affects ball angle."""
    # Hit at top of paddle
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + 10
    ball.vx = -5
    ball.vy = 0
    ball.check_paddle_collision(paddle)
    # Should have negative vy (moving up)
    assert ball.vy < 0

    # Reset and hit at bottom
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height - 10
    ball.vx = -5
    ball.vy = 0
    ball.check_paddle_collision(paddle)
    # Should have positive vy (moving down)
    assert ball.vy > 0


def test_ball_no_collision_when_not_touching(ball, paddle):
    """Test that no collision is detected when ball doesn't touch paddle."""
    ball.x = paddle.x + paddle.width + 50
    ball.y = paddle.y + paddle.height // 2
    collision = ball.check_paddle_collision(paddle)
    assert collision is False


def test_ball_is_out_left(ball):
    """Test that is_out_left detects when ball leaves left side."""
    ball.x = -10
    assert ball.is_out_left() is True
    ball.x = 50
    assert ball.is_out_left() is False


def test_ball_is_out_right(ball):
    """Test that is_out_right detects when ball leaves right side."""
    ball.x = WINDOW_WIDTH + 10
    assert ball.is_out_right() is True
    ball.x = WINDOW_WIDTH - 50
    assert ball.is_out_right() is False


def test_ball_reset(ball):
    """Test that reset moves ball to new position and resets velocity."""
    ball.vx = 10
    ball.vy = 10
    ball.speed = 10
    ball.reset(500, 400)
    assert ball.x == 500
    assert ball.y == 400
    assert ball.speed == BALL_INITIAL_SPEED
    # Velocity should be reset
    magnitude = math.sqrt(ball.vx**2 + ball.vy**2)
    assert abs(magnitude - BALL_INITIAL_SPEED) < 0.1


def test_ball_draw():
    """Test that ball draw method works without errors."""
    pygame.init()
    surface = pygame.Surface((800, 600))
    ball = Ball(400, 300)
    # Should not raise any exceptions
    ball.draw(surface)


def test_ball_multiple_bounces(ball):
    """Test ball bouncing multiple times."""
    ball.y = 5
    ball.vy = -5
    ball.update()  # First bounce
    assert ball.vy > 0
    old_vy = ball.vy

    # Move to bottom
    ball.y = WINDOW_HEIGHT - 5
    ball.update()  # Second bounce
    assert ball.vy < 0


def test_ball_paddle_collision_moves_ball_away(ball, paddle):
    """Test that collision moves ball away from paddle to prevent multiple hits."""
    ball.x = paddle.x + paddle.width
    ball.y = paddle.y + paddle.height // 2
    ball.vx = -5
    ball.check_paddle_collision(paddle)
    # Ball should be moved away from paddle
    assert ball.x > paddle.x + paddle.width


def test_ball_velocity_direction_randomness():
    """Test that ball can start in different directions."""
    pygame.init()
    directions = set()
    for _ in range(10):
        test_ball = Ball(400, 300)
        direction = 1 if test_ball.vx > 0 else -1
        directions.add(direction)
    # Should have both directions after 10 attempts
    assert len(directions) == 2

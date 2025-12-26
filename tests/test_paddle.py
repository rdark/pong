"""Tests for the Paddle class."""

import pygame
import pytest
from pong.paddle import Paddle
from pong.constants import PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, WINDOW_HEIGHT


@pytest.fixture
def paddle():
    """Create a test paddle."""
    pygame.init()
    return Paddle(x=100, y=250)


def test_paddle_initialization(paddle):
    """Test that paddle initializes with correct attributes."""
    assert paddle.x == 100
    assert paddle.y == 250
    assert paddle.width == PADDLE_WIDTH
    assert paddle.height == PADDLE_HEIGHT
    assert paddle.speed == PADDLE_SPEED
    assert paddle.velocity == 0


def test_paddle_rect(paddle):
    """Test that paddle rect is correct."""
    rect = paddle.rect
    assert rect.x == 100
    assert rect.y == 250
    assert rect.width == PADDLE_WIDTH
    assert rect.height == PADDLE_HEIGHT


def test_paddle_center_y(paddle):
    """Test that paddle center_y is calculated correctly."""
    assert paddle.center_y == 250 + PADDLE_HEIGHT / 2


def test_paddle_move_up(paddle):
    """Test that move_up sets velocity correctly."""
    paddle.move_up()
    assert paddle.velocity == -PADDLE_SPEED


def test_paddle_move_down(paddle):
    """Test that move_down sets velocity correctly."""
    paddle.move_down()
    assert paddle.velocity == PADDLE_SPEED


def test_paddle_stop(paddle):
    """Test that stop sets velocity to zero."""
    paddle.move_up()
    paddle.stop()
    assert paddle.velocity == 0


def test_paddle_update_moves_paddle(paddle):
    """Test that update moves the paddle based on velocity."""
    initial_y = paddle.y
    paddle.move_down()
    paddle.update()
    assert paddle.y == initial_y + PADDLE_SPEED


def test_paddle_update_respects_top_boundary(paddle):
    """Test that paddle stops at top of screen."""
    paddle.y = 5
    paddle.move_up()
    paddle.update()
    assert paddle.y == 0


def test_paddle_update_respects_bottom_boundary(paddle):
    """Test that paddle stops at bottom of screen."""
    paddle.y = WINDOW_HEIGHT - PADDLE_HEIGHT + 5
    paddle.move_down()
    paddle.update()
    assert paddle.y == WINDOW_HEIGHT - PADDLE_HEIGHT


def test_paddle_reset(paddle):
    """Test that reset moves paddle to new position and stops it."""
    paddle.move_down()
    paddle.update()
    paddle.reset(200, 300)
    assert paddle.x == 200
    assert paddle.y == 300
    assert paddle.velocity == 0


def test_paddle_custom_speed():
    """Test that paddle can be initialized with custom speed."""
    pygame.init()
    custom_paddle = Paddle(x=100, y=250, speed=10)
    assert custom_paddle.speed == 10
    custom_paddle.move_up()
    assert custom_paddle.velocity == -10


def test_paddle_draw():
    """Test that paddle draw method works without errors."""
    pygame.init()
    surface = pygame.Surface((800, 600))
    paddle = Paddle(100, 250)
    # Should not raise any exceptions
    paddle.draw(surface)


def test_paddle_multiple_updates(paddle):
    """Test paddle movement over multiple updates."""
    paddle.move_down()
    initial_y = paddle.y
    for _ in range(5):
        paddle.update()
    assert paddle.y == initial_y + (PADDLE_SPEED * 5)


def test_paddle_boundary_stays_at_zero(paddle):
    """Test that paddle stays at y=0 after hitting top boundary."""
    paddle.y = 0
    paddle.move_up()
    paddle.update()
    paddle.update()
    paddle.update()
    assert paddle.y == 0


def test_paddle_boundary_stays_at_bottom(paddle):
    """Test that paddle stays at bottom after hitting boundary."""
    paddle.y = WINDOW_HEIGHT - PADDLE_HEIGHT
    paddle.move_down()
    paddle.update()
    paddle.update()
    paddle.update()
    assert paddle.y == WINDOW_HEIGHT - PADDLE_HEIGHT

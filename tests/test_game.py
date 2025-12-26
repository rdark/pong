"""Tests for the Game class."""

import pygame
import pytest
from pong.game import Game, GameMode, GameState
from pong.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINNING_SCORE, FPS


@pytest.fixture
def game():
    """Create a test game."""
    pygame.init()
    return Game()


def test_game_initialization(game):
    """Test that game initializes with correct attributes."""
    assert game.running is True
    assert game.state == GameState.MENU
    assert game.mode == GameMode.TWO_PLAYER
    assert game.score_left == 0
    assert game.score_right == 0
    assert game.paddle_left is not None
    assert game.paddle_right is not None
    assert game.ball is not None
    assert game.ai is not None


def test_game_set_mode_to_one_player(game):
    """Test setting game mode to 1P."""
    game.set_mode(GameMode.ONE_PLAYER)
    assert game.mode == GameMode.ONE_PLAYER


def test_game_set_mode_to_two_player(game):
    """Test setting game mode to 2P."""
    game.set_mode(GameMode.TWO_PLAYER)
    assert game.mode == GameMode.TWO_PLAYER


def test_game_start_game(game):
    """Test starting a new game."""
    game.score_left = 5
    game.score_right = 3
    game.start_game()
    assert game.state == GameState.PLAYING
    assert game.score_left == 0
    assert game.score_right == 0


def test_game_toggle_mode_to_one_player(game):
    """Test toggling mode from 2P to 1P."""
    game.mode = GameMode.TWO_PLAYER
    game.toggle_mode()
    assert game.mode == GameMode.ONE_PLAYER


def test_game_toggle_mode_to_two_player(game):
    """Test toggling mode from 1P to 2P."""
    game.mode = GameMode.ONE_PLAYER
    game.toggle_mode()
    assert game.mode == GameMode.TWO_PLAYER


def test_game_return_to_menu(game):
    """Test returning to menu."""
    game.state = GameState.PLAYING
    game.score_left = 5
    game.score_right = 3
    game.return_to_menu()
    assert game.state == GameState.MENU
    assert game.score_left == 0
    assert game.score_right == 0


def test_game_quit(game):
    """Test quitting the game."""
    game.quit()
    assert game.running is False


def test_game_get_fps(game):
    """Test getting FPS."""
    assert game.get_fps() == FPS


def test_game_handle_input_player1_up(game):
    """Test handling player 1 up input."""
    game.start_game()
    keys = pygame.key.get_pressed()
    # Simulate W key press
    keys_dict = {pygame.K_w: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    assert game.paddle_left.velocity < 0


def test_game_handle_input_player1_down(game):
    """Test handling player 1 down input."""
    game.start_game()
    keys_dict = {pygame.K_s: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    assert game.paddle_left.velocity > 0


def test_game_handle_input_player2_up(game):
    """Test handling player 2 up input in 2P mode."""
    game.mode = GameMode.TWO_PLAYER
    game.start_game()
    keys_dict = {pygame.K_UP: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    assert game.paddle_right.velocity < 0


def test_game_handle_input_player2_down(game):
    """Test handling player 2 down input in 2P mode."""
    game.mode = GameMode.TWO_PLAYER
    game.start_game()
    keys_dict = {pygame.K_DOWN: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    assert game.paddle_right.velocity > 0


def test_game_handle_input_player2_ignored_in_1p(game):
    """Test that player 2 input is ignored in 1P mode."""
    game.mode = GameMode.ONE_PLAYER
    game.start_game()
    initial_velocity = game.paddle_right.velocity
    keys_dict = {pygame.K_UP: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    # In 1P mode, paddle_right should not respond to arrow keys
    assert game.paddle_right.velocity == initial_velocity


def test_game_handle_input_no_keys(game):
    """Test handling input when no keys are pressed."""
    game.start_game()
    game.paddle_left.velocity = 5
    keys_dict = {}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    game.handle_input(KeyWrapper())
    assert game.paddle_left.velocity == 0


def test_game_handle_input_ignores_input_in_menu(game):
    """Test that input is ignored in menu state."""
    game.state = GameState.MENU
    keys_dict = {pygame.K_w: True}

    class KeyWrapper:
        def __getitem__(self, key):
            return keys_dict.get(key, False)

    initial_velocity = game.paddle_left.velocity
    game.handle_input(KeyWrapper())
    assert game.paddle_left.velocity == initial_velocity


def test_game_update_moves_paddles(game):
    """Test that update moves paddles."""
    game.start_game()
    game.paddle_left.move_down()
    initial_y = game.paddle_left.y
    game.update()
    assert game.paddle_left.y > initial_y


def test_game_update_moves_ball(game):
    """Test that update moves ball."""
    game.start_game()
    initial_x = game.ball.x
    game.update()
    assert game.ball.x != initial_x


def test_game_update_ai_in_1p_mode(game):
    """Test that AI updates in 1P mode."""
    game.mode = GameMode.ONE_PLAYER
    game.start_game()
    # Place ball far from AI paddle to trigger movement
    game.ball.y = 100
    game.paddle_right.y = 500
    game.update()
    # AI should set velocity (will be applied on next update)
    assert game.paddle_right.velocity != 0


def test_game_update_no_ai_in_2p_mode(game):
    """Test that AI doesn't control paddle in 2P mode."""
    game.mode = GameMode.TWO_PLAYER
    game.start_game()
    game.paddle_right.velocity = 0
    game.ball.y = 100
    game.paddle_right.y = 500
    game.update()
    # In 2P mode, AI shouldn't control right paddle
    assert game.paddle_right.y == 500


def test_game_update_ignores_updates_in_menu(game):
    """Test that update is ignored in menu state."""
    game.state = GameState.MENU
    initial_ball_x = game.ball.x
    game.update()
    assert game.ball.x == initial_ball_x


def test_game_scoring_left(game):
    """Test scoring for left player."""
    game.start_game()
    initial_score = game.score_left
    # Move ball out on the right side
    game.ball.x = WINDOW_WIDTH + 100
    game.update()
    assert game.score_left == initial_score + 1


def test_game_scoring_right(game):
    """Test scoring for right player."""
    game.start_game()
    initial_score = game.score_right
    # Move ball out on the left side
    game.ball.x = -100
    game.update()
    assert game.score_right == initial_score + 1


def test_game_winning_condition_left(game):
    """Test that game ends when left player reaches winning score."""
    game.start_game()
    game.score_left = WINNING_SCORE - 1
    game.ball.x = WINDOW_WIDTH + 100
    game.update()
    assert game.state == GameState.GAME_OVER


def test_game_winning_condition_right(game):
    """Test that game ends when right player reaches winning score."""
    game.start_game()
    game.score_right = WINNING_SCORE - 1
    game.ball.x = -100
    game.update()
    assert game.state == GameState.GAME_OVER


def test_game_ball_resets_after_scoring(game):
    """Test that ball resets to center after scoring."""
    game.start_game()
    game.ball.x = WINDOW_WIDTH + 100
    game.update()
    # Ball should be reset to center
    assert abs(game.ball.x - WINDOW_WIDTH // 2) < 10


def test_game_draw_returns_surface(game):
    """Test that draw returns a surface."""
    surface = game.draw()
    assert isinstance(surface, pygame.Surface)
    assert surface.get_width() == WINDOW_WIDTH
    assert surface.get_height() == WINDOW_HEIGHT


def test_game_draw_menu(game):
    """Test drawing menu state."""
    game.state = GameState.MENU
    surface = game.draw()
    assert surface is not None


def test_game_draw_playing(game):
    """Test drawing playing state."""
    game.start_game()
    surface = game.draw()
    assert surface is not None


def test_game_draw_game_over(game):
    """Test drawing game over state."""
    game.state = GameState.GAME_OVER
    game.score_left = WINNING_SCORE
    surface = game.draw()
    assert surface is not None


def test_game_paddle_positions_reset(game):
    """Test that paddles reset to center after scoring."""
    game.start_game()
    game.paddle_left.y = 100
    game.paddle_right.y = 400
    game.ball.x = WINDOW_WIDTH + 100
    game.update()
    # Paddles should be back near center
    expected_y = (WINDOW_HEIGHT - 100) // 2  # 100 is paddle height
    assert abs(game.paddle_left.y - expected_y) < 10
    assert abs(game.paddle_right.y - expected_y) < 10

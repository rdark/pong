"""Game class for Pong."""

from enum import Enum
import pygame
from pong.paddle import Paddle
from pong.ball import Ball
from pong.ai import AIPlayer
from pong.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PADDLE_OFFSET,
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    FPS,
    WHITE,
    BLACK,
    GRAY,
    WINNING_SCORE,
    DOUBLES_PADDLE_HEIGHT,
    DOUBLES_PADDLE_OFFSET_X,
    DOUBLES_PADDLE_SPACING_Y,
)


class GameMode(Enum):
    """Game mode enumeration."""

    ONE_PLAYER = "1P"
    TWO_PLAYER = "2P"
    DOUBLES = "Doubles"


class GameState(Enum):
    """Game state enumeration."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    """Main game class that manages the Pong game."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.mode = GameMode.TWO_PLAYER

        # Initialize game objects
        self._init_game_objects()

        # Score
        self.score_left = 0
        self.score_right = 0

        # Fonts
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def _init_game_objects(self) -> None:
        """Initialize paddles, ball, and AI."""
        if self.mode == GameMode.DOUBLES:
            # Doubles mode: 4 paddles (2 humans left, 2 AI right)
            center_y = WINDOW_HEIGHT // 2

            # Left team (humans) - confined to left half
            self.paddle_left_top = Paddle(
                DOUBLES_PADDLE_OFFSET_X,
                center_y - DOUBLES_PADDLE_SPACING_Y,
                min_x=0,
                max_x=WINDOW_WIDTH // 2
            )
            self.paddle_left_bottom = Paddle(
                DOUBLES_PADDLE_OFFSET_X,
                center_y + DOUBLES_PADDLE_SPACING_Y - DOUBLES_PADDLE_HEIGHT,
                min_x=0,
                max_x=WINDOW_WIDTH // 2
            )
            self.paddle_left_top.height = DOUBLES_PADDLE_HEIGHT
            self.paddle_left_bottom.height = DOUBLES_PADDLE_HEIGHT

            # Right team (AI) - confined to right half
            self.paddle_right_top = Paddle(
                WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH,
                center_y - DOUBLES_PADDLE_SPACING_Y,
                min_x=WINDOW_WIDTH // 2,
                max_x=WINDOW_WIDTH
            )
            self.paddle_right_bottom = Paddle(
                WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH,
                center_y + DOUBLES_PADDLE_SPACING_Y - DOUBLES_PADDLE_HEIGHT,
                min_x=WINDOW_WIDTH // 2,
                max_x=WINDOW_WIDTH
            )
            self.paddle_right_top.height = DOUBLES_PADDLE_HEIGHT
            self.paddle_right_bottom.height = DOUBLES_PADDLE_HEIGHT

            # For compatibility, set main paddles to top paddles
            self.paddle_left = self.paddle_left_top
            self.paddle_right = self.paddle_right_top

            # Create 2 AI instances for right team with 2D movement and zone-based strategy
            # Top AI defends upper zone
            top_zone_center = center_y - DOUBLES_PADDLE_SPACING_Y // 2
            self.ai = AIPlayer(
                self.paddle_right_top,
                difficulty="medium",
                doubles_mode=True,
                zone="top",
                zone_center_y=top_zone_center
            )
            # Bottom AI defends lower zone
            bottom_zone_center = center_y + DOUBLES_PADDLE_SPACING_Y // 2
            self.ai_bottom = AIPlayer(
                self.paddle_right_bottom,
                difficulty="medium",
                doubles_mode=True,
                zone="bottom",
                zone_center_y=bottom_zone_center
            )
        else:
            # Standard modes: 2 paddles
            paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2

            # Create paddles (full horizontal movement for singles/doubles is not needed)
            self.paddle_left = Paddle(PADDLE_OFFSET, paddle_y)
            self.paddle_right = Paddle(WINDOW_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH, paddle_y)

            # No doubles paddles in standard mode
            self.paddle_left_top = None
            self.paddle_left_bottom = None
            self.paddle_right_top = None
            self.paddle_right_bottom = None
            self.ai_bottom = None

            # Create AI
            self.ai = AIPlayer(self.paddle_right, difficulty="medium")

        # Create ball
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def set_mode(self, mode: GameMode) -> None:
        """Set the game mode.

        Args:
            mode: Game mode to set
        """
        self.mode = mode

    def start_game(self) -> None:
        """Start a new game."""
        self.state = GameState.PLAYING
        self.score_left = 0
        self.score_right = 0
        self._init_game_objects()
        self._reset_positions()

    def _reset_positions(self) -> None:
        """Reset all game objects to starting positions."""
        if self.mode == GameMode.DOUBLES:
            center_y = WINDOW_HEIGHT // 2
            self.paddle_left_top.reset(
                DOUBLES_PADDLE_OFFSET_X,
                center_y - DOUBLES_PADDLE_SPACING_Y
            )
            self.paddle_left_bottom.reset(
                DOUBLES_PADDLE_OFFSET_X,
                center_y + DOUBLES_PADDLE_SPACING_Y - DOUBLES_PADDLE_HEIGHT
            )
            self.paddle_right_top.reset(
                WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH,
                center_y - DOUBLES_PADDLE_SPACING_Y
            )
            self.paddle_right_bottom.reset(
                WINDOW_WIDTH - DOUBLES_PADDLE_OFFSET_X - PADDLE_WIDTH,
                center_y + DOUBLES_PADDLE_SPACING_Y - DOUBLES_PADDLE_HEIGHT
            )
        else:
            paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
            self.paddle_left.reset(PADDLE_OFFSET, paddle_y)
            self.paddle_right.reset(WINDOW_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH, paddle_y)

        self.ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle keyboard input.

        Args:
            keys: Pygame key state
        """
        if self.state != GameState.PLAYING:
            return

        if self.mode == GameMode.DOUBLES:
            # Player 1 (left top): WASD
            # Y-axis
            if keys[pygame.K_w]:
                self.paddle_left_top.move_up()
            elif keys[pygame.K_s]:
                self.paddle_left_top.move_down()
            else:
                self.paddle_left_top.stop_y()

            # X-axis
            if keys[pygame.K_a]:
                self.paddle_left_top.move_left()
            elif keys[pygame.K_d]:
                self.paddle_left_top.move_right()
            else:
                self.paddle_left_top.stop_x()

            # Player 2 (left bottom): IJKL
            # Y-axis
            if keys[pygame.K_UP]:
                self.paddle_left_bottom.move_up()
            elif keys[pygame.K_DOWN]:
                self.paddle_left_bottom.move_down()
            else:
                self.paddle_left_bottom.stop_y()

            # X-axis
            if keys[pygame.K_LEFT]:
                self.paddle_left_bottom.move_left()
            elif keys[pygame.K_RIGHT]:
                self.paddle_left_bottom.move_right()
            else:
                self.paddle_left_bottom.stop_x()
        else:
            # Standard 1P/2P controls
            # Player 1 controls (left paddle)
            if keys[pygame.K_w]:
                self.paddle_left.move_up()
            elif keys[pygame.K_s]:
                self.paddle_left.move_down()
            else:
                self.paddle_left.stop()

            # Player 2 controls (right paddle) - only in 2P mode
            if self.mode == GameMode.TWO_PLAYER:
                if keys[pygame.K_UP]:
                    self.paddle_right.move_up()
                elif keys[pygame.K_DOWN]:
                    self.paddle_right.move_down()
                else:
                    self.paddle_right.stop()

    def update(self) -> None:
        """Update game state."""
        if self.state != GameState.PLAYING:
            return

        if self.mode == GameMode.DOUBLES:
            # Update all 4 paddles
            self.paddle_left_top.update()
            self.paddle_left_bottom.update()
            self.paddle_right_top.update()
            self.paddle_right_bottom.update()

            # Update both AI players
            self.ai.update(self.ball)
            self.ai_bottom.update(self.ball)

            # Update ball
            self.ball.update()

            # Check paddle collisions with all 4 paddles
            self.ball.check_paddle_collision(self.paddle_left_top)
            self.ball.check_paddle_collision(self.paddle_left_bottom)
            self.ball.check_paddle_collision(self.paddle_right_top)
            self.ball.check_paddle_collision(self.paddle_right_bottom)
        else:
            # Standard 1P/2P mode
            # Update paddles
            self.paddle_left.update()
            self.paddle_right.update()

            # Update AI in 1P mode
            if self.mode == GameMode.ONE_PLAYER:
                self.ai.update(self.ball)

            # Update ball
            self.ball.update()

            # Check paddle collisions
            self.ball.check_paddle_collision(self.paddle_left)
            self.ball.check_paddle_collision(self.paddle_right)

        # Check scoring (same for all modes)
        if self.ball.is_out_left():
            self._score_right()
        elif self.ball.is_out_right():
            self._score_left()

    def _score_left(self) -> None:
        """Handle left player scoring."""
        self.score_left += 1
        if self.score_left >= WINNING_SCORE:
            self.state = GameState.GAME_OVER
        else:
            self._reset_positions()
            # Randomize AI strategies in doubles mode
            if self.mode == GameMode.DOUBLES:
                self.ai.randomize_strategy()
                self.ai_bottom.randomize_strategy()
            elif self.mode == GameMode.ONE_PLAYER:
                self.ai.randomize_strategy()

    def _score_right(self) -> None:
        """Handle right player scoring."""
        self.score_right += 1
        if self.score_right >= WINNING_SCORE:
            self.state = GameState.GAME_OVER
        else:
            self._reset_positions()
            # Randomize AI strategies in doubles mode
            if self.mode == GameMode.DOUBLES:
                self.ai.randomize_strategy()
                self.ai_bottom.randomize_strategy()
            elif self.mode == GameMode.ONE_PLAYER:
                self.ai.randomize_strategy()

    def draw(self) -> pygame.Surface:
        """Draw the game.

        Returns:
            The surface with the game drawn on it
        """
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()

        return self.screen

    def _draw_menu(self) -> None:
        """Draw the menu screen."""
        title = self.font_large.render("PONG", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        mode_text = self.font_medium.render(
            f"Mode: {self.mode.value}", True, WHITE
        )
        mode_rect = mode_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(mode_text, mode_rect)

        instructions = [
            "Press SPACE to change mode",
            "Press ENTER to start",
        ]
        y = 400
        for instruction in instructions:
            text = self.font_small.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50

    def _draw_game(self) -> None:
        """Draw the game screen."""
        # Draw center line
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(self.screen, GRAY, (WINDOW_WIDTH // 2 - 2, y, 4, 10))

        # Draw paddles and ball
        if self.mode == GameMode.DOUBLES:
            self.paddle_left_top.draw(self.screen)
            self.paddle_left_bottom.draw(self.screen)
            self.paddle_right_top.draw(self.screen)
            self.paddle_right_bottom.draw(self.screen)
        else:
            self.paddle_left.draw(self.screen)
            self.paddle_right.draw(self.screen)

        self.ball.draw(self.screen)

        # Draw scores
        score_left_text = self.font_large.render(str(self.score_left), True, WHITE)
        score_right_text = self.font_large.render(str(self.score_right), True, WHITE)

        self.screen.blit(score_left_text, (WINDOW_WIDTH // 4, 50))
        self.screen.blit(score_right_text, (3 * WINDOW_WIDTH // 4, 50))

    def _draw_game_over(self) -> None:
        """Draw the game over screen."""
        # Draw the final game state
        self._draw_game()

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Draw winner text
        winner = "Player 1" if self.score_left >= WINNING_SCORE else "Player 2"
        if self.mode == GameMode.ONE_PLAYER and winner == "Player 2":
            winner = "AI"

        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        winner_text = self.font_medium.render(f"{winner} Wins!", True, WHITE)

        game_over_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        winner_rect = winner_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        )

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(winner_text, winner_rect)

        # Instructions
        restart_text = self.font_small.render(
            "Press ENTER to return to menu", True, GRAY
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        )
        self.screen.blit(restart_text, restart_rect)

    def toggle_mode(self) -> None:
        """Toggle between 1P, 2P, and Doubles modes."""
        if self.mode == GameMode.ONE_PLAYER:
            self.mode = GameMode.TWO_PLAYER
        elif self.mode == GameMode.TWO_PLAYER:
            self.mode = GameMode.DOUBLES
        else:
            self.mode = GameMode.ONE_PLAYER

        # Reinitialize game objects for the new mode
        self._init_game_objects()

    def return_to_menu(self) -> None:
        """Return to the menu screen."""
        self.state = GameState.MENU
        self.score_left = 0
        self.score_right = 0

    def quit(self) -> None:
        """Quit the game."""
        self.running = False
        pygame.quit()

    def get_fps(self) -> int:
        """Get the target FPS.

        Returns:
            Target frames per second
        """
        return FPS

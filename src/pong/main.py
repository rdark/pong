"""Main entry point for Pong game."""

import pygame
from pong.game import Game, GameState
from pong.constants import WINDOW_WIDTH, WINDOW_HEIGHT


def main() -> None:
    """Run the main game loop."""
    # Initialize pygame
    pygame.init()

    # Create display window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")

    # Create game instance
    game = Game()

    # Main game loop
    while game.running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.quit()
                    return

                # Menu controls
                if game.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        game.start_game()
                    elif event.key == pygame.K_SPACE:
                        game.toggle_mode()

                # Game over controls
                elif game.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        game.return_to_menu()

        # Handle continuous input (for paddle movement)
        keys = pygame.key.get_pressed()
        game.handle_input(keys)

        # Update game state
        game.update()

        # Draw everything
        game_surface = game.draw()
        screen.blit(game_surface, (0, 0))
        pygame.display.flip()

        # Control frame rate
        game.clock.tick(game.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

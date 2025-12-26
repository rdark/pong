# Pong Game

A classic Pong game implementation in Python using pygame-ce (pygame Community Edition), supporting both 1-player (vs AI) and 2-player modes.

## Features

- **Two Game Modes**:
  - 1P: Play against an AI opponent with configurable difficulty
  - 2P: Local multiplayer for two players
- **AI Opponent**: Smart AI with three difficulty levels (easy, medium, hard)
- **Smooth Physics**: Ball speed increases with each paddle hit, with angle-based reflections
- **Score Tracking**: First to 10 points wins
- **Clean UI**: Minimalist design with clear score display and menus

## Installation

### Option 1: Using uv (Recommended)

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository (or navigate to the directory)
cd pong

# Install dependencies (uv will automatically create a virtual environment)
uv sync
```

### Option 2: Using pip with requirements.txt

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# For development (includes testing tools)
uv pip install -r requirements-dev.txt
```

## Running the Game

```bash
# Run with uv
uv run pong

# Or activate the virtual environment and run directly
source .venv/bin/activate
python -m pong.main
```

## Controls

### Menu
- **SPACE**: Toggle between 1P and 2P modes
- **ENTER**: Start the game
- **ESC**: Quit

### Gameplay
- **Player 1** (Left Paddle):
  - W: Move up
  - S: Move down

- **Player 2** (Right Paddle, 2P mode only):
  - UP ARROW: Move up
  - DOWN ARROW: Move down

### Game Over
- **ENTER**: Return to menu
- **ESC**: Quit

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src/pong --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_game.py -v

# Generate HTML coverage report
uv run pytest --cov=src/pong --cov-report=html
# Open htmlcov/index.html in your browser
```

### Game Configuration

You can modify game settings in `src/pong/constants.py`:

- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Display dimensions
- `FPS`: Frame rate (default: 60)
- `PADDLE_SPEED`: Paddle movement speed
- `BALL_INITIAL_SPEED`: Starting ball speed
- `BALL_MAX_SPEED`: Maximum ball speed
- `WINNING_SCORE`: Points needed to win (default: 10)
- `AI_SPEED`: AI paddle speed
- `AI_REACTION_ZONE`: AI dead zone (affects difficulty)

## Architecture

### Component Design

- **Paddle**: Handles paddle movement, boundary constraints, and rendering
- **Ball**: Manages ball physics, collision detection, and velocity
- **AIPlayer**: Controls AI paddle with configurable difficulty
- **Game**: Orchestrates game state, score tracking, and rendering
- **main**: Entry point with pygame event loop

### Game States

1. **MENU**: Initial screen with mode selection
2. **PLAYING**: Active gameplay
3. **PAUSED**: Game paused (not yet implemented)
4. **GAME_OVER**: End screen showing winner

### Physics

- Ball bounces off top/bottom walls with velocity reversal
- Paddle collisions reverse horizontal direction
- Hit position on paddle affects ball angle
- Ball speed increases after each paddle hit (up to max speed)

## License

MIT

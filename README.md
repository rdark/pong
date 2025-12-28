# Pong Game

A classic Pong game implementation in Python using pygame-ce (pygame Community Edition), supporting 1-player, 2-player, and doubles modes.

## Features

- **Three Game Modes**:
  - **1P**: Play against an AI opponent with configurable difficulty
  - **2P**: Local multiplayer for two players
  - **Doubles**: Tennis-style doubles - 2 human players vs 2 AI opponents with 2D paddle movement!
- **AI Opponent**: Smart AI with three difficulty levels (easy, medium, hard)
  - In doubles mode, AI uses 2D movement with dynamic positioning strategies
  - Four AI strategies that randomly change per point: Defensive (stay back), Balanced (middle court), Aggressive (at net), Ball-reactive (adaptive)
- **2D Movement in Doubles**: All paddles can move horizontally and vertically within their half of the court
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
- **SPACE**: Toggle between 1P, 2P, and Doubles modes
- **ENTER**: Start the game
- **ESC**: Quit

### Gameplay - 1P/2P Modes
- **Player 1** (Left Paddle):
  - W: Move up
  - S: Move down

- **Player 2** (Right Paddle, 2P mode only):
  - UP ARROW: Move up
  - DOWN ARROW: Move down

### Gameplay - Doubles Mode
- **Player 1** (Left Top Paddle):
  - W: Move up
  - S: Move down
  - A: Move left
  - D: Move right

- **Player 2** (Left Bottom Paddle):
  - I: Move up
  - K: Move down
  - J: Move left
  - L: Move right

- **AI Team** (Right side): 2 AI opponents control the right paddles

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

**Display & General:**
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Display dimensions
- `FPS`: Frame rate (default: 60)
- `WINNING_SCORE`: Points needed to win (default: 10)

**Standard Mode Settings:**
- `PADDLE_SPEED`: Paddle movement speed
- `PADDLE_WIDTH`, `PADDLE_HEIGHT`: Paddle dimensions
- `PADDLE_OFFSET`: Distance from edge of screen

**Ball Physics:**
- `BALL_INITIAL_SPEED`: Starting ball speed
- `BALL_MAX_SPEED`: Maximum ball speed
- `BALL_SPEED_INCREMENT`: Speed increase per hit
- `ANGLE_FACTOR`: How much paddle hit position affects ball angle

**AI Settings:**
- `AI_SPEED`: AI paddle speed
- `AI_REACTION_ZONE`: AI dead zone (affects difficulty)
- `AI_AGGRESSIVE_OFFSET`: Distance from net for aggressive positioning
- `AI_BALL_REACTIVE_FORWARD_OFFSET`: Forward position when ball approaches
- `AI_BALL_REACTIVE_BACK_OFFSET`: Back position when ball moves away

**Doubles Mode Settings:**
- `DOUBLES_PADDLE_HEIGHT`: Paddle height in doubles mode
- `DOUBLES_PADDLE_OFFSET_X`: Horizontal distance from edge
- `DOUBLES_PADDLE_SPACING_Y`: Vertical spacing between teammates

## Architecture

### Component Design

- **Paddle**: Handles 2D paddle movement (X and Y axes), boundary constraints, and rendering
  - Supports configurable X-axis boundaries for doubles mode (half-court restriction)
  - Independent X and Y velocity control
- **Ball**: Manages ball physics, collision detection with multiple paddles, and velocity
- **AIPlayer**: Controls AI paddle with configurable difficulty
  - Standard modes: Y-axis movement only
  - Doubles mode: Full 2D movement (X and Y axes) with dynamic positioning strategies
  - Four positioning strategies: Defensive (stay back), Balanced (middle), Aggressive (forward), Ball-reactive (adaptive)
  - Strategies randomly change after each point scored
  - In doubles mode, 2 AI instances coordinate using zone-based defense to prevent overlap
- **Game**: Orchestrates game state, score tracking, and rendering
  - Manages 2 or 4 paddles depending on mode
  - Handles mode switching (1P → 2P → Doubles)
- **main**: Entry point with pygame event loop

### Game Modes

1. **1P**: Single player vs AI
2. **2P**: Two players, local multiplayer
3. **Doubles**: 2 human players (left) vs 2 AI opponents (right)
   - Paddles can move in 2D within their half of the court
   - Tennis-style doubles gameplay

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

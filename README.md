# Food Tetris

A fun twist on the classic Tetris game, where instead of traditional Tetris blocks, you'll be playing with food-themed pieces! Stack burgers, pizzas, fries, and more to clear lines and score points.

## Features

- Food-themed Tetrominoes (Burger, Pizza, Fries, Sushi, Donut, Hotdog, Broccoli)
- Ghost piece preview showing where the current piece will land
- Score tracking and level progression
- Next piece preview
- Pause functionality
- Game over screen with restart option

## Controls

- Arrow Keys: Move pieces left/right/down
- Up Arrow: Rotate piece
- Space: Hard drop (instantly drops the piece)
- P: Pause/Resume game
- R: Restart game

## Installation

### Option 1: Using pip (Recommended)
```bash
pip install food-tetris
```

### Option 2: From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/food-tetris.git
   cd food-tetris
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the game:
   ```bash
   pip install -e .
   ```

## Running the Game

After installation, you can run the game in one of these ways:

1. Using the command-line:
   ```bash
   food-tetris
   ```

2. Or by running the Python script directly:
   ```bash
   python food_tetris.py
   ```

## Game Rules

- Stack the food pieces to create complete horizontal lines
- When a line is completed, it will be cleared and you'll earn points
- The game speeds up as you level up
- Game ends when pieces stack up to the top of the screen

## Scoring System

- 1 line cleared: 100 points × level
- 2 lines cleared: 300 points × level
- 3 lines cleared: 500 points × level
- 4 lines cleared: 800 points × level

Level up every 10 lines cleared!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
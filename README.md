# Food Tetris

A fun twist on the classic Tetris game, where instead of traditional Tetris blocks, you'll be playing with food-themed pieces! Stack burgers, pizzas, fries, and more to clear lines and score points.

## Quick Start Guide

### Step 1: Install the Game
Choose one of these methods:

**Method A - From GitHub (Recommended):**
```bash
pip install git+https://github.com/GabeisAgentic/Food-Tetris-.git
```

**Method B - From PyPI:**
```bash
pip install food-tetris
```

### Step 2: Run the Game
After installation, simply type:
```bash
food-tetris
```

That's it! The game should now start. If you encounter any issues, please check the Troubleshooting section below.

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

## Troubleshooting

If you encounter any issues:

1. Make sure you have Python 3.6 or higher installed
2. If you get a "command not found" error, try:
   ```bash
   python -m food_tetris
   ```
3. If you have any problems, please open an issue on GitHub

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
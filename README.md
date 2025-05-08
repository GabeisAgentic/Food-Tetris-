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

1. Make sure you have Python 3.x installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

Simply run the Python script:
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
import unittest
import pygame
import sys
import os
from food_tetris import (
    FOODS,
    new_piece,
    valid_move,
    GRID_WIDTH,
    GRID_HEIGHT
)

class TestFoodTetris(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_new_piece(self):
        """Test that new pieces are created correctly"""
        piece = new_piece()
        self.assertIn(piece['type'], FOODS)
        self.assertEqual(piece['y'], 0)
        self.assertEqual(piece['rotation'], 0)
        # Check that x position is within valid range
        self.assertGreaterEqual(piece['x'], 0)
        self.assertLess(piece['x'], GRID_WIDTH)

    def test_valid_move(self):
        """Test piece movement validation"""
        piece = new_piece()
        # Test valid moves
        self.assertTrue(valid_move(piece, piece['x'], piece['y'], piece['rotation'], self.grid))
        self.assertTrue(valid_move(piece, piece['x'] + 1, piece['y'], piece['rotation'], self.grid))
        self.assertTrue(valid_move(piece, piece['x'] - 1, piece['y'], piece['rotation'], self.grid))
        self.assertTrue(valid_move(piece, piece['x'], piece['y'] + 1, piece['rotation'], self.grid))

        # Test invalid moves
        # Move piece to bottom
        piece['y'] = GRID_HEIGHT - 1
        self.assertFalse(valid_move(piece, piece['x'], piece['y'] + 1, piece['rotation'], self.grid))
        # Move piece to left edge
        piece['x'] = 0
        self.assertFalse(valid_move(piece, piece['x'] - 1, piece['y'], piece['rotation'], self.grid))
        # Move piece to right edge
        piece['x'] = GRID_WIDTH - 1
        self.assertFalse(valid_move(piece, piece['x'] + 1, piece['y'], piece['rotation'], self.grid))

    def test_piece_types(self):
        """Test that all piece types have valid shapes"""
        for piece_type, piece_data in FOODS.items():
            shapes = piece_data['shape']
            # Check that there are 4 rotation states
            self.assertEqual(len(shapes), 4)
            # Check that each shape is valid
            for shape in shapes:
                # Check that shape is not empty
                self.assertTrue(len(shape) > 0)
                self.assertTrue(len(shape[0]) > 0)
                # Check that shape contains only dots and X's
                for row in shape:
                    for cell in row:
                        self.assertIn(cell, ['.', 'X'])

    def test_grid_bounds(self):
        """Test that pieces can't move outside grid bounds"""
        piece = new_piece()
        # Test left boundary
        piece['x'] = 0
        self.assertFalse(valid_move(piece, -1, piece['y'], piece['rotation'], self.grid))
        # Test right boundary
        piece['x'] = GRID_WIDTH - 1
        self.assertFalse(valid_move(piece, GRID_WIDTH, piece['y'], piece['rotation'], self.grid))
        # Test bottom boundary
        piece['y'] = GRID_HEIGHT - 1
        self.assertFalse(valid_move(piece, piece['x'], GRID_HEIGHT, piece['rotation'], self.grid))

    def test_piece_rotation(self):
        """Test that pieces rotate correctly"""
        for piece_type in FOODS:
            piece = {'type': piece_type, 'x': 5, 'y': 5, 'rotation': 0}  # Place piece in middle of grid
            # Test all rotation states
            for rotation in range(4):
                self.assertTrue(valid_move(piece, piece['x'], piece['y'], rotation, self.grid))

if __name__ == '__main__':
    unittest.main() 
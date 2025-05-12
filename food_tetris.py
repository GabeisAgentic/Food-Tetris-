import pygame
import random
import os
import sys
import traceback
import time
import math

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Food Tetris')

# Get the screen info for fullscreen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Create game window in fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Constants
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRID_COLOR = (200, 200, 200)  # Lighter gray for grid lines
GAME_BG = (255, 255, 255)  # White background for game area
RED = (255, 0, 0)

# Add these constants after the other color definitions
PAUSE_BUTTON_COLOR = (100, 100, 100)  # Gray
PAUSE_BUTTON_HOVER_COLOR = (150, 150, 150)  # Lighter gray
PAUSE_BUTTON_SIZE = 40
PAUSE_BUTTON_MARGIN = 20

# Food-themed Tetrominoes
FOODS = {
    'fries': {  # I shape - Classic long piece styled as french fries
        'shape': [
            ['.....',
             '.....',
             'XXXX.',
             '.....',
             '.....'],
            ['..X..',
             '..X..',
             '..X..',
             '..X..',
             '.....'],
            ['.....',
             '.....',
             'XXXX.',
             '.....',
             '.....'],
            ['..X..',
             '..X..',
             '..X..',
             '..X..',
             '.....']
        ],
        'color': (255, 215, 0)  # Golden yellow for fries
    },
    'cheeseburger': {  # O shape - Classic square piece styled as cheeseburger
        'shape': [
            ['.....',
             '.....',
             '.XX..',
             '.XX..',
             '.....'],
            ['.....',
             '.....',
             '.XX..',
             '.XX..',
             '.....'],
            ['.....',
             '.....',
             '.XX..',
             '.XX..',
             '.....'],
            ['.....',
             '.....',
             '.XX..',
             '.XX..',
             '.....']
        ],
        'color': (139, 69, 19)  # Brown for burger bun
    },
    'chicken': {  # T shape - Classic T piece styled as chicken nuggets
        'shape': [
            ['.....',
             '..X..',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '..X..',
             '.XX..',
             '..X..',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '..X..',
             '.....'],
            ['.....',
             '..X..',
             '..XX.',
             '..X..',
             '.....']
        ],
        'color': (210, 180, 140)  # Tan color for chicken
    },
    'banana': {  # L shape - Classic L piece styled as banana
        'shape': [
            ['.....',
             '...X.',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '.XX..',
             '..X..',
             '..X..',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '.X...',
             '.....'],
            ['.....',
             '..X..',
             '..X..',
             '..XX.',
             '.....']
        ],
        'color': (255, 223, 0)  # Yellow for banana
    },
    'carrot': {  # J shape - Classic J piece styled as carrot
        'shape': [
            ['.....',
             '.X...',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '..X..',
             '..X..',
             '.XX..',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '...X.',
             '.....'],
            ['.....',
             '.XX..',
             '.X...',
             '.X...',
             '.....']
        ],
        'color': (255, 140, 0)  # Orange for carrot
    },
    'pretzel': {  # S shape - Classic S piece styled as pretzel
        'shape': [
            ['.....',
             '.....',
             '..XX.',
             '.XX..',
             '.....'],
            ['.....',
             '.X...',
             '.XX..',
             '..X..',
             '.....'],
            ['.....',
             '.....',
             '..XX.',
             '.XX..',
             '.....'],
            ['.....',
             '.X...',
             '.XX..',
             '..X..',
             '.....']
        ],
        'color': (139, 69, 19)  # Brown for pretzel
    },
    'pasta': {  # Z shape - Classic Z piece styled as twisted pasta
        'shape': [
            ['.....',
             '.....',
             '.XX..',
             '..XX.',
             '.....'],
            ['.....',
             '..X..',
             '.XX..',
             '.X...',
             '.....'],
            ['.....',
             '.....',
             '.XX..',
             '..XX.',
             '.....'],
            ['.....',
             '..X..',
             '.XX..',
             '.X...',
             '.....']
        ],
        'color': (255, 248, 220)  # Cream color for pasta
    }
}

# Character fullness and explosion state
character_fullness = 0
character_max_fullness = 10 * 20  # 10 lines cleared (20 fullness per line)
character_exploded = False
character_last_eat_time = 0
character_eat_animation_time = 0.5  # seconds
character_eating = False
character_start_time = time.time()

# Hold piece state
held_piece = None
can_hold = True  # Flag to prevent holding multiple times in a row

# Game over messages
GAME_OVER_MESSAGES = [
    "Too much food, not enough space!",
    "Your character couldn't handle the feast!",
    "The food pile got too high!",
    "Time to start a new food adventure!",
    "Your character needs a break!",
    "The food avalanche was too much!",
    "Your character is taking a food coma!",
    "The food tower collapsed!",
    "Your character is full to the brim!",
    "The food mountain was too steep!"
]

# Victory messages
VICTORY_MESSAGES = [
    "You've mastered the food stacking!",
    "Perfect food balance achieved!",
    "Your character is a food stacking champion!",
    "Incredible food management!",
    "You've conquered the food challenge!",
    "Your character is a food stacking legend!",
    "Outstanding food organization!",
    "You've reached food stacking perfection!",
    "Your character is a food stacking master!",
    "Brilliant food strategy!"
]

def process_food_image(image, food_type=None):
    """Process a food image to match the game's style"""
    # Scale the image to match the grid size
    image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
    
    # Create a new surface with black background for chicken
    if food_type == 'chicken':
        # Create a new surface with black background
        new_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        new_surface.fill((0, 0, 0))  # Black background
        # Blit the scaled image on top of the black background
        new_surface.blit(image, (0, 0))
        # Add a border
        pygame.draw.rect(new_surface, (255, 255, 255), new_surface.get_rect(), 1)
        return new_surface
    else:
        # Add a semi-transparent overlay for other pieces
        overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 50))
        image.blit(overlay, (0, 0))
        # Add a border
        pygame.draw.rect(image, (255, 255, 255), image.get_rect(), 1)
        return image

def create_food_image(color, label):
    """Create a colored surface for a food piece with label"""
    # Create a surface for the food piece
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
    
    # Try to load the image first
    image_paths = [
        os.path.join('images', f'{label.lower()}.png .webp'),  # Try the exact file name we found
        os.path.join('images', f'{label.lower()}.png'),        # Try .png
        os.path.join('images', f'{label.lower()}.webp')        # Try .webp
    ]
    
    for image_path in image_paths:
        print(f"Trying to load image from: {image_path}")  # Debug print
        print(f"Does file exist? {os.path.exists(image_path)}")  # Debug print
        try:
            if os.path.exists(image_path):
                print(f"Loading image for {label} from {image_path}")  # Debug print
                # Load and scale the image
                food_image = pygame.image.load(image_path)
                # Process the image with the food type
                food_image = process_food_image(food_image, label.lower())
                return food_image
        except Exception as e:
            print(f"Error loading image {image_path}: {str(e)}")  # Debug print
            continue
    
    print(f"Falling back to colored block for {label}")  # Debug print
    
    # Fill with the base color
    pygame.draw.rect(surface, color, (0, 0, GRID_SIZE, GRID_SIZE))
    
    # Add a letter label as fallback
    font = pygame.font.Font(None, GRID_SIZE // 2)
    letter = label[0].upper()
    text = font.render(letter, True, (0, 0, 0))
    text_rect = text.get_rect(center=(GRID_SIZE // 2, GRID_SIZE // 2))
    surface.blit(text, text_rect)
    
    # Add a white border
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 1)
    
    return surface

def load_food_images():
    """Load food images or create emoji-based food pieces"""
    food_images = {}
    food_labels = {
        'fries': 'fries',
        'cheeseburger': 'burger',
        'chicken': 'chicken',
        'banana': 'banana',
        'carrot': 'carrot',
        'pretzel': 'pretzel',
        'pasta': 'pasta'
    }
    
    for food_name in FOODS.keys():
        food_images[food_name] = create_food_image(FOODS[food_name]['color'], food_labels[food_name])
    
    return food_images

def new_piece():
    """Create a new piece"""
    global current_piece, next_pieces
    if 'next_pieces' not in globals() or not next_pieces:
        # First piece of the game
        current_piece = {
            'type': random.choice(list(FOODS.keys())),
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        }
        next_pieces = [
            {
                'type': random.choice(list(FOODS.keys())),
                'x': GRID_WIDTH // 2 - 2,
                'y': 0,
                'rotation': 0
            } for _ in range(3)
        ]
    else:
        # Use the first next piece as current and generate a new next piece
        current_piece = next_pieces[0]
        next_pieces = next_pieces[1:] + [{
            'type': random.choice(list(FOODS.keys())),
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        }]
    return current_piece

def valid_move(piece, x, y, rotation, grid):
    """Check if a move is valid"""
    shape = FOODS[piece['type']]['shape'][rotation]
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 'X':
                new_x = x + j
                new_y = y + i
                if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                    return False
                if grid[new_y][new_x]:
                    return False
    return True

def merge_piece(piece):
    """Merge the current piece with the grid"""
    shape = FOODS[piece['type']]['shape'][piece['rotation']]
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 'X':
                grid[piece['y'] + i][piece['x'] + j] = piece['type']

def clear_lines():
    """Clear completed lines and update score"""
    global score, level, lines_cleared, character_fullness, character_eating, character_last_eat_time, character_exploded, game_over
    lines = 0
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [None for _ in range(GRID_WIDTH)])
            lines += 1
    
    if lines > 0:
        lines_cleared += lines
        score += [0, 100, 300, 500, 800][lines] * level
        level = lines_cleared // 10 + 1
        character_fullness += lines * 20  # Increased fullness per line
        character_eating = True
        character_last_eat_time = time.time()
        if character_fullness >= character_max_fullness:
            character_exploded = True
            game_over = True  # Ensure win screen appears immediately
            # Add bonus points for winning
            score += 1000 * level

def draw_grid():
    """Draw the game grid"""
    # Fill game area with white background
    pygame.draw.rect(screen, GAME_BG, (0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
    
    # Draw grid lines
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRID_COLOR,
                           (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            if grid[y][x]:
                # Draw individual food block
                food_type = grid[y][x]
                food_image = food_images[food_type]
                # Scale down the food image to fit a single block
                scaled_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))
                screen.blit(scaled_image, (x * GRID_SIZE, y * GRID_SIZE))

def draw_piece(piece, ghost=False):
    """Draw a piece on the screen"""
    shape = FOODS[piece['type']]['shape'][piece['rotation']]
    
    # Draw individual blocks for the piece
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 'X':
                # Draw individual food block
                food_image = food_images[piece['type']]
                # Scale down the food image to fit a single block
                scaled_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))
                
                if ghost:
                    # Create a darker ghost version of just this block
                    ghost_surface = scaled_image.copy()
                    ghost_surface.set_alpha(80)
                    dark_overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    dark_overlay.fill((0, 0, 0, 100))
                    ghost_surface.blit(dark_overlay, (0, 0))
                    screen.blit(ghost_surface, ((piece['x'] + j) * GRID_SIZE, (piece['y'] + i) * GRID_SIZE))
                else:
                    screen.blit(scaled_image, ((piece['x'] + j) * GRID_SIZE, (piece['y'] + i) * GRID_SIZE))

def draw_ghost_piece(piece):
    """Draw the ghost piece showing where the current piece will land"""
    ghost_piece = piece.copy()
    while valid_move(ghost_piece, ghost_piece['x'], ghost_piece['y'] + 1, ghost_piece['rotation'], grid):
        ghost_piece['y'] += 1
    draw_piece(ghost_piece, ghost=True)

def draw_sidebar():
    """Draw the sidebar with score, level, and next pieces"""
    # Draw sidebar background
    pygame.draw.rect(screen, BLACK, (GRID_WIDTH * GRID_SIZE, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (GRID_WIDTH * GRID_SIZE + 20, 20))
    
    # Draw level
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (GRID_WIDTH * GRID_SIZE + 20, 60))
    
    # Draw lines cleared
    lines_text = font.render(f'Lines: {lines_cleared}', True, WHITE)
    screen.blit(lines_text, (GRID_WIDTH * GRID_SIZE + 20, 100))
    
    # Draw hold piece section
    hold_text = font.render('Hold:', True, WHITE)
    screen.blit(hold_text, (GRID_WIDTH * GRID_SIZE + 20, 160))
    
    if held_piece:
        # Create a copy of the held piece for preview
        preview_piece = held_piece.copy()
        
        # Get the shape for the current rotation
        shape = FOODS[preview_piece['type']]['shape'][preview_piece['rotation']]
        
        # Calculate the dimensions of the shape
        shape_width = len(shape[0]) * GRID_SIZE
        shape_height = len(shape) * GRID_SIZE
        
        # Calculate piece position (centered in sidebar)
        start_x = GRID_WIDTH * GRID_SIZE + (SIDEBAR_WIDTH - shape_width) // 2
        start_y = 200
        
        # Draw individual blocks for the preview piece
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == 'X':
                    # Draw individual food block
                    food_image = food_images[preview_piece['type']]
                    # Scale down the food image to fit a single block
                    scaled_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))
                    screen.blit(scaled_image, (start_x + col_idx * GRID_SIZE, start_y + row_idx * GRID_SIZE))
    
    # Draw next pieces
    next_text = font.render('Next:', True, WHITE)
    screen.blit(next_text, (GRID_WIDTH * GRID_SIZE + 20, 300))
    
    if next_pieces:
        for i, next_piece in enumerate(next_pieces):
            # Create a copy of the piece for preview
            preview_piece = next_piece.copy()
            
            # Get the shape for the current rotation
            shape = FOODS[preview_piece['type']]['shape'][preview_piece['rotation']]
            
            # Calculate the dimensions of the shape
            shape_width = len(shape[0]) * GRID_SIZE
            shape_height = len(shape) * GRID_SIZE
            
            # Calculate piece position (centered in sidebar)
            start_x = GRID_WIDTH * GRID_SIZE + (SIDEBAR_WIDTH - shape_width) // 2
            start_y = 340 + (i * 140)
            
            # Draw individual blocks for the preview piece
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell == 'X':
                        # Draw individual food block
                        food_image = food_images[preview_piece['type']]
                        # Scale down the food image to fit a single block
                        scaled_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))
                        screen.blit(scaled_image, (start_x + col_idx * GRID_SIZE, start_y + row_idx * GRID_SIZE))

def draw_game_over(selected_message):
    """Draw game over screen"""
    global play_again_button_rect
    
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Draw game over text
    font = pygame.font.Font(None, 74)
    if character_exploded:
        text = font.render("You Won!", True, (255, 215, 0))  # Gold color for victory
    else:
        text = font.render("Game Over!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)
    
    # Draw score
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(score_text, score_rect)
    
    # Draw a single random message
    font = pygame.font.Font(None, 36)
    if character_exploded:
        # Select a random victory message
        message = selected_message
    else:
        # Select a random game over message
        message = selected_message
    message_text = font.render(message, True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(message_text, message_rect)
    
    # Draw play again button
    button_width = 200
    button_height = 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2 + 100
    
    # Draw button background
    pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, (100, 100, 100), (button_x, button_y, button_width, button_height), 2)
    
    # Draw button text
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, button_text_rect)
    
    # Store button rect for click detection
    play_again_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

def draw_pause():
    """Draw the pause menu with controls"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Draw pause menu box
    menu_width = 400
    menu_height = 500
    menu_x = (SCREEN_WIDTH - menu_width) // 2
    menu_y = (SCREEN_HEIGHT - menu_height) // 2
    
    pygame.draw.rect(screen, BLACK, (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(screen, WHITE, (menu_x, menu_y, menu_width, menu_height), 2)
    
    # Draw title
    font = pygame.font.Font(None, 48)
    title = font.render('PAUSED', True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 40))
    screen.blit(title, title_rect)
    
    # Draw menu options
    font = pygame.font.Font(None, 36)
    menu_items = [
        "Controls:",
        "← → ↓ : Move",
        "↑ : Rotate",
        "Space : Hard Drop",
        "P : Resume",
        "R : Restart"
    ]
    
    for i, text in enumerate(menu_items):
        item = font.render(text, True, WHITE)
        item_rect = item.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 100 + i * 40))
        screen.blit(item, item_rect)

def draw_controls():
    """Draw minimal controls at the bottom of the screen"""
    font = pygame.font.Font(None, 24)
    controls = [
        "P : Pause",
        "R : Restart"
    ]
    
    for i, text in enumerate(controls):
        control_text = font.render(text, True, BLACK)  # Changed to black text
        screen.blit(control_text, (20, SCREEN_HEIGHT - 50 + i * 25))

def try_wall_kick(piece, new_rotation, grid):
    """Try to move the piece left or right to make rotation possible"""
    # Store original position
    original_x = piece['x']
    original_y = piece['y']
    original_rotation = piece['rotation']
    
    # Try moving left
    if valid_move(piece, piece['x'] - 1, piece['y'], new_rotation, grid):
        piece['x'] -= 1
        piece['rotation'] = new_rotation
        return True
    
    # Try moving right
    if valid_move(piece, piece['x'] + 1, piece['y'], new_rotation, grid):
        piece['x'] += 1
        piece['rotation'] = new_rotation
        return True
    
    # Try moving up (for pieces near the bottom)
    if valid_move(piece, piece['x'], piece['y'] - 1, new_rotation, grid):
        piece['y'] -= 1
        piece['rotation'] = new_rotation
        return True
    
    # If no valid wall kick found, restore original position
    piece['x'] = original_x
    piece['y'] = original_y
    piece['rotation'] = original_rotation
    return False

def draw_character():
    """Draw the character with dynamic belly size and eating animation"""
    global character_eating, character_last_eat_time
    
    # Calculate character position (in the right sidebar)
    char_x = GRID_WIDTH * GRID_SIZE + SIDEBAR_WIDTH + (SCREEN_WIDTH - (GRID_WIDTH * GRID_SIZE + SIDEBAR_WIDTH)) // 2  # Center in the right sidebar
    char_y = SCREEN_HEIGHT - 200  # Position from bottom of screen
    
    # Calculate belly size based on fullness
    belly_radius = 30 + int(60 * (character_fullness / character_max_fullness))
    
    # Calculate body proportions based on fullness
    body_height = 120 + int(40 * (character_fullness / character_max_fullness))
    body_width = 60 + int(40 * (character_fullness / character_max_fullness))
    
    # Draw character body
    if not character_exploded:
        # Draw legs
        leg_width = 20
        leg_height = 60
        leg_spacing = 30
        pygame.draw.rect(screen, (139, 69, 19), (char_x - leg_spacing - leg_width//2, char_y + body_height//2, leg_width, leg_height))  # Left leg
        pygame.draw.rect(screen, (139, 69, 19), (char_x + leg_spacing - leg_width//2, char_y + body_height//2, leg_width, leg_height))  # Right leg
        
        # Draw feet
        foot_width = 30
        foot_height = 15
        pygame.draw.rect(screen, (0, 0, 0), (char_x - leg_spacing - foot_width//2, char_y + body_height//2 + leg_height, foot_width, foot_height))  # Left foot
        pygame.draw.rect(screen, (0, 0, 0), (char_x + leg_spacing - foot_width//2, char_y + body_height//2 + leg_height, foot_width, foot_height))  # Right foot
        
        # Draw body (shirt)
        shirt_color = (0, 0, 255)  # Blue shirt
        if character_fullness > character_max_fullness * 0.7:  # Shirt starts ripping at 70% fullness
            shirt_color = (100, 100, 255)  # Lighter blue for stretched shirt
        pygame.draw.rect(screen, shirt_color, (char_x - body_width//2, char_y - body_height//2, body_width, body_height))
        
        # Draw belly (showing through shirt)
        pygame.draw.circle(screen, (255, 200, 150), (char_x, char_y), belly_radius)
        
        # Draw arms
        arm_width = 15
        arm_height = 40
        arm_y = char_y - body_height//4
        pygame.draw.rect(screen, (255, 200, 150), (char_x - body_width//2 - arm_width, arm_y, arm_width, arm_height))  # Left arm
        pygame.draw.rect(screen, (255, 200, 150), (char_x + body_width//2, arm_y, arm_width, arm_height))  # Right arm
        
        # Draw head
        head_radius = 25
        pygame.draw.circle(screen, (255, 200, 150), (char_x, char_y - body_height//2 - head_radius), head_radius)
        
        # Draw face
        eye_radius = 4
        pygame.draw.circle(screen, (0, 0, 0), (char_x - 8, char_y - body_height//2 - head_radius), eye_radius)  # Left eye
        pygame.draw.circle(screen, (0, 0, 0), (char_x + 8, char_y - body_height//2 - head_radius), eye_radius)  # Right eye
        
        # Draw mouth (changes based on eating state)
        if character_eating:
            # Open mouth for eating
            pygame.draw.arc(screen, (0, 0, 0), 
                          (char_x - 15, char_y - body_height//2 - head_radius - 5, 30, 20),
                          0, 3.14, 2)
        else:
            # Normal smile
            pygame.draw.arc(screen, (0, 0, 0), 
                          (char_x - 15, char_y - body_height//2 - head_radius - 5, 30, 20),
                          0, 3.14, 2)
        
        # Draw pants
        pants_color = (50, 50, 50)  # Dark gray pants
        if character_fullness > character_max_fullness * 0.8:  # Pants start ripping at 80% fullness
            pants_color = (100, 100, 100)  # Lighter gray for stretched pants
        pygame.draw.rect(screen, pants_color, (char_x - body_width//2, char_y + body_height//4, body_width, body_height//2))
        
        # Draw ripping effects when very full
        if character_fullness > character_max_fullness * 0.9:  # Show ripping at 90% fullness
            # Draw ripping lines on shirt
            rip_color = (200, 200, 200)
            for i in range(3):
                start_x = char_x - body_width//2 + random.randint(0, body_width)
                start_y = char_y - body_height//2 + random.randint(0, body_height)
                end_x = start_x + random.randint(-20, 20)
                end_y = start_y + random.randint(-20, 20)
                pygame.draw.line(screen, rip_color, (start_x, start_y), (end_x, end_y), 2)
    else:
        # Single explosion animation
        explosion_radius = 100
        explosion_color = (255, 100, 0)  # Orange explosion
        
        # Draw explosion circle
        pygame.draw.circle(screen, explosion_color, (char_x, char_y), explosion_radius)
        
        # Draw explosion lines
        for i in range(16):
            angle = i * (360 / 16)
            rad_angle = math.radians(angle)
            end_x = char_x + explosion_radius * 1.5 * math.cos(rad_angle)
            end_y = char_y + explosion_radius * 1.5 * math.sin(rad_angle)
            pygame.draw.line(screen, explosion_color, (char_x, char_y), (end_x, end_y), 8)
        
        # Draw inner explosion
        pygame.draw.circle(screen, (255, 255, 0), (char_x, char_y), explosion_radius * 0.7)  # Yellow inner circle
        
        # Draw small debris
        for _ in range(20):
            debris_x = char_x + random.randint(-explosion_radius, explosion_radius)
            debris_y = char_y + random.randint(-explosion_radius, explosion_radius)
            debris_size = random.randint(5, 15)
            pygame.draw.circle(screen, (255, 100, 0), (debris_x, debris_y), debris_size)

def reset_game():
    """Reset the game state"""
    global grid, next_pieces, current_piece, score, level, lines_cleared, game_over, held_piece, can_hold, character_fullness, character_exploded, character_eating, character_start_time, paused
    
    # Reset game state
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    next_pieces = [
        {
            'type': random.choice(list(FOODS.keys())),
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        } for _ in range(3)
    ]
    current_piece = new_piece()
    score = 0
    level = 1
    lines_cleared = 0
    game_over = False
    paused = False
    held_piece = None
    can_hold = True
    
    # Reset character state
    character_fullness = 0
    character_exploded = False
    character_eating = False
    character_start_time = time.time()

def draw_pause_button():
    """Draw the pause button in the top-right corner of the game area"""
    # Calculate button position
    button_x = GRID_WIDTH * GRID_SIZE - PAUSE_BUTTON_SIZE - PAUSE_BUTTON_MARGIN
    button_y = PAUSE_BUTTON_MARGIN
    
    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Check if mouse is hovering over button
    is_hovering = (button_x <= mouse_x <= button_x + PAUSE_BUTTON_SIZE and 
                  button_y <= mouse_y <= button_y + PAUSE_BUTTON_SIZE)
    
    # Draw button background
    button_color = PAUSE_BUTTON_HOVER_COLOR if is_hovering else PAUSE_BUTTON_COLOR
    pygame.draw.rect(screen, button_color, 
                    (button_x, button_y, PAUSE_BUTTON_SIZE, PAUSE_BUTTON_SIZE))
    
    # Draw pause icon (two vertical bars)
    bar_width = 8
    bar_height = 20
    bar_spacing = 4
    bar_x = button_x + (PAUSE_BUTTON_SIZE - (bar_width * 2 + bar_spacing)) // 2
    bar_y = button_y + (PAUSE_BUTTON_SIZE - bar_height) // 2
    
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, WHITE, (bar_x + bar_width + bar_spacing, bar_y, bar_width, bar_height))
    
    return (button_x, button_y, PAUSE_BUTTON_SIZE, PAUSE_BUTTON_SIZE)

def main():
    """Main game loop"""
    global current_piece, next_pieces, score, level, lines_cleared, game_over, paused, grid, screen, food_images, character_exploded, character_eating, held_piece, can_hold, play_again_button_rect
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption('Food Tetris')
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load food images
    food_images = load_food_images()
    
    # Initialize game state
    reset_game()
    
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Initialize last move time for continuous movement
    last_move_time = 0
    last_horizontal_move_time = 0
    move_delay = 16  # milliseconds between moves when holding down (about 60 moves per second)
    horizontal_move_delay = 100
    
    # Variables for piece locking
    piece_lock_delay = 500  # milliseconds before piece locks in place
    piece_lock_timer = 0
    piece_has_landed = False
    
    # Variables for explosion animation
    explosion_start_time = 0
    explosion_duration = 2.0  # 2 seconds for explosion animation
    showing_explosion = False
    selected_message = None  # Store the selected message
    
    # Main game loop
    while True:
        current_time = pygame.time.get_ticks()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if play again button was clicked
                if game_over and play_again_button_rect and play_again_button_rect.collidepoint(event.pos):
                    reset_game()
                    showing_explosion = False
                    selected_message = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    reset_game()
                    showing_explosion = False
                    selected_message = None
                
                if not paused and not game_over and not showing_explosion:
                    if event.key == pygame.K_c and can_hold:
                        # Hold piece functionality
                        if held_piece is None:
                            # If no piece is held, store current piece and get new piece
                            held_piece = current_piece.copy()
                            current_piece = new_piece()
                        else:
                            # Swap current piece with held piece
                            temp_piece = current_piece.copy()
                            current_piece = held_piece.copy()
                            held_piece = temp_piece.copy()
                            # Reset position and rotation for the swapped piece
                            current_piece['x'] = GRID_WIDTH // 2 - 2
                            current_piece['y'] = 0
                            current_piece['rotation'] = 0
                        can_hold = False  # Prevent holding again until piece is placed
                        piece_has_landed = False
                        piece_lock_timer = 0
                    elif event.key == pygame.K_UP:
                        # Store original state
                        original_rotation = current_piece['rotation']
                        original_x = current_piece['x']
                        original_y = current_piece['y']
                        
                        # Try rotation
                        new_rotation = (current_piece['rotation'] + 1) % 4
                        if valid_move(current_piece, current_piece['x'], current_piece['y'], new_rotation, grid):
                            current_piece['rotation'] = new_rotation
                            # Reset lock timer on successful rotation
                            piece_has_landed = False
                            piece_lock_timer = 0
                        else:
                            # Try wall kicks if direct rotation isn't possible
                            if try_wall_kick(current_piece, new_rotation, grid):
                                # Reset lock timer on successful wall kick
                                piece_has_landed = False
                                piece_lock_timer = 0
                            else:
                                # If no valid rotation found, restore original state
                                current_piece['rotation'] = original_rotation
                                current_piece['x'] = original_x
                                current_piece['y'] = original_y
                    elif event.key == pygame.K_SPACE:
                        while valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                            current_piece['y'] += 1
                        merge_piece(current_piece)
                        clear_lines()
                        current_piece = new_piece()
                        can_hold = True  # Allow holding again after piece is placed
                        piece_has_landed = False
                        piece_lock_timer = 0
                        if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation'], grid):
                            game_over = True
        
        if not paused and not game_over and not showing_explosion:
            # Handle continuous movement
            keys = pygame.key.get_pressed()
            
            # Check if piece has landed
            if not piece_has_landed and not valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                piece_has_landed = True
                piece_lock_timer = current_time
            
            # Handle left movement
            if keys[pygame.K_LEFT] and current_time - last_horizontal_move_time > horizontal_move_delay:
                if valid_move(current_piece, current_piece['x'] - 1, current_piece['y'], current_piece['rotation'], grid):
                    current_piece['x'] -= 1
                    last_horizontal_move_time = current_time
                    # Reset lock timer on successful move
                    piece_has_landed = False
                    piece_lock_timer = 0
            
            # Handle right movement
            if keys[pygame.K_RIGHT] and current_time - last_horizontal_move_time > horizontal_move_delay:
                if valid_move(current_piece, current_piece['x'] + 1, current_piece['y'], current_piece['rotation'], grid):
                    current_piece['x'] += 1
                    last_horizontal_move_time = current_time
                    # Reset lock timer on successful move
                    piece_has_landed = False
                    piece_lock_timer = 0
            
            # Handle down movement
            if keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
                if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                    current_piece['y'] += 1
                    last_move_time = current_time
                    # Reset lock timer on successful move
                    piece_has_landed = False
                    piece_lock_timer = 0
            elif not keys[pygame.K_DOWN]:
                # Move piece down automatically
                if current_time - last_move_time > 1000:  # 1 second between automatic falls
                    if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                        current_piece['y'] += 1
                        last_move_time = current_time
                        # Reset lock timer on successful move
                        piece_has_landed = False
                        piece_lock_timer = 0
                    else:
                        # Check if piece should lock
                        if piece_has_landed and current_time - piece_lock_timer > piece_lock_delay:
                            merge_piece(current_piece)
                            clear_lines()
                            current_piece = new_piece()
                            can_hold = True  # Allow holding again after piece is placed
                            piece_has_landed = False
                            piece_lock_timer = 0
                            if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation'], grid):
                                game_over = True
                        last_move_time = current_time
        
        # Draw everything
        screen.fill(GAME_BG)  # Changed to white background
        
        # Draw character first (so it appears behind the grid)
        draw_character()
        
        # Draw game elements
        draw_grid()
        if not game_over and not paused and not showing_explosion:
            draw_ghost_piece(current_piece)
            draw_piece(current_piece)
        draw_sidebar()
        
        # Draw pause button and get its rect
        pause_button_rect = draw_pause_button()
        
        if paused:
            draw_pause()
        elif game_over:
            draw_game_over(selected_message)
        
        pygame.display.flip()
        clock.tick(60)

        # Update character eating state
        if character_eating and time.time() - character_last_eat_time > character_eat_animation_time:
            character_eating = False
            
        # Handle explosion and win screen sequence
        if character_exploded and not showing_explosion:
            showing_explosion = True
            explosion_start_time = time.time()
            # Select a random message when explosion starts
            selected_message = random.choice(VICTORY_MESSAGES)
        elif showing_explosion:
            if time.time() - explosion_start_time > explosion_duration:
                showing_explosion = False
                game_over = True
        elif not character_exploded and time.time() - character_start_time > character_max_fullness:
            character_exploded = True
            showing_explosion = True
            explosion_start_time = time.time()
            # Select a random message when explosion starts
            selected_message = random.choice(VICTORY_MESSAGES)

if __name__ == "__main__":
    try:
        # Set up display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Print debugging information
        print("Python version:", sys.version)
        print("Pygame version:", pygame.version.ver)
        print("Display driver:", pygame.display.get_driver())
        print("Available display modes:", pygame.display.list_modes())
        
        print("Starting game...")
        main()
        print("Game ended successfully")
        
    except Exception as e:
        print("Error during game execution:", str(e))
        traceback.print_exc()
        sys.exit(1) 
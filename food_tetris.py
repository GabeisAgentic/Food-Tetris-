import pygame
import random
import os
import sys
import traceback

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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

def create_food_image(color, label):
    """Create a colored surface for a food piece with label"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
    surface.fill(color)
    # Add a semi-transparent overlay to make it look more like food
    overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 50))
    surface.blit(overlay, (0, 0))
    # Add a border
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 1)
    
    # Add text label
    font = pygame.font.Font(None, 20)
    text = font.render(label, True, (0, 0, 0))
    text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE//2))
    surface.blit(text, text_rect)
    
    return surface

def process_food_image(image):
    """Process a food image to match the game's style"""
    # Scale the image to match the grid size
    image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
    # Add a semi-transparent overlay
    overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 50))
    image.blit(overlay, (0, 0))
    # Add a border
    pygame.draw.rect(image, (255, 255, 255), image.get_rect(), 1)
    return image

def load_food_images():
    """Load food images or create placeholders if images are not found"""
    food_images = {}
    food_labels = {
        'fries': 'Fries',
        'cheeseburger': 'Burger',
        'chicken': 'Chicken',
        'banana': 'Banana',
        'carrot': 'Carrot',
        'pretzel': 'Pretzel',
        'pasta': 'Pasta'
    }
    
    for food_name in FOODS.keys():
        try:
            # Try to load the actual food image
            image_path = os.path.join('images', f'{food_name}.png')
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                food_images[food_name] = process_food_image(image)
            else:
                # Create a placeholder with label if image is not found
                food_images[food_name] = create_food_image(FOODS[food_name]['color'], food_labels[food_name])
        except:
            # Fallback to placeholder if loading fails
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
                if (new_x < 0 or new_x >= GRID_WIDTH or 
                    new_y >= GRID_HEIGHT or 
                    (new_y >= 0 and grid[new_y][new_x])):
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
    global score, level, lines_cleared
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
                screen.blit(food_images[grid[y][x]],
                          (x * GRID_SIZE, y * GRID_SIZE))

def draw_piece(piece, ghost=False):
    """Draw a piece on the screen"""
    shape = FOODS[piece['type']]['shape'][piece['rotation']]
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 'X':
                x = (piece['x'] + j) * GRID_SIZE
                y = (piece['y'] + i) * GRID_SIZE
                if ghost:
                    # Create a darker ghost version of the food image
                    ghost_surface = food_images[piece['type']].copy()
                    # Make the ghost piece darker by using a lower alpha value
                    ghost_surface.set_alpha(80)  # Changed from 128 to 80 for darker shadow
                    # Add a dark overlay to make it even more visible
                    dark_overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    dark_overlay.fill((0, 0, 0, 100))  # Semi-transparent black overlay
                    ghost_surface.blit(dark_overlay, (0, 0))
                    screen.blit(ghost_surface, (x, y))
                else:
                    screen.blit(food_images[piece['type']], (x, y))

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
    
    # Draw pause button
    button_width = 160
    button_height = 40
    button_x = GRID_WIDTH * GRID_SIZE + (SIDEBAR_WIDTH - button_width) // 2
    button_y = 140
    
    # Draw button background
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)
    
    # Draw button text
    button_text = "PAUSE" if not paused else "RESUME"
    button_font = pygame.font.Font(None, 32)
    text_surface = button_font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    screen.blit(text_surface, text_rect)
    
    # Store button rect for click detection
    global pause_button_rect
    pause_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Draw next pieces
    next_text = font.render('Next:', True, WHITE)
    screen.blit(next_text, (GRID_WIDTH * GRID_SIZE + 20, 200))
    
    if next_pieces:
        for i, next_piece in enumerate(next_pieces):
            # Create a copy of the piece for preview
            preview_piece = next_piece.copy()
            
            # Get the shape for the current rotation
            shape = FOODS[preview_piece['type']]['shape'][preview_piece['rotation']]
            
            # Calculate the dimensions of the shape
            shape_width = len(shape[0]) * GRID_SIZE
            shape_height = len(shape) * GRID_SIZE
            
            # Calculate preview box dimensions with padding
            box_padding = 10
            box_width = max(shape_width, GRID_SIZE * 4) + (box_padding * 2)  # Ensure minimum width
            box_height = max(shape_height, GRID_SIZE * 4) + (box_padding * 2)  # Ensure minimum height
            
            # Calculate box position
            box_x = GRID_WIDTH * GRID_SIZE + (SIDEBAR_WIDTH - box_width) // 2
            box_y = 240 + (i * 140)  # Increased spacing between pieces
            
            # Draw preview box background
            pygame.draw.rect(screen, (40, 40, 40), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 1)
            
            # Calculate piece position within the box (centered)
            start_x = box_x + (box_width - shape_width) // 2
            start_y = box_y + (box_height - shape_height) // 2
            
            # Draw the piece
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell == 'X':
                        x = start_x + col_idx * GRID_SIZE
                        y = start_y + row_idx * GRID_SIZE
                        screen.blit(food_images[preview_piece['type']], (x, y))

def draw_game_over():
    """Draw the game over screen"""
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('GAME OVER', True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    
    font = pygame.font.Font(None, 36)
    restart_text = font.render('Press R to Restart', True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

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

def main():
    """Main game loop"""
    global current_piece, next_pieces, score, level, lines_cleared, game_over, paused, grid, screen, food_images, pause_button_rect
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption('Food Tetris')
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load food images
    food_images = load_food_images()
    
    # Initialize game state
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    level = 1
    lines_cleared = 0
    game_over = False
    paused = False
    pause_button_rect = None
    
    # Initialize first pieces
    next_pieces = [
        {
            'type': random.choice(list(FOODS.keys())),
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        } for _ in range(3)
    ]
    current_piece = new_piece()
    
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Initialize last move time for continuous movement
    last_move_time = 0
    last_horizontal_move_time = 0
    move_delay = 16  # milliseconds between moves when holding down (about 60 moves per second)
    horizontal_move_delay = 100  # milliseconds between horizontal moves (about 10 moves per second)
    
    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if pause button was clicked
                if pause_button_rect and pause_button_rect.collidepoint(event.pos):
                    paused = not paused
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    # Reset game
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
                
                if not paused and not game_over:
                    if event.key == pygame.K_UP:
                        # Store original state
                        original_rotation = current_piece['rotation']
                        original_x = current_piece['x']
                        original_y = current_piece['y']
                        
                        # Try rotation
                        new_rotation = (current_piece['rotation'] + 1) % 4
                        if valid_move(current_piece, current_piece['x'], current_piece['y'], new_rotation, grid):
                            current_piece['rotation'] = new_rotation
                        else:
                            # Try wall kicks if direct rotation isn't possible
                            if try_wall_kick(current_piece, new_rotation, grid):
                                pass
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
                        if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation'], grid):
                            game_over = True
        
        if not paused and not game_over:
            # Handle continuous movement
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            
            # Handle left movement
            if keys[pygame.K_LEFT] and current_time - last_horizontal_move_time > horizontal_move_delay:
                if valid_move(current_piece, current_piece['x'] - 1, current_piece['y'], current_piece['rotation'], grid):
                    current_piece['x'] -= 1
                    last_horizontal_move_time = current_time
            
            # Handle right movement
            if keys[pygame.K_RIGHT] and current_time - last_horizontal_move_time > horizontal_move_delay:
                if valid_move(current_piece, current_piece['x'] + 1, current_piece['y'], current_piece['rotation'], grid):
                    current_piece['x'] += 1
                    last_horizontal_move_time = current_time
            
            # Handle down movement
            if keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
                if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                    current_piece['y'] += 1
                    last_move_time = current_time
            elif not keys[pygame.K_DOWN]:
                # Move piece down automatically
                if current_time - last_move_time > 1000:  # 1 second between automatic falls
                    if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation'], grid):
                        current_piece['y'] += 1
                    else:
                        merge_piece(current_piece)
                        clear_lines()
                        current_piece = new_piece()
                        if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation'], grid):
                            game_over = True
                    last_move_time = current_time
        
        # Draw everything
        screen.fill(GAME_BG)  # Changed to white background
        draw_grid()
        if not game_over and not paused:
            draw_ghost_piece(current_piece)
            draw_piece(current_piece)
        draw_sidebar()
        
        if paused:
            draw_pause()
        elif game_over:
            draw_game_over()
        
        pygame.display.flip()
        clock.tick(60)

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
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
GRID_COLOR = (40, 40, 40)

# Food-themed Tetrominoes
FOODS = {
    'burger': {  # I shape
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
        'color': (255, 165, 0)  # Orange
    },
    'pizza': {  # O shape
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
        'color': (255, 0, 0)  # Red
    },
    'fries': {  # T shape
        'shape': [
            ['.....',
             '..X..',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '..X..',
             '..XX.',
             '..X..',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '..X..',
             '.....'],
            ['.....',
             '..X..',
             '.XX..',
             '..X..',
             '.....']
        ],
        'color': (255, 255, 0)  # Yellow
    },
    'sushi': {  # L shape
        'shape': [
            ['.....',
             '...X.',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '..X..',
             '..X..',
             '..XX.',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '.X...',
             '.....'],
            ['.....',
             '.XX..',
             '..X..',
             '..X..',
             '.....']
        ],
        'color': (0, 255, 0)  # Green
    },
    'donut': {  # J shape
        'shape': [
            ['.....',
             '.X...',
             '.XXX.',
             '.....',
             '.....'],
            ['.....',
             '.XX..',
             '.X...',
             '.X...',
             '.....'],
            ['.....',
             '.....',
             '.XXX.',
             '...X.',
             '.....'],
            ['.....',
             '..X..',
             '..X..',
             '.XX..',
             '.....']
        ],
        'color': (255, 192, 203)  # Pink
    },
    'hotdog': {  # S shape
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
        'color': (139, 69, 19)  # Brown
    },
    'broccoli': {  # Z shape
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
        'color': (34, 139, 34)  # Forest Green
    }
}

def create_food_image(color):
    """Create a colored surface for a food piece"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
    surface.fill(color)
    # Add a semi-transparent overlay to make it look more like food
    overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 50))
    surface.blit(overlay, (0, 0))
    # Add a border
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 1)
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
    for food_name in FOODS.keys():
        try:
            # Try to load the actual food image
            image_path = os.path.join('images', f'{food_name}.png')
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                food_images[food_name] = process_food_image(image)
            else:
                # Create a placeholder if image is not found
                food_images[food_name] = create_food_image(FOODS[food_name]['color'])
        except:
            # Fallback to placeholder if loading fails
            food_images[food_name] = create_food_image(FOODS[food_name]['color'])
    return food_images

def new_piece():
    """Create a new piece"""
    global current_piece, next_piece
    if 'next_piece' not in globals() or next_piece is None:
        next_piece = {
            'type': random.choice(list(FOODS.keys())),
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        }
    current_piece = {
        'type': next_piece['type'],
        'x': GRID_WIDTH // 2 - 2,
        'y': 0,
        'rotation': 0
    }
    next_piece = {
        'type': random.choice(list(FOODS.keys())),
        'x': GRID_WIDTH // 2 - 2,
        'y': 0,
        'rotation': 0
    }
    return current_piece

def valid_move(piece, x, y, rotation):
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
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines += 1
    
    if lines > 0:
        lines_cleared += lines
        score += [0, 100, 300, 500, 800][lines] * level
        level = lines_cleared // 10 + 1

def draw_grid():
    """Draw the game grid"""
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
                    # Create a ghost version of the food image
                    ghost_surface = food_images[piece['type']].copy()
                    ghost_surface.set_alpha(128)
                    screen.blit(ghost_surface, (x, y))
                else:
                    screen.blit(food_images[piece['type']], (x, y))

def draw_ghost_piece(piece):
    """Draw the ghost piece showing where the current piece will land"""
    ghost_piece = piece.copy()
    while valid_move(ghost_piece, ghost_piece['x'], ghost_piece['y'] + 1, ghost_piece['rotation']):
        ghost_piece['y'] += 1
    draw_piece(ghost_piece, ghost=True)

def draw_sidebar():
    """Draw the sidebar with score, level, and next piece"""
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
    
    # Draw next piece
    next_text = font.render('Next:', True, WHITE)
    screen.blit(next_text, (GRID_WIDTH * GRID_SIZE + 20, 160))
    
    if next_piece:
        next_shape = FOODS[next_piece['type']]['shape'][0]
        for i, row in enumerate(next_shape):
            for j, cell in enumerate(row):
                if cell == 'X':
                    x = GRID_WIDTH * GRID_SIZE + 60 + j * GRID_SIZE
                    y = 200 + i * GRID_SIZE
                    screen.blit(food_images[next_piece['type']], (x, y))

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
    """Draw the pause menu with controls and future sound options"""
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
        "R : Restart",
        "",
        "Sound Options:",
        "Coming Soon!"
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
        control_text = font.render(text, True, WHITE)
        screen.blit(control_text, (20, SCREEN_HEIGHT - 50 + i * 25))

def main():
    """Main game loop"""
    global current_piece, next_piece, score, level, lines_cleared, game_over, paused, grid
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption('Food Tetris')
    
    # Create game window
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load food images
    global food_images
    food_images = load_food_images()
    
    # Initialize game state
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = new_piece()
    next_piece = new_piece()
    score = 0
    level = 1
    lines_cleared = 0
    game_over = False
    paused = False
    
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Initialize last move time for continuous movement
    last_move_time = 0
    move_delay = 16  # milliseconds between moves when holding down (about 60 moves per second)
    
    # Main game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    # Reset game
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    current_piece = new_piece()
                    next_piece = new_piece()
                    score = 0
                    level = 1
                    lines_cleared = 0
                    game_over = False
                    paused = False
                elif not paused and not game_over:
                    if event.key == pygame.K_LEFT:
                        if valid_move(current_piece, current_piece['x'] - 1, current_piece['y'], current_piece['rotation']):
                            current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if valid_move(current_piece, current_piece['x'] + 1, current_piece['y'], current_piece['rotation']):
                            current_piece['x'] += 1
                    elif event.key == pygame.K_UP:
                        new_rotation = (current_piece['rotation'] + 1) % 4
                        if valid_move(current_piece, current_piece['x'], current_piece['y'], new_rotation):
                            current_piece['rotation'] = new_rotation
                    elif event.key == pygame.K_SPACE:
                        while valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation']):
                            current_piece['y'] += 1
                        merge_piece(current_piece)
                        clear_lines()
                        current_piece = new_piece()
                        if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation']):
                            game_over = True
        
        # Handle continuous movement when key is held down
        if not paused and not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
                if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation']):
                    current_piece['y'] += 1
                    last_move_time = current_time
            elif not keys[pygame.K_DOWN]:
                # Move piece down automatically
                if current_time - last_move_time > 1000:  # 1 second between automatic falls
                    if valid_move(current_piece, current_piece['x'], current_piece['y'] + 1, current_piece['rotation']):
                        current_piece['y'] += 1
                    else:
                        merge_piece(current_piece)
                        clear_lines()
                        current_piece = new_piece()
                        if not valid_move(current_piece, current_piece['x'], current_piece['y'], current_piece['rotation']):
                            game_over = True
                    last_move_time = current_time
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        if not game_over and not paused:
            draw_ghost_piece(current_piece)
            draw_piece(current_piece)
        draw_sidebar()
        draw_controls()
        
        if paused:
            draw_pause()
        elif game_over:
            draw_game_over()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

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
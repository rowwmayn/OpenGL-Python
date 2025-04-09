from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game states
PLAYING = 0
PAUSED = 1
GAME_OVER = 2

# Colors
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
BRIGHT_TEAL = (0.0, 0.8, 0.8)
AMBER = (1.0, 0.75, 0.0)
BACKGROUND = (0.1, 0.1, 0.2)

# Game variables
gameState = PLAYING
score = 0
diamondSpeed = 2.0  # Initial speed of falling diamonds
lastFrameTime = 0
catcher = {
    'x': WINDOW_WIDTH // 2,
    'y': 50,
    'width': 60,
    'height': 30,
    'color': WHITE
}
diamond = {
    'x': random.randint(50, WINDOW_WIDTH - 50),
    'y': WINDOW_HEIGHT - 50,
    'size': 20,
    'color': (random.random(), random.random(), random.random())
}
buttons = {
    'restart': {'x': 50, 'y': WINDOW_HEIGHT - 30, 'size': 15, 'color': BRIGHT_TEAL},
    'pause': {'x': WINDOW_WIDTH // 2, 'y': WINDOW_HEIGHT - 30, 'size': 15, 'color': AMBER},
    'quit': {'x': WINDOW_WIDTH - 50, 'y': WINDOW_HEIGHT - 30, 'size': 15, 'color': RED}
}

# Midpoint line algorithm
def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    # Cast to integers to avoid floating point issues
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    x, y = x1, y1
    
    while True:
        glVertex2f(x, y)
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    
    glEnd()

# Draw diamond using midpoint line algorithm
def draw_diamond(x, y, size, color):
    draw_line(x, y + size, x + size, y, color)  # Top-right line
    draw_line(x + size, y, x, y - size, color)  # Right-bottom line
    draw_line(x, y - size, x - size, y, color)  # Bottom-left line
    draw_line(x - size, y, x, y + size, color)  # Left-top line

# Draw catcher using midpoint line algorithm
def draw_catcher(x, y, width, height, color):
    half_width = width // 2
    draw_line(x - half_width, y, x - half_width + 10, y - height, color)  # Left side
    draw_line(x - half_width + 10, y - height, x + half_width - 10, y - height, color)  # Bottom
    draw_line(x + half_width - 10, y - height, x + half_width, y, color)  # Right side
    draw_line(x - half_width, y, x + half_width, y, color)  # Top

# Draw restart button (left arrow)
def draw_restart_button(x, y, size, color):
    draw_line(x - size, y, x + size, y, color)  # Horizontal line
    draw_line(x - size, y, x, y + size, color)  # Top diagonal
    draw_line(x - size, y, x, y - size, color)  # Bottom diagonal

# Draw play/pause button
def draw_pause_play_button(x, y, size, color):
    if gameState == PAUSED:
        # Play icon (triangle)
        draw_line(x - size // 2, y - size, x - size // 2, y + size, color)  # Left
        draw_line(x - size // 2, y - size, x + size, y, color)  # Bottom diagonal
        draw_line(x - size // 2, y + size, x + size, y, color)  # Top diagonal
    else:
        # Pause icon (two vertical lines)
        draw_line(x - size // 2, y - size, x - size // 2, y + size, color)  # Left line
        draw_line(x + size // 2, y - size, x + size // 2, y + size, color)  # Right line

# Draw quit button (cross)
def draw_quit_button(x, y, size, color):
    draw_line(x - size, y - size, x + size, y + size, color)  # Diagonal 1
    draw_line(x - size, y + size, x + size, y - size, color)  # Diagonal 2

# Check collision between diamond and catcher
def check_collision():
    half_width = catcher['width'] // 2
    # Check if the diamond's bottom point is within the catcher's range
    diamond_bottom_y = diamond['y'] - diamond['size']
    return (diamond_bottom_y <= catcher['y'] and 
            diamond_bottom_y >= catcher['y'] - catcher['height'] and
            diamond['x'] >= catcher['x'] - half_width and 
            diamond['x'] <= catcher['x'] + half_width)

# Check if diamond is missed
def check_missed():
    return diamond['y'] - diamond['size'] < 0

# Reset diamond position
def reset_diamond():
    diamond['x'] = random.randint(50, WINDOW_WIDTH - 50)
    diamond['y'] = WINDOW_HEIGHT - 50
    # Generate a random bright color
    r = random.uniform(0.5, 1.0)
    g = random.uniform(0.5, 1.0)
    b = random.uniform(0.5, 1.0)
    diamond['color'] = (r, g, b)

# Reset game
def reset_game():
    global gameState, score, diamondSpeed
    gameState = PLAYING
    score = 0
    diamondSpeed = 2.0
    catcher['color'] = WHITE
    catcher['x'] = WINDOW_WIDTH // 2
    reset_diamond()
    print("Starting Over")

# Display function
def display():
    try:
        glClearColor(*BACKGROUND, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw buttons
        draw_restart_button(buttons['restart']['x'], buttons['restart']['y'], 
                          buttons['restart']['size'], buttons['restart']['color'])
        draw_pause_play_button(buttons['pause']['x'], buttons['pause']['y'], 
                             buttons['pause']['size'], buttons['pause']['color'])
        draw_quit_button(buttons['quit']['x'], buttons['quit']['y'], 
                       buttons['quit']['size'], buttons['quit']['color'])
        
        # Draw diamond (only if not in game over state)
        if gameState != GAME_OVER:
            draw_diamond(diamond['x'], diamond['y'], diamond['size'], diamond['color'])
        
        # Draw catcher
        draw_catcher(catcher['x'], catcher['y'], catcher['width'], catcher['height'], catcher['color'])
        
        glutSwapBuffers()
    except OpenGL.error.GLError:
        # In case of OpenGL error, just swap buffers to prevent crashes
        glutSwapBuffers()

# Update game state - separated from rendering to avoid OpenGL errors
def update(value):
    global gameState, score, diamondSpeed, lastFrameTime
    
    currentTime = time.time()
    deltaTime = currentTime - lastFrameTime
    lastFrameTime = currentTime
    
    if gameState == PLAYING:
        # Move diamond
        diamond['y'] -= diamondSpeed
        
        # First check if diamond is missed
        if check_missed():
            gameState = GAME_OVER
            catcher['color'] = RED
            print(f"Game Over! Final Score: {score}")
        # Then check for collision
        elif check_collision():
            score += 1
            print(f"Score: {score}")
            reset_diamond()
            # Increase speed gradually
            diamondSpeed += 0.1
    
    glutPostRedisplay()
    # Ensure we continue the game loop
    glutTimerFunc(16, update, 0)

# Keyboard function for special keys (arrow keys)
def special_keys(key, x, y):
    if gameState == PLAYING:
        if key == GLUT_KEY_LEFT and catcher['x'] > catcher['width'] // 2:
            catcher['x'] -= 10
        elif key == GLUT_KEY_RIGHT and catcher['x'] < WINDOW_WIDTH - catcher['width'] // 2:
            catcher['x'] += 10

# Mouse function for button clicks
def mouse(button, state, x, y):
    global gameState
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert screen coordinates to OpenGL coordinates
        y = WINDOW_HEIGHT - y
        
        # Check restart button (square hit area for simplicity)
        if abs(x - buttons['restart']['x']) <= buttons['restart']['size'] * 2 and abs(y - buttons['restart']['y']) <= buttons['restart']['size'] * 2:
            reset_game()
        
        # Check pause button
        elif abs(x - buttons['pause']['x']) <= buttons['pause']['size'] * 2 and abs(y - buttons['pause']['y']) <= buttons['pause']['size'] * 2:
            if gameState == PLAYING:
                gameState = PAUSED
                print("Game Paused")
            elif gameState == PAUSED:
                gameState = PLAYING
                print("Game Resumed")
        
        # Check quit button
        elif abs(x - buttons['quit']['x']) <= buttons['quit']['size'] * 2 and abs(y - buttons['quit']['y']) <= buttons['quit']['size'] * 2:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

# Initialize OpenGL settings
def init():
    # Set up the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
    # Set up the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Set point size for drawing
    glPointSize(2.0)
    
    # Initialize time tracking
    global lastFrameTime
    lastFrameTime = time.time()

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    
    # Register callback functions
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)
    
    # Initialize OpenGL settings
    init()
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
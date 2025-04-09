from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PLAYING = 0
PAUSED = 1
GAME_OVER = 2
TINKU_MODE = 3

WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
BRIGHT_TEAL = (0.0, 0.8, 0.8)
AMBER = (1.0, 0.75, 0.0)
BACKGROUND = (0.1, 0.1, 0.2)
TINKU_COLOR = (1.0, 0.0, 1.0)

gameState = PLAYING
score = 0
diamondSpeed = 2.0
lastFrameTime = 0
catcher = {
    'x': WINDOW_WIDTH // 2,
    'y': 50,
    'width': 60,
    'height': 30,
    'color': WHITE,
    'original_width': 60,
    'original_height': 30
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

cheat_buffer = ""
cheat_timeout = 0
cheat_cooldown = 1.0

def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
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

def draw_diamond(x, y, size, color):
    draw_line(x, y + size, x + size, y, color)
    draw_line(x + size, y, x, y - size, color)
    draw_line(x, y - size, x - size, y, color)
    draw_line(x - size, y, x, y + size, color)

def draw_catcher(x, y, width, height, color):
    half_width = width // 2
    draw_line(x - half_width, y, x - half_width + 10, y - height, color)
    draw_line(x - half_width + 10, y - height, x + half_width - 10, y - height, color)
    draw_line(x + half_width - 10, y - height, x + half_width, y, color)
    draw_line(x - half_width, y, x + half_width, y, color)

def draw_restart_button(x, y, size, color):
    draw_line(x - size, y, x + size, y, color)
    draw_line(x - size, y, x, y + size, color)
    draw_line(x - size, y, x, y - size, color)

def draw_pause_play_button(x, y, size, color):
    if gameState == PAUSED:
        draw_line(x - size // 2, y - size, x - size // 2, y + size, color)
        draw_line(x - size // 2, y - size, x + size, y, color)
        draw_line(x - size // 2, y + size, x + size, y, color)
    else:
        draw_line(x - size // 2, y - size, x - size // 2, y + size, color)
        draw_line(x + size // 2, y - size, x + size // 2, y + size, color)

def draw_quit_button(x, y, size, color):
    draw_line(x - size, y - size, x + size, y + size, color)
    draw_line(x - size, y + size, x + size, y - size, color)

def check_collision():
    half_width = catcher['width'] // 2
    diamond_bottom_y = diamond['y'] - diamond['size']
    return (diamond_bottom_y <= catcher['y'] and 
            diamond_bottom_y >= catcher['y'] - catcher['height'] and
            diamond['x'] >= catcher['x'] - half_width and 
            diamond['x'] <= catcher['x'] + half_width)

def check_missed():
    return diamond['y'] - diamond['size'] < 0

def reset_diamond():
    diamond['x'] = random.randint(50, WINDOW_WIDTH - 50)
    diamond['y'] = WINDOW_HEIGHT - 50
    r = random.uniform(0.5, 1.0)
    g = random.uniform(0.5, 1.0)
    b = random.uniform(0.5, 1.0)
    diamond['color'] = (r, g, b)

def reset_game():
    global gameState, score, diamondSpeed
    gameState = PLAYING
    score = 0
    diamondSpeed = 2.0
    catcher['color'] = WHITE
    catcher['x'] = WINDOW_WIDTH // 2
    catcher['width'] = catcher['original_width']
    catcher['height'] = catcher['original_height']
    reset_diamond()
    print("Starting Over")

def process_cheat_code(code):
    global cheat_buffer, gameState
    
    if code == "long":
        catcher['width'] = catcher['original_width'] * 2
        catcher['height'] = catcher['original_height']
        print("Cheat activated: LONG catcher!")
    elif code == "big":
        catcher['width'] = catcher['original_width'] * 2
        catcher['height'] = catcher['original_height'] * 2
        print("Cheat activated: BIG catcher!")
    elif code == "oops":
        catcher['width'] = catcher['original_width']
        catcher['height'] = catcher['original_height']
        print("Cheat deactivated: Original catcher size restored.")
    elif code == "tinku":
        if gameState == PLAYING:
            gameState = TINKU_MODE
            catcher['color'] = TINKU_COLOR
            print("TINKU MODE activated! Control the diamond!")
    elif code == "notinku":
        if gameState == TINKU_MODE:
            gameState = PLAYING
            catcher['color'] = WHITE
            print("TINKU MODE deactivated. Back to normal.")
    
    cheat_buffer = ""

def display():
    try:
        glClearColor(*BACKGROUND, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        draw_restart_button(buttons['restart']['x'], buttons['restart']['y'], 
                          buttons['restart']['size'], buttons['restart']['color'])
        draw_pause_play_button(buttons['pause']['x'], buttons['pause']['y'], 
                             buttons['pause']['size'], buttons['pause']['color'])
        draw_quit_button(buttons['quit']['x'], buttons['quit']['y'], 
                       buttons['quit']['size'], buttons['quit']['color'])
        
        if gameState != GAME_OVER:
            draw_diamond(diamond['x'], diamond['y'], diamond['size'], diamond['color'])
        
        draw_catcher(catcher['x'], catcher['y'], catcher['width'], catcher['height'], catcher['color'])
        
        if gameState == TINKU_MODE:
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(10, WINDOW_HEIGHT - 20)
            for c in "TINKU MODE":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
        
        if cheat_buffer:
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(10, 10)
            for c in cheat_buffer:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
        
        glutSwapBuffers()
    except OpenGL.error.GLError:
        glutSwapBuffers()

def update(value):
    global gameState, score, diamondSpeed, lastFrameTime, cheat_timeout, cheat_buffer
    
    currentTime = time.time()
    deltaTime = currentTime - lastFrameTime
    lastFrameTime = currentTime
    
    if cheat_buffer and currentTime > cheat_timeout:
        cheat_buffer = ""
    
    if gameState == PLAYING:
        diamond['y'] -= diamondSpeed
        
        if check_missed():
            gameState = GAME_OVER
            catcher['color'] = RED
            print(f"Game Over! Final Score: {score}")
        elif check_collision():
            score += 1
            print(f"Score: {score}")
            reset_diamond()
            diamondSpeed += 0.1
    
    elif gameState == TINKU_MODE:
        if check_collision():
            score += 1
            print(f"Score: {score}")
            reset_diamond()
            diamondSpeed += 0.1
    
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def special_keys(key, x, y):
    if gameState == PLAYING:
        if key == GLUT_KEY_LEFT and catcher['x'] > catcher['width'] // 2:
            catcher['x'] -= 10
        elif key == GLUT_KEY_RIGHT and catcher['x'] < WINDOW_WIDTH - catcher['width'] // 2:
            catcher['x'] += 10
    
    elif gameState == TINKU_MODE:
        if key == GLUT_KEY_LEFT and diamond['x'] > diamond['size']:
            diamond['x'] -= 10
        elif key == GLUT_KEY_RIGHT and diamond['x'] < WINDOW_WIDTH - diamond['size']:
            diamond['x'] += 10
        elif key == GLUT_KEY_UP and diamond['y'] < WINDOW_HEIGHT - diamond['size']:
            diamond['y'] += 10
        elif key == GLUT_KEY_DOWN and diamond['y'] > diamond['size']:
            diamond['y'] -= 10

def keyboard(key, x, y):
    global cheat_buffer, cheat_timeout
    
    try:
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        
        if key.isalpha() or key.isdigit():
            if not cheat_buffer:
                cheat_timeout = time.time() + cheat_cooldown
            
            cheat_buffer += key.lower()
            
            if cheat_buffer in ["long", "big", "oops", "tinku", "notinku"]:
                process_cheat_code(cheat_buffer)
                
    except Exception as e:
        print(f"Keyboard error: {e}")

def mouse(button, state, x, y):
    global gameState
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = WINDOW_HEIGHT - y
        
        if abs(x - buttons['restart']['x']) <= buttons['restart']['size'] * 2 and abs(y - buttons['restart']['y']) <= buttons['restart']['size'] * 2:
            reset_game()
        
        elif abs(x - buttons['pause']['x']) <= buttons['pause']['size'] * 2 and abs(y - buttons['pause']['y']) <= buttons['pause']['size'] * 2:
            if gameState == PLAYING:
                gameState = PAUSED
                print("Game Paused")
            elif gameState == PAUSED:
                gameState = PLAYING
                print("Game Resumed")
            elif gameState == TINKU_MODE:
                gameState = PAUSED
                print("Game Paused (TINKU Mode)")
            elif gameState == PAUSED and catcher['color'] == TINKU_COLOR:
                gameState = TINKU_MODE
                print("Game Resumed (TINKU Mode)")
        
        elif abs(x - buttons['quit']['x']) <= buttons['quit']['size'] * 2 and abs(y - buttons['quit']['y']) <= buttons['quit']['size'] * 2:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glPointSize(2.0)
    
    global lastFrameTime
    lastFrameTime = time.time()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)
    
    init()
    
    glutMainLoop()

if __name__ == "__main__":
    main()
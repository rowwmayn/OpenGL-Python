from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window dimensions for both windows
width, height = 800, 600

# Global variables for rain
rain_x = []
rain_y = []
rain_speed = []
rain_angle = 0.0  # Controls the rain direction (0 = straight down)

# Global variables for day/night cycle
day_night = 0.5  # 0 = night, 1 = day
transition_speed = 0.01  # How fast day/night changes

# Movable points variables
points = []
speed_multiplier = 1.0
blinking = False
frozen = False

# Initialize rain positions
def init_rain(num_drops=40):
    for i in range(num_drops):
        rain_x.append(-10 + 20 * random.random())
        rain_y.append(10 - 5 * random.random())
        rain_speed.append(0.05 + 0.1 * random.random())

# Custom random function using math since we can't import random in OpenGL
def get_random_seed():
    return glutGet(GLUT_ELAPSED_TIME) / 1000.0

random.random = lambda: math.sin(get_random_seed() * len(rain_x) / 10.0) * 0.5 + 0.5

# Draw a simple house (for rain simulation)
def draw_house():
    house_color = adjust_color(0.8, 0.6, 0.4)
    roof_color = adjust_color(0.8, 0.2, 0.2)
    door_color = adjust_color(0.5, 0.3, 0.2)
    window_color = adjust_color(0.8, 0.8, 1.0)
    outline_color = adjust_color(0.2, 0.2, 0.2)
    
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3fv(outline_color)
    glVertex3f(-5, -5, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(5, 3, 0)
    glVertex3f(5, 3, 0)
    glVertex3f(-5, 3, 0)
    glVertex3f(-5, 3, 0)
    glVertex3f(-5, -5, 0)
    glVertex3f(-6, 3, 0)
    glVertex3f(6, 3, 0)
    glVertex3f(-6, 3, 0)
    glVertex3f(0, 7, 0)
    glVertex3f(0, 7, 0)
    glVertex3f(6, 3, 0)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3fv(house_color)
    glVertex3f(-5, -5, 0)  
    glVertex3f(5, -5, 0)   
    glVertex3f(-5, 3, 0)   
    
    glVertex3f(5, -5, 0)   
    glVertex3f(5, 3, 0)    
    glVertex3f(-5, 3, 0)   
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3fv(roof_color)
    glVertex3f(-6, 3, 0)   
    glVertex3f(6, 3, 0)    
    glVertex3f(0, 7, 0)    
    glEnd()

def adjust_color(r, g, b):
    darkness = 0.2 + 0.8 * day_night
    r_adjusted = r * darkness
    g_adjusted = g * darkness
    b_adjusted = b * darkness
    return [r_adjusted, g_adjusted, b_adjusted]

def draw_rain():
    rain_color = adjust_color(0.7, 0.7, 1.0)
    if day_night < 0.5:
        rain_color = [0.6, 0.6, 0.9]  
    glLineWidth(1.5)
    glBegin(GL_LINES)
    glColor3fv(rain_color)
    for i in range(len(rain_x)):
        x_offset = 0.5 * math.sin(math.radians(rain_angle))
        glVertex3f(rain_x[i], rain_y[i], 0)
        glVertex3f(rain_x[i] + x_offset, rain_y[i] - 0.5, 0)
    glEnd()

def update_rain():
    for i in range(len(rain_y)):
        rain_y[i] -= rain_speed[i]
        rain_x[i] += 0.02 * math.sin(math.radians(rain_angle))
        if rain_y[i] < -10 or rain_x[i] < -12 or rain_x[i] > 12:
            rain_x[i] = -10 + 20 * random.random()
            rain_y[i] = 10

def display_rain():
    bg_color = [day_night * 0.5, day_night * 0.7, day_night * 0.9, 1.0]
    glClearColor(bg_color[0], bg_color[1], bg_color[2], bg_color[3])
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def keyboard_rain(key, x, y):
    global rain_angle, day_night
    if key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle - 5, -45)  
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 5, 45)   
    glutPostRedisplay()

def normal_keyboard_rain(key, x, y):
    global day_night
    key = ord(key)
    if key == 100 or key == 68:
        day_night = min(day_night + transition_speed, 1.0)
    elif key == 110 or key == 78:
        day_night = max(day_night - transition_speed, 0.0)
    elif key == 27:
        exit(0)
    glutPostRedisplay()

def timer_rain(value):
    update_rain()
    glutPostRedisplay()
    glutTimerFunc(16, timer_rain, 0)

def reshape_rain(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW)

# Movable points logic
def add_point(x, y):
    dx = random.choice([-1, 1]) * speed_multiplier
    dy = random.choice([-1, 1]) * speed_multiplier
    color = [random.random(), random.random(), random.random()]
    points.append([x, y, dx, dy, color, color])

def move_points():
    if frozen:
        return
    for p in points:
        p[0] += p[2]
        p[1] += p[3]
        if p[0] <= 0 or p[0] >= width:
            p[2] *= -1
        if p[1] <= 0 or p[1] >= height:
            p[3] *= -1

def display_points():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(*p[4] if blinking else p[5])
        glVertex2f(p[0], p[1])
    glEnd()
    glutSwapBuffers()

def mouse_points(button, state, x, y):
    global blinking
    if frozen:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        add_point(x, height - y)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking

def special_keyboard_points(key, x, y):
    global speed_multiplier
    if frozen:
        return
    if key == GLUT_KEY_UP:
        speed_multiplier *= 1.2
    elif key == GLUT_KEY_DOWN:
        speed_multiplier *= 0.8
    for p in points:
        p[2] = (p[2] / abs(p[2])) * speed_multiplier if p[2] != 0 else p[2]
        p[3] = (p[3] / abs(p[3])) * speed_multiplier if p[3] != 0 else p[3]

def normal_keyboard_points(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

def update_points(value):
    move_points()
    glutPostRedisplay()
    glutTimerFunc(10, update_points, 0)

def reshape_points(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)

# Main function to initialize both windows
def main():
    # Create the first window (rain simulation)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    window1 = glutCreateWindow("Rain Simulation")
    glClearColor(0.5, 0.7, 0.9, 1.0)
    glutDisplayFunc(display_rain)
    glutKeyboardFunc(normal_keyboard_rain)
    glutReshapeFunc(reshape_rain)
    glutSpecialFunc(keyboard_rain)
    glutTimerFunc(16, timer_rain, 0)
    init_rain()

    # Create the second window (movable points)
    window2 = glutCreateWindow("Movable Points OpenGL")
    glClearColor(0, 0, 0, 1)
    glutDisplayFunc(display_points)
    glutMouseFunc(mouse_points)
    glutReshapeFunc(reshape_points)
    glutSpecialFunc(special_keyboard_points)
    glutKeyboardFunc(normal_keyboard_points)
    glutTimerFunc(10, update_points, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()

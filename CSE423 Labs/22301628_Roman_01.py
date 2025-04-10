from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

width, height = 800, 600
rain_x, rain_y, rain_speed = [], [], []
rain_angle = 0.0
day_night = 0.5
transition_speed = 0.01

def init_rain(num_drops=40):
    for i in range(num_drops):
        rain_x.append(-10 + 20 * math.random())
        rain_y.append(10 - 5 * math.random())
        rain_speed.append(0.05 + 0.1 * math.random())

def get_random_seed():
    return glutGet(GLUT_ELAPSED_TIME) / 1000.0

math.random = lambda: math.sin(get_random_seed() * len(rain_x) / 10.0) * 0.5 + 0.5

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
    glBegin(GL_TRIANGLES)
    glColor3fv(door_color)
    glVertex3f(-1.5, -5, 0)
    glVertex3f(1.5, -5, 0)
    glVertex3f(1.5, 0, 0)
    glVertex3f(-1.5, -5, 0)
    glVertex3f(-1.5, 0, 0)
    glVertex3f(1.5, 0, 0)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3fv(window_color)
    glVertex3f(-4, 0, 0)
    glVertex3f(-2, 0, 0)
    glVertex3f(-2, 2, 0)
    glVertex3f(-4, 0, 0)
    glVertex3f(-4, 2, 0)
    glVertex3f(-2, 2, 0)
    glVertex3f(2, 0, 0)
    glVertex3f(4, 0, 0)
    glVertex3f(4, 2, 0)
    glVertex3f(2, 0, 0)
    glVertex3f(2, 2, 0)
    glVertex3f(4, 2, 0)
    glEnd()
    glBegin(GL_LINES)
    glColor3fv(outline_color)
    glVertex3f(-3, 0, 0)
    glVertex3f(-3, 2, 0)
    glVertex3f(-4, 1, 0)
    glVertex3f(-2, 1, 0)
    glVertex3f(3, 0, 0)
    glVertex3f(3, 2, 0)
    glVertex3f(2, 1, 0)
    glVertex3f(4, 1, 0)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3fv(adjust_color(0.6, 0.6, 0.6))
    glVertex3f(3, 4, 0)
    glVertex3f(4, 4, 0)
    glVertex3f(3, 6, 0)
    glVertex3f(4, 4, 0)
    glVertex3f(4, 6, 0)
    glVertex3f(3, 6, 0)
    glEnd()

def adjust_color(r, g, b):
    darkness = 0.2 + 0.8 * day_night
    return [r * darkness, g * darkness, b * darkness]

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
            rain_x[i] = -10 + 20 * math.random()
            rain_y[i] = 10

def keyboard(key, x, y):
    global rain_angle, day_night
    if key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle - 5, -45)
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 5, 45)
    glutPostRedisplay()

def normal_keyboard(key, x, y):
    global day_night
    key = ord(key)
    if key == 100 or key == 68:
        day_night = min(day_night + transition_speed, 1.0)
    elif key == 110 or key == 78:
        day_night = max(day_night - transition_speed, 0.0)
    elif key == 27:
        exit(0)
    glutPostRedisplay()

def display():
    bg_color = [day_night * 0.5, day_night * 0.7, day_night * 0.9, 1.0]
    glClearColor(bg_color[0], bg_color[1], bg_color[2], bg_color[3])
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    draw_rain()
    draw_instructions()
    glutSwapBuffers()

def draw_instructions():
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(-9.5, 9)
    text = "Controls: Left/Right Arrows - Change rain direction | D - Day | N - Night"
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

def timer(value):
    update_rain()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW)

def init():
    glClearColor(0.5, 0.7, 0.9, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    init_rain()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Interactive House with Rain")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(keyboard)
    glutKeyboardFunc(normal_keyboard)
    glutTimerFunc(16, timer, 0)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()




# This is task 2. Uncomment the code below and run it to see the output. (But comment out the above code before running this code)

'''
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

WIDTH, HEIGHT = 800, 600
points = []
speed_multiplier = 1.0
blinking = False
frozen = False

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
        if p[0] <= 0 or p[0] >= WIDTH:
            p[2] *= -1
        if p[1] <= 0 or p[1] >= HEIGHT:
            p[3] *= -1

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(*p[4] if blinking else p[5])
        glVertex2f(p[0], p[1])
    glEnd()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global blinking
    if frozen:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        add_point(x, HEIGHT - y)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking

def special_keyboard(key, x, y):
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

def normal_keyboard(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

def update(value):
    move_points()
    glutPostRedisplay()
    glutTimerFunc(10, update, 0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("Movable Points OpenGL")
    glClearColor(0, 0, 0, 1)
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_keyboard)
    glutKeyboardFunc(normal_keyboard)
    glutTimerFunc(10, update, 0)
    glutMainLoop()

main()


'''    
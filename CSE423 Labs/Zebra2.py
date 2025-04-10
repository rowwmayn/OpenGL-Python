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
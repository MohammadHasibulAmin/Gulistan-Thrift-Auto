from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

# =========================
# CAMERA & GAME STATE
# =========================


cam_distance = 700
cam_angle = 0
camera_pos = [20, 200, 200]
cam_movement_speed = 10

enemy_radius = 80
gun_angle = 270
rad_angle = math.radians(gun_angle)

building_heights = []
fovY = 60  # Field of view
bound_l = -50
bound_r = 100

# BULLET FORMAT: (x, y, angle, weapon_name, z)
bullets = []

fpv = False
player_pos = (0, 0, 0)
enemy_pos = enemy_pos = [[random.randint(-45, 45), random.randint(-2000, 400)] for _ in range(2)]

#PICKPOCKETING VARIABLES
money = 0
pickpocket_active = False; pickpocket_start_time = 0.0; pickpocket_enemy_index = None

default_fov = fovY

sniper = False; assault = False

GRID_LENGTH = 1000;
dress_color = [0.5, 0.5, 1]; 
missed = 0; points = 0; player_life = 5; game = True

near_car = False
driving_car = None
car_specs = [
    (0, 0, 'sport', [random.uniform(0.1, 0.8), random.uniform(0.1, 0.8), random.uniform(0.1, 0.8)]),
    (35, -200, 'sedan', [random.uniform(0.1, 0.8), random.uniform(0.1, 0.8), random.uniform(0.1, 0.8)]),
    (-35, -400, 'suv', [random.uniform(0.1, 0.8), random.uniform(0.1, 0.8), random.uniform(0.1, 0.8)])
]
in_car = False

look_at = (500 * math.sin(rad_angle), 500 * math.cos(rad_angle), 50)

# =========================
# WEAPONS
# =========================

WEAPONS = {
    "pistol": {
        "fire_mode": "single",
        "fire_rate": 10,
        "bullet_speed": 1,
        "size": 10,
        "color": (1, 0, 0),
        "zoom_fov": None
    },
    "auto": {
        "fire_mode": "auto",
        "fire_rate": 3,
        "bullet_speed": 3,
        "size": 8,
        "color": (1, 1, 0),
        "zoom_fov": None
    },
    "sniper": {
        "fire_mode": "single",
        "fire_rate": 1,
        "bullet_speed": 4,
        "size": 12,
        "color": (0, 1, 1),
        "zoom_fov": 80
    }
}

current_weapon = "pistol"
fire_cooldown = 0
is_firing = False

def draw_roads():
    glBegin(GL_QUADS)
    # road
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(-50, -2000, 0)
    glVertex3f(50, -2000, 0)
    glVertex3f(50, 400, 0)
    glVertex3f(-50, 400, 0)

    # intersection
    glVertex3f(-400, -50, 0)
    glVertex3f(-50, -50, 0)
    glVertex3f(-50, 50, 0)
    glVertex3f(-400, 50, 0)

    glColor3f(0.45, 0.45, 0.45)
    glVertex3f(-400, -100, 0)
    glVertex3f(-50, -100, 0)
    glVertex3f(-50, 50, 0)
    glVertex3f(-400, 50, 0)

    glVertex3f(-400, 50, 0)
    glVertex3f(-50, 50, 0)
    glVertex3f(-50, 100, 0)
    glVertex3f(-400, 100, 0)       

    # sidewalk left
    glColor3f(0.45, 0.45, 0.45)
    glVertex3f(-100, -2000, 0)
    glVertex3f(-50, -2000, 0)
    glVertex3f(-50, 400, 0)
    glVertex3f(-100, 400, 0)

    # sidewalk right
    glVertex3f(100, -2000, 0)
    glVertex3f(50, -2000, 0)
    glVertex3f(50, 400, 0)
    glVertex3f(100, 400, 0)

    # river
    glColor3f(0.12, 0.35, 0.55)
    glVertex3f(2000, -2000, 0)
    glVertex3f(100, -2000, 0)
    glVertex3f(100, 400, 0)
    glVertex3f(400, 400, 0)
    glEnd()


def init_buildings():
    global building_heights
    start_y = -2000
    end_y = 400
    building_width = 50
    gap = 80
    min_height = 100
    max_height = 200

    y = start_y
    while y < end_y:
        height = random.randint(min_height, max_height)
        color = (random.random(), random.random(), random.random())
        building_heights.append((y, height, color))
        y += building_width + gap


def draw_buildings():
    start_x = -100
    end_x = -50
    building_width = end_x - start_x
    center_x = (start_x + end_x) / 2
    counter = 0
    for y, height, color in building_heights:
        center_y = y + building_width / 2
        if -50 <= center_y <= 50:
            continue
        glPushMatrix()
        glTranslatef(center_x, center_y, height / 2)
        r, g, b = color
        if counter == 12:
            r = g = b = 0
        elif counter ==13:
            r = 0.55
            g = 0.27
            b = 0.07
        elif counter == 14:
            r = 1.0
            g = 0.4
            b = 0.7            

        glColor3f(r, g, b)
        glScalef(building_width, building_width, height)
        glutSolidCube(1)
        glPopMatrix()

        counter += 1



def draw_sky():
    glBegin(GL_QUADS)
    glColor3f(0.53, 0.81, 0.92)

    # BACK
    glVertex3f(-3000, -3000, -3000)
    glVertex3f( 3000, -3000, -3000)
    glVertex3f( 3000, -3000, 3000)
    glVertex3f(-3000, -3000, 3000)

    # LEFT
    glVertex3f(-2000, -3000, -8000)
    glVertex3f(-2000,  3000, -8000)
    glVertex3f(-2000,  3000, 3000)
    glVertex3f(-2000, -3000, 3000)


    # TOP
    glVertex3f(-3000, 2000, -6000)
    glVertex3f( 3000, 3000, -6000)
    glVertex3f( 3000, 3000, 3000)
    glVertex3f(-3000, 2000, 3000)
    glEnd()

class Car:
    def __init__(self, x = 0, y = 0, angle = 0, color = (1,0,0)):
        self.x = x

        self.y = y
        self.angle = angle
        self.color = color

        self.speed = 0.0
        self.height = 10
        self.type = None
        self.controlled = False
    # ----------------- CAR TYPES -----------------
    def Sport(self):
        self.speed = 1
        self.height = 10
        self.type = 'sport'

    def Sedan(self):
        self.speed = 0.5
        self.height = 20
        self.type = 'sedan'

    def SUV(self):
        self.speed = 0.25
        self.height = 30
        self.type = 'suv'

    # ----------------- DRAW HELPERS -----------------
    def draw_wheel(self):
        glPushMatrix()

        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 6, 6, 5, 20, 20)
        glPopMatrix()

    def draw_headlight(self, offset_x):
        glPushMatrix()

        glTranslatef(offset_x, 26, 4)
        glColor3f(1, 1, 0.8)
        glutSolidCube(4)
        glPopMatrix()

    # ----------------- DRAW CAR -----------------
    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, self.height / 2)
        glRotatef(self.angle, 0, 0, 1)

        # Body
        glColor3f(self.color[0], self.color[1], self.color[2])
        glPushMatrix()
        glScalef( 1.5, 2.5, self.height / 20)
        glutSolidCube(20)
        glPopMatrix()

        # Wheels
        glColor3f(0, 0, 0)
        wheel_positions = [
            (-15, 18, -self.height/2),
            (15, 18, -self.height/2),
            (-15, -18, -self.height/2),
            (15, -18, -self.height/2)
        ]

        for wx, wy, wz in wheel_positions:
            glPushMatrix()
            glTranslatef(wx, wy, wz)
            self.draw_wheel()
            glPopMatrix()

        # Headlights
        self.draw_headlight(-6)
        self.draw_headlight(6)

        glPopMatrix()

    # ----------------- MOVEMENT -----------------
    def move_backward(self):
        rad = math.radians(self.angle - 90)
        dx = math.cos(rad) * self.speed * 5
        dy = math.sin(rad) * self.speed * 5

        new_x = self.x + dx
        new_y = self.y + dy

        road1 = (-50 <= new_x <= 50 and -2000 <= new_y <= 400)
        intersection = (-400 <= new_x <= -50 and -50 <= new_y <= 50)

        if road1 or intersection:
            self.x = new_x
            self.y = new_y

    def move_forward(self):
        rad = math.radians(self.angle - 90)
        dx = math.cos(rad) * self.speed * 5
        dy = math.sin(rad) * self.speed * 5

        new_x = self.x - dx
        new_y = self.y - dy

        road1 = (-50 <= new_x <= 50 and -2000 <= new_y <= 400)
        intersection = (-400 <= new_x <= -50 and -50 <= new_y <= 50)

        if road1 or intersection:
            self.x = new_x
            self.y = new_y          

    def turn_left(self):
        self.angle += 3

    def turn_right(self):
        self.angle -= 3

cars = []
for x, y, typ, color in car_specs:
    c = Car(x, y, 0, color)
    if typ == 'sport':
        c.Sport()
    elif typ == 'sedan':
        c.Sedan()
    elif typ == 'suv':
        c.SUV()
    cars.append(c)

def angle_calculator(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18): # type: ignore
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_enemies():
    global enemy_pos, enemy_radius

    ENEMY_SCALE = 0.20

    quad = gluNewQuadric()

    for x, y in enemy_pos:
        glPushMatrix()

        glTranslatef(x, y, 0)

        glScalef(ENEMY_SCALE, ENEMY_SCALE, ENEMY_SCALE)

        # Body
        glColor3f(1, 0.1, 0.1)
        glTranslatef(0, 0, enemy_radius)
        gluSphere(quad, enemy_radius, 12, 12)

        # Head
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, enemy_radius + 25)
        gluSphere(quad, 50, 12, 12)

        glPopMatrix()

def draw_bullet(weapon_name):
    w = WEAPONS[weapon_name]
    glColor3f(*w["color"])
    glutSolidCube(w["size"])

def draw_player():
    global player_pos, gun_angle, current_weapon,dress_color
    scale_factor = 0.25

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(gun_angle, 0, 0, 1)

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 100 * scale_factor)
    glColor3f(dress_color[0],dress_color[1],dress_color[2])
    glScalef(1, 2, 2.5)
    glScalef(scale_factor, scale_factor, scale_factor)
    glutSolidCube(50)
    glPopMatrix()

    # Legs
    glColor3f(1, 0.7, 0.7)
    glTranslatef(0, 50 * scale_factor, 150 * scale_factor)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20 * scale_factor, 10 * scale_factor, 100 * scale_factor, 10, 10)
    glTranslatef(0, -100 * scale_factor, 0)
    gluCylinder(gluNewQuadric(), 20 * scale_factor, 10 * scale_factor, 100 * scale_factor, 10, 10)

    # Arms
    glColor3f(0.7, 0.7, 1)
    glTranslatef(110 * scale_factor, 20 * scale_factor, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20 * scale_factor, 10 * scale_factor, 70 * scale_factor, 10, 10)
    glTranslatef(0, 60 * scale_factor, 0)
    gluCylinder(gluNewQuadric(), 20 * scale_factor, 10 * scale_factor, 70 * scale_factor, 10, 10)

    # Gun barrel
    glColor3f(1.0, 0.0, 1.0)
    glTranslatef(0, -30 * scale_factor, -110 * scale_factor)
    glRotatef(-90, 0, 1, 0)
    if current_weapon == "pistol":
        gluCylinder(gluNewQuadric(), 15 * scale_factor, 5 * scale_factor, 120 * scale_factor, 10, 10)
    elif current_weapon == "auto":
        gluCylinder(gluNewQuadric(), 12 * scale_factor, 3 * scale_factor, 120 * scale_factor, 10, 10)
    elif current_weapon == "sniper":
        gluCylinder(gluNewQuadric(), 20 * scale_factor, 10 * scale_factor, 120 * scale_factor, 10, 10)

    # Head
    glColor3f(1, 0.7, 0.7)
    glTranslatef(-30 * scale_factor, 0, 0)
    gluSphere(gluNewQuadric(), 30 * scale_factor, 10, 10)

    glPopMatrix()


# =========================
# INPUT
# =========================

def keyboardListener(key, x, y):
    global gun_angle, rad_angle, current_weapon, fovY, fpv, player_pos, look_at, in_car, near_car, driving_car, cars,sniper,AR
    global money, pickpocket_active, pickpocket_enemy_index,dress_color,money,sniper,assault

    a, b, c = player_pos
    rad_angle = math.radians(gun_angle)
    dir_x = math.cos(rad_angle)
    dir_y = math.sin(rad_angle)
    move_speed = 10.0

    if key == b'w':
        if in_car and driving_car is not None:
            driving_car.move_forward()
        else:
            new_a = a + move_speed * dir_x
            new_b = b + move_speed * dir_y
            # main road
            if (-50<= new_a <= 100 and -2000 <= new_b <= 400):
                player_pos = (new_a, new_b, c)

            # intersection (right/left road)
            elif (-400 <= new_a <= -50 and -50 <= new_b <= 50):
                player_pos = (new_a, new_b, c)

            if -460<=new_b<=-370 and new_a<-45:
                if money>=30:
                    sniper = True
                    money-=30

            if -310<=new_b<=-260 and new_a<-45:
                if money>=20:
                    assault = True
                    money-=20

            if -180<=new_b<=-130 and new_a<-45: 
                dress_color = [random.random(),random.random(),random.random()]        
                        

    if key == b's':
        if in_car and driving_car is not None:
            driving_car.move_backward()
        else:        
            new_a = a - move_speed * dir_x
            new_b = b - move_speed * dir_y
            if (-50 <= new_a <= 50 and -2000 <= new_b <= 400):
                player_pos = (new_a, new_b, c)

            # intersection
            elif (-400 <= new_a <= -50 and -50 <= new_b <= 50):
                player_pos = (new_a, new_b, c)

            if -460<=new_b<=-370 and new_a<-45:
                if money>=30:
                    sniper = True   
                    money -=30             

            if -310<=new_b<=-260 and new_a<-45:
                if money>=20:
                    assault = True  
                    money -=20 

            if -180<=new_b<=-130 and new_a<-45: 
                dress_color = [random.random(),random.random(),random.random()]
                   

    if key == b'a':
        if in_car and driving_car is not None:
            driving_car.turn_left()
        else:        
            gun_angle += 5
    if key == b'd':
        if in_car and driving_car is not None:
            driving_car.turn_right()
        else:        
            gun_angle -= 5
    if key == b'1':
        current_weapon = "pistol"
        fovY = default_fov
    if key == b'2':
        if assault:
            current_weapon = "auto"
            fovY = default_fov
    if key == b'3':
        if sniper:
            current_weapon = "sniper"
            fpv = True

    if key == b'f':
        if not in_car:
            nearest = None
            best_d = float('inf')
            for car in cars:
                d = math.hypot(car.x - player_pos[0], car.y - player_pos[1])
                if d < best_d:
                    best_d = d
                    nearest = car
            if nearest is not None and best_d <= 50:
                nearest.controlled = True
                in_car = True
                driving_car = nearest
                player_pos = (driving_car.x, driving_car.y, driving_car.height / 2)
        else:
            if driving_car is not None:
                player_pos = (driving_car.x + 60, driving_car.y, 0)
                driving_car.controlled = False
            in_car = False
            driving_car = None   

    rad_angle = math.radians(gun_angle)

    if key == b'x':
        if pickpocket_active and pickpocket_enemy_index is not None:
            money += 10
            enemy_pos[pickpocket_enemy_index] = [
                random.randint(-45, 45),
                random.randint(-2000, 400)
            ]
            pickpocket_active = False
            pickpocket_enemy_index = None


def mouseListener(button, state, x, y):
    global is_firing, fpv, fovY, current_weapon, default_fov, in_car

    if in_car:
        return
    
    if button == GLUT_LEFT_BUTTON:
        is_firing = (state == GLUT_DOWN)

    if button == GLUT_RIGHT_BUTTON:
        if current_weapon == "sniper":
            # Right-click for sniper zoom
            if state == GLUT_DOWN:
                fpv = True
                fovY = WEAPONS["sniper"]["zoom_fov"]
            elif state == GLUT_UP:
                fpv = False
                fovY = default_fov


# =========================
# CAMERA
# =========================

def setupCamera():
    global fpv
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 5000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if fpv:
        dx = math.cos(rad_angle)
        dy = math.sin(rad_angle)
        x, y, z = player_pos
        gluLookAt(
            x, y, z + 60,
            x + dx * 500, y + dy * 500, z + 60,
            0, 0, 1
        )
    else:
        cx, cy, cz = camera_pos
        px, py, pz = player_pos
        gluLookAt(cx, cy, cz, px, py, pz, 0, 0, 1)


# =========================
# GAME LOOP
# =========================

def idle():
    global fire_cooldown, bullets, missed, points, is_firing
    global player_pos
    global pickpocket_active, pickpocket_start_time, pickpocket_enemy_index

    if not game:
        glutPostRedisplay()
        return


    for idx, enemy in enumerate(enemy_pos):
        d_x = player_pos[0] - enemy[0]
        d_y = player_pos[1] - enemy[1]
        distance = math.sqrt(d_x ** 2 + d_y ** 2)

        # ---- pickpocket distance deadzone ----
        if pickpocket_active and pickpocket_enemy_index is not None:
            e = enemy_pos[pickpocket_enemy_index]
            if math.dist((player_pos[0], player_pos[1]), (e[0], e[1])) > 40:
                pickpocket_active = False
                pickpocket_enemy_index = None

        # ---- picpocket chance ----
        if 20 <= distance <= 40 and not pickpocket_active:
            pickpocket_active = True
            pickpocket_start_time = time.time()
            pickpocket_enemy_index = idx

        # ---- chance over ----
        if pickpocket_active:
            if time.time() - pickpocket_start_time > 2.0:
                pickpocket_active = False
                pickpocket_enemy_index = None

        # ---- enemy attack ----
        if distance < 20:
            enemy[:] = [random.randint(-45, 45), random.randint(-2000, 400)]
            pickpocket_active = False
            pickpocket_enemy_index = None

        if distance > 0:
            move_speed = 0.01
            enemy[0] += (d_x / distance) * move_speed
            enemy[1] += (d_y / distance) * move_speed

    weapon = WEAPONS[current_weapon]
    scale_factor = 0.25

    if fire_cooldown > 0:
        fire_cooldown -= 1

    if is_firing and fire_cooldown == 0:
        bullet_spawn_z = player_pos[2] + 100 * scale_factor
        bullets.append((player_pos[0], player_pos[1], gun_angle, current_weapon, bullet_spawn_z))
        fire_cooldown = int(60 / weapon["fire_rate"])
        if weapon["fire_mode"] == "single":
            is_firing = False

    new_bullets = []
    for b_x, b_y, angle, weapon_name, b_z in bullets:
        w = WEAPONS[weapon_name]
        dir_x = math.cos(math.radians(angle))
        dir_y = math.sin(math.radians(angle))
        b_x += w["bullet_speed"] * dir_x
        b_y += w["bullet_speed"] * dir_y

        hit = False
        for i, (e_x, e_y) in enumerate(enemy_pos):
            if math.dist((b_x, b_y), (e_x, e_y)) <= enemy_radius:
                enemy_pos[i] = [random.randint(-45, 45), random.randint(-2000, 400)]
                points += 1
                hit = True
                break

        if not hit and abs(b_x) < 2000 and abs(b_y) < 2000:
            new_bullets.append((b_x, b_y, angle, weapon_name, b_z))
        else:
            missed += 1

    bullets = new_bullets
    near_car = False
    for car in cars:
        if not getattr(car, 'controlled', False):
            car.y += car.speed
            if car.y > GRID_LENGTH:
                car.y = -2000

        if abs(car.x - player_pos[0]) <= 50 and abs(car.y - player_pos[1]) <= 50:
            near_car = True

    if in_car and driving_car is not None:
        player_pos = (driving_car.x, driving_car.y, driving_car.height / 2)

    glutPostRedisplay()


# =========================
# RENDER
# =========================

def showScreen():
    global money

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 1000, cam_distance)
    setupCamera()

    draw_sky()
    draw_roads()
    draw_buildings()
    draw_enemies()
    if not in_car:
        draw_player()

    # Draw bullets
    for b_x, b_y, angle, weapon_name, b_z in bullets:
        glPushMatrix()
        glTranslatef(b_x, b_y, b_z)
        draw_bullet(weapon_name)
        glPopMatrix()
    glPushMatrix()    
    for car in cars:
        car.draw()
    glPopMatrix()

    if pickpocket_active:
        draw_text(350, cam_distance - 40, "Press X to pickpocket")
    
    draw_text(10, 775, f"money: {money}")
    draw_text(10,715,"Black Building - Buy SNIPER")
    draw_text(10,680,"Brown Building - Buy Assault Rifle")
    draw_text(10,645,"Pink Building - Shopping Mall")

    draw_text(10,605,"Assault Rifle - Press 2")
    draw_text(10,570,"Sniper - Press 3")
    draw_text(10,530,"Right Click for Scope")
    glutSwapBuffers()


# =========================
# MAIN
# =========================

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, cam_distance)
    glutCreateWindow(b"Gulistan Thrift Auto")

    init_buildings()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

    glutMainLoop()


if __name__ == "__main__":
    main()
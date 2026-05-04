import pgzrun
import pygame
import random

# globale Variablen
WIDTH = 1280
HEIGHT = 720
MOVE_SPEED = 5

# Bilder Asteroiden
ASTEROID_IMAGES = [
    "meteorbrown_big1",
    "meteorbrown_med1",
    "meteorbrown_small1",
    "meteorgrey_med1",
]
ASTEROIDS = []

# Raumschiff
Raumschiff = Actor("playership2_red", anchor=("center", "bottom"))
Raumschiff.pos = (WIDTH // 2, HEIGHT // 2)

Raumschiff.vx = 0
Raumschiff.vy = 0
Raumschiff.on_ground = False

#Zufälliges Spawnen von Asteroiden
def spawn_asteroid():
    image_name = random.choice(ASTEROID_IMAGES)
    asteroid = Actor(image_name)

    side = random.choice(["top", "bottom", "left", "right"])
    speed = random.uniform(2.0, 4.5)
    angle = random.uniform(-1.0, 1.0)

    if side == "top":
        asteroid.midbottom = (random.randint(0, WIDTH), -20)
        asteroid.vx = angle
        asteroid.vy = speed
    elif side == "bottom":
        asteroid.midtop = (random.randint(0, WIDTH), HEIGHT + 20)
        asteroid.vx = angle
        asteroid.vy = -speed
    elif side == "left":
        asteroid.midright = (-20, random.randint(0, HEIGHT))
        asteroid.vx = speed
        asteroid.vy = angle
    else: 
        asteroid.midleft = (WIDTH + 20, random.randint(0, HEIGHT))
        asteroid.vx = -speed
        asteroid.vy = angle

    asteroid.angle = random.randint(0, 360)
    asteroid.rotation_speed = random.uniform(-2.0, 2.0)
    ASTEROIDS.append(asteroid)


def draw():
    # Zeichne Hintergrund skaliert auf Fenstergröße
    hintergrund = images.load("hintergrund")
    scaled_hintergrund = pygame.transform.scale(hintergrund, (WIDTH, HEIGHT))
    screen.blit(scaled_hintergrund, (0, 0))

    # Zeichne Asteroiden
    for asteroid in ASTEROIDS:
        asteroid.draw()

    # Zeichne Raumschiff
    Raumschiff.draw()


def update():
    # x-Geschwindigkeit berechnen (links/rechts)
    Raumschiff.vx = 0
    if keyboard.left:
        Raumschiff.vx = -MOVE_SPEED
    elif keyboard.right:
        Raumschiff.vx = MOVE_SPEED

    # x-Bewegung ausführen
    Raumschiff.x += Raumschiff.vx
    # y-Bewegung berechnen
    Raumschiff.vy = 0
    if keyboard.up:
        Raumschiff.vy = -MOVE_SPEED
    elif keyboard.down:
        Raumschiff.vy = MOVE_SPEED

    # y-Bewegung ausführen
    Raumschiff.y += Raumschiff.vy

    # Asteroiden zufällig erzeugen
    if random.random() < 0.02:
        spawn_asteroid()

    # Asteroiden bewegen und rotieren
    for asteroid in ASTEROIDS[:]:
        asteroid.x += asteroid.vx
        asteroid.y += asteroid.vy
        asteroid.angle += asteroid.rotation_speed

        if (
            asteroid.x < -100
            or asteroid.x > WIDTH + 100
            or asteroid.y < -100
            or asteroid.y > HEIGHT + 100
        ):
            ASTEROIDS.remove(asteroid)

pgzrun.go()
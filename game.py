import pgzrun
import pygame
import random
import math

WIDTH, HEIGHT, MOVE_SPEED = 1280, 720, 5
ROTATION_SPEED = 3
ASTEROID_IMAGES = ["meteorbrown_big1", "meteorbrown_med1", "meteorbrown_small1", "meteorgrey_med1"]
ASTEROIDS = []
game_over = False

# Raumschiff
Raumschiff = Actor("playership2_red", anchor=("center", "top"))
Raumschiff.pos = (WIDTH // 2, HEIGHT // 2)
Raumschiff.vx = Raumschiff.vy = 0
Raumschiff.angle = 0

#Zufälliges Spawnen von Asteroiden
def spawn_asteroid():
    asteroid = Actor(random.choice(ASTEROID_IMAGES))
    side = random.choice(["top", "bottom", "left", "right"])
    speed = random.uniform(2.0, 4.5)
    angle = random.uniform(-1.0, 1.0)
    #spawnen Asteroiden von unterschiedlichen Seiten, Geschwindigkeit und Winkel abhängig von Seite
    if side == "top":
        asteroid.midbottom = (random.randint(0, WIDTH), -20)
        asteroid.vx, asteroid.vy = angle, speed
    elif side == "bottom":
        asteroid.midtop = (random.randint(0, WIDTH), HEIGHT + 20)
        asteroid.vx, asteroid.vy = angle, -speed
    elif side == "left":
        asteroid.midright = (-20, random.randint(0, HEIGHT))
        asteroid.vx, asteroid.vy = speed, angle
    else:
        asteroid.midleft = (WIDTH + 20, random.randint(0, HEIGHT))
        asteroid.vx, asteroid.vy = -speed, angle
    
    asteroid.angle = random.randint(0, 360)
    asteroid.rotation_speed = random.uniform(-2.0, 2.0)
    ASTEROIDS.append(asteroid)


def check_collision():
    global game_over
    for asteroid in ASTEROIDS:
        if Raumschiff.colliderect(asteroid):
            game_over = True
            return True
    return False


def reset_game():
    global game_over, ASTEROIDS
    game_over = False
    ASTEROIDS.clear()
    Raumschiff.pos = (WIDTH // 2, HEIGHT // 2)
    Raumschiff.vx = Raumschiff.vy = 0
    Raumschiff.angle = 0


def draw():
    screen.blit(pygame.transform.scale(images.load("hintergrund"), (WIDTH, HEIGHT)), (0, 0))
    for asteroid in ASTEROIDS:
        asteroid.draw()

    # Zeichne Raumschiff wenn Spiel nicht vorbei
    if not game_over:
        Raumschiff.draw()
    else:
        screen.draw.text("GAME OVER!", (WIDTH // 2 - 100, HEIGHT // 2 - 50), fontsize=80, color="red")
        screen.draw.text("Drücke LEERTASTE zum Neustart", (WIDTH // 2 - 77, HEIGHT // 2 + 20), fontsize=30, color="white")


def update():
    # Wenn Spiel vorbei ist, prüfe auf Neustart mit Leertaste
    if game_over:
        if keyboard.space:
            reset_game()
        return
    
    # Drehen mit links/rechts Pfeiltasten
    if keyboard.left:
        Raumschiff.angle += ROTATION_SPEED
    if keyboard.right:
        Raumschiff.angle -= ROTATION_SPEED
    
    # Bewegung basierend auf Winkel mit oben/unten Pfeiltasten
    if keyboard.up or keyboard.down:
        radians = math.radians(Raumschiff.angle)
        direction = 1 if keyboard.up else -1
        Raumschiff.vx = -math.sin(radians) * MOVE_SPEED * direction
        Raumschiff.vy = -math.cos(radians) * MOVE_SPEED * direction
    else:
        Raumschiff.vx = 0
        Raumschiff.vy = 0
    
    Raumschiff.x += Raumschiff.vx
    Raumschiff.y += Raumschiff.vy

    Raumschiff.x = WIDTH if Raumschiff.x < 0 else 0 if Raumschiff.x > WIDTH else Raumschiff.x
    Raumschiff.y = HEIGHT if Raumschiff.y < 0 else 0 if Raumschiff.y > HEIGHT else Raumschiff.y

    # Asteroiden zufällig erzeugen
    if random.random() < 0.02:
        spawn_asteroid()

    # Asteroiden bewegen und rotieren
    for asteroid in ASTEROIDS[:]:
        asteroid.x += asteroid.vx
        asteroid.y += asteroid.vy
        asteroid.angle += asteroid.rotation_speed
        if not (-100 < asteroid.x < WIDTH + 100 and -100 < asteroid.y < HEIGHT + 100):
            ASTEROIDS.remove(asteroid)
    
    # Prüfe auf Kollision
    check_collision()

pgzrun.go()
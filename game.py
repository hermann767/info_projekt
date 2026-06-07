import pgzrun, pygame, random, math, time

WIDTH, HEIGHT, MOVE_SPEED = 1280, 720, 5
ROTATION_SPEED = 3
LASER_SPEED = 15
LASER_COOLDOWN = 1
ASTEROID_IMAGES = ["meteorbrown_big1","meteorbrown_med1","meteorbrown_small1","meteorgrey_med1"]
ASTEROIDS=[]
LASERS=[]
last_shot_time=0.0
game_over=False

Raumschiff=Actor("playership2_red",anchor=("center","center"))
Raumschiff.pos=(WIDTH//2,HEIGHT//2)
Raumschiff.vx=Raumschiff.vy=0
Raumschiff.angle=0

def spawn_asteroid():
    asteroid=Actor(random.choice(ASTEROID_IMAGES))
    side=random.choice(["top","bottom","left","right"])
    speed=random.uniform(2.0,4.5)
    angle=random.uniform(-1.0,1.0)
    if side=="top":
        asteroid.midbottom=(random.randint(0,WIDTH),-20); asteroid.vx,asteroid.vy=angle,speed
    elif side=="bottom":
        asteroid.midtop=(random.randint(0,WIDTH),HEIGHT+20); asteroid.vx,asteroid.vy=angle,-speed
    elif side=="left":
        asteroid.midright=(-20,random.randint(0,HEIGHT)); asteroid.vx,asteroid.vy=speed,angle
    else:
        asteroid.midleft=(WIDTH+20,random.randint(0,HEIGHT)); asteroid.vx,asteroid.vy=-speed,angle
    asteroid.angle=random.randint(0,360)
    asteroid.rotation_speed=random.uniform(-2.0,2.0)
    ASTEROIDS.append(asteroid)

def check_collision():
    global game_over
    if any(Raumschiff.colliderect(a) for a in ASTEROIDS):
        game_over=True


def reset_game():
    global game_over
    game_over=False
    ASTEROIDS.clear(); LASERS.clear()
    Raumschiff.pos=(WIDTH//2,HEIGHT//2); Raumschiff.vx=Raumschiff.vy=0; Raumschiff.angle=0


def fire_laser():
    radians=math.radians(Raumschiff.angle)
    LASERS.append({
        "x":Raumschiff.x-math.sin(radians)*40,
        "y":Raumschiff.y-math.cos(radians)*40,
        "vx":-math.sin(radians)*LASER_SPEED,
        "vy":-math.cos(radians)*LASER_SPEED,
    })


def on_mouse_down(pos, button):
    global last_shot_time
    if button==mouse.LEFT and not game_over:
        now=time.time()
        if now-last_shot_time>=LASER_COOLDOWN:
            last_shot_time=now; fire_laser()


def draw():
    screen.blit(pygame.transform.scale(images.load("hintergrund"),(WIDTH,HEIGHT)),(0,0))
    for asteroid in ASTEROIDS: asteroid.draw()
    for laser in LASERS:
        end_x=laser["x"]-laser["vx"]*5; end_y=laser["y"]-laser["vy"]*5
        for offset in (-2,0,2): screen.draw.line((laser["x"],laser["y"]+offset),(end_x,end_y+offset),"red")
        screen.draw.circle((laser["x"],laser["y"]),3,"yellow")
    if not game_over:
        Raumschiff.draw()
    else:
        screen.draw.text("GAME OVER!",(WIDTH//2-100,HEIGHT//2-50),fontsize=80,color="red")
        screen.draw.text("Drücke LEERTASTE zum Neustart",(WIDTH//2-77,HEIGHT//2+20),fontsize=30,color="white")


def update():

    if game_over:
        if keyboard.space: reset_game()
        return
    if keyboard.left: Raumschiff.angle+=ROTATION_SPEED
    if keyboard.right: Raumschiff.angle-=ROTATION_SPEED
    if keyboard.up or keyboard.down:
        radians=math.radians(Raumschiff.angle)
        direction=1 if keyboard.up else -1
        Raumschiff.vx=-math.sin(radians)*MOVE_SPEED*direction
        Raumschiff.vy=-math.cos(radians)*MOVE_SPEED*direction
    else: Raumschiff.vx=Raumschiff.vy=0
    Raumschiff.x=max(0,min(WIDTH,Raumschiff.x+Raumschiff.vx))
    Raumschiff.y=max(0,min(HEIGHT,Raumschiff.y+Raumschiff.vy))
    if random.random()<0.02: spawn_asteroid()

    for asteroid in ASTEROIDS[:]:
        asteroid.x += asteroid.vx; asteroid.y += asteroid.vy; asteroid.angle += asteroid.rotation_speed
        if not (-100 < asteroid.x < WIDTH + 100 and -100 < asteroid.y < HEIGHT + 100): ASTEROIDS.remove(asteroid)
    for laser in LASERS[:]:
        laser["x"] += laser["vx"]; laser["y"] += laser["vy"]
        if not (0 <= laser["x"] <= WIDTH and 0 <= laser["y"] <= HEIGHT): LASERS.remove(laser); continue
        for asteroid in ASTEROIDS[:]:
            if math.hypot(laser["x"]-asteroid.x,laser["y"]-asteroid.y)<30:
                ASTEROIDS.remove(asteroid)
                if laser in LASERS: LASERS.remove(laser)
                break
    check_collision()

pgzrun.go()
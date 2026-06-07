import pgzrun, pygame, random, math, time

WIDTH, HEIGHT, MOVE_SPEED = 1280, 720, 5
ROTATION_SPEED = 3
LASER_SPEED = 15
LASER_COOLDOWN = 1
SHOCKWAVE_RADIUS = 80
SHOCKWAVE_MAX_RADIUS = 350
SHOCKWAVE_FORCE = 1
SHOCKWAVE_DURATION = 20
SHOCKWAVE_COOLDOWN = 6
SHIP_HITBOX_RADIUS = 20
ASTEROID_IMAGES = ["meteorbrown_big1","meteorbrown_med1","meteorbrown_small1","meteorgrey_med1"]
ASTEROIDS, LASERS, SHOCKWAVES = [], [], []
last_shot_time = last_shockwave_time = 0.0
game_over = tutorial_shown = False
start_time = current_time = best_time = 0.0
wave_number = 1

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
    global game_over, best_time
    if any(math.hypot(a.x-Raumschiff.x,a.y-Raumschiff.y)<SHIP_HITBOX_RADIUS+a.width//2 for a in ASTEROIDS):
        game_over = True
        best_time = max(best_time, current_time)


def reset_game():
    global game_over, current_time, wave_number, start_time
    game_over=False; ASTEROIDS.clear(); LASERS.clear(); SHOCKWAVES.clear()
    Raumschiff.pos=(WIDTH//2,HEIGHT//2); Raumschiff.vx=Raumschiff.vy=0; Raumschiff.angle=0
    current_time=0.0; wave_number=1; start_time=time.time()


def fire_laser():
    radians=math.radians(Raumschiff.angle)
    LASERS.append({
        "x":Raumschiff.x-math.sin(radians)*40,
        "y":Raumschiff.y-math.cos(radians)*40,
        "vx":-math.sin(radians)*LASER_SPEED,
        "vy":-math.cos(radians)*LASER_SPEED,
    })


def create_shockwave():
    SHOCKWAVES.append({"life": SHOCKWAVE_DURATION})
    for asteroid in ASTEROIDS:
        dx, dy = asteroid.x - Raumschiff.x, asteroid.y - Raumschiff.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            asteroid.vx += SHOCKWAVE_FORCE; asteroid.vy += SHOCKWAVE_FORCE
        elif distance < SHOCKWAVE_RADIUS:
            push = (SHOCKWAVE_RADIUS-distance)/SHOCKWAVE_RADIUS*SHOCKWAVE_FORCE
            nx, ny = dx/distance, dy/distance
            asteroid.x += nx*push*12; asteroid.y += ny*push*12
            asteroid.vx += nx*SHOCKWAVE_FORCE; asteroid.vy += ny*SHOCKWAVE_FORCE


def on_mouse_down(pos, button):
    global last_shot_time, last_shockwave_time, tutorial_shown, start_time, current_time, wave_number
    if not tutorial_shown:
        tutorial_shown = True
        start_time = time.time()
        current_time = 0.0
        wave_number = 1
        return
    if not game_over and button==mouse.LEFT:
        now=time.time()
        if now-last_shot_time>=LASER_COOLDOWN: last_shot_time=now; fire_laser()
    elif not game_over and button==mouse.RIGHT:
        now=time.time()
        if now-last_shockwave_time>=SHOCKWAVE_COOLDOWN: last_shockwave_time=now; create_shockwave()


def draw():
    screen.blit(pygame.transform.scale(images.load("hintergrund"),(WIDTH,HEIGHT)),(0,0))
    
    if not tutorial_shown:
        overlay_rect = pygame.Rect(WIDTH//5, HEIGHT//5, WIDTH*3//5, HEIGHT*3//5)
        overlay_surface = pygame.Surface((overlay_rect.width, overlay_rect.height), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 200))
        screen.surface.blit(overlay_surface, overlay_rect.topleft)
        pygame.draw.rect(screen.surface,(255,255,255),overlay_rect,4)
        screen.draw.text("STEUERUNG", center=(WIDTH//2,HEIGHT//5+30), fontsize=48, color="white", owidth=2, ocolor="black")
        for i,text in enumerate(("Pfeiltasten: Raumschiff steuern","Linke Maustaste: Schießen","Rechte Maustaste: Schockwelle auslösen","Klick irgendwo, um zu starten")):
            screen.draw.text(text, center=(WIDTH//2, HEIGHT//5+110+i*45), fontsize=28, color="yellow", owidth=2, ocolor="black")
        return
    
    for asteroid in ASTEROIDS: asteroid.draw()
    for laser in LASERS:
        end_x, end_y = laser["x"]-laser["vx"]*5, laser["y"]-laser["vy"]*5
        [screen.draw.line((laser["x"],laser["y"]+offset),(end_x,end_y+offset),"red") for offset in (-2,0,2)]
        screen.draw.circle((laser["x"],laser["y"]),3,"yellow")
    screen.draw.text(f"Zeit: {int(current_time)}s", topleft=(10, 10), fontsize=28, color="white", owidth=1, ocolor="black")
    screen.draw.text(f"Highscore: {int(best_time)}s", topleft=(10, 40), fontsize=28, color="white", owidth=1, ocolor="black")
    screen.draw.text(f"Welle: {wave_number}", topright=(WIDTH-10, 10), fontsize=28, color="white", owidth=1, ocolor="black")
    
    ship_img = pygame.transform.scale(images.load("ship_b"),(25,25))
    for wave in SHOCKWAVES:
        current_radius = SHOCKWAVE_RADIUS + (SHOCKWAVE_MAX_RADIUS-SHOCKWAVE_RADIUS)*(1-wave["life"]/SHOCKWAVE_DURATION)
        alpha = int(255*wave["life"]/SHOCKWAVE_DURATION)
        for i in range(12):
            angle = 30*i; radians = math.radians(angle)
            ship = pygame.transform.rotate(ship_img,-angle)
            ship.set_alpha(alpha)
            screen.blit(ship,(Raumschiff.x+math.cos(radians)*current_radius-12,Raumschiff.y+math.sin(radians)*current_radius-12))
    
    Raumschiff.draw() if not game_over else (
        screen.draw.text("GAME OVER!",(WIDTH//2-100,HEIGHT//2-50),fontsize=80,color="red"),
        screen.draw.text("Drücke LEERTASTE zum Neustart",(WIDTH//2-77,HEIGHT//2+20),fontsize=30,color="white")
    )


def update():
    global current_time, wave_number
    if not tutorial_shown:
        return
    if game_over:
        if keyboard.space: reset_game()
        return
    current_time = time.time()-start_time
    new_wave_number=int(current_time//20)+1
    if new_wave_number!=wave_number:
        wave_number=new_wave_number; spawn_asteroid(); spawn_asteroid()
    spawn_chance = 0.01 + 0.004 * wave_number
    if current_time < 15:
        spawn_chance *= 0.35
    elif current_time < 30:
        spawn_chance *= 0.6
    elif current_time < 45:
        spawn_chance *= 0.8
    if random.random() < spawn_chance: spawn_asteroid()

    if keyboard.left: Raumschiff.angle += ROTATION_SPEED
    if keyboard.right: Raumschiff.angle -= ROTATION_SPEED
    if keyboard.up or keyboard.down:
        radians = math.radians(Raumschiff.angle)
        direction = 1 if keyboard.up else -1
        Raumschiff.vx = -math.sin(radians) * MOVE_SPEED * direction
        Raumschiff.vy = -math.cos(radians) * MOVE_SPEED * direction
    else: Raumschiff.vx = Raumschiff.vy = 0
    Raumschiff.x = max(0, min(WIDTH, Raumschiff.x + Raumschiff.vx))
    Raumschiff.y = max(0, min(HEIGHT, Raumschiff.y + Raumschiff.vy))

    for wave in SHOCKWAVES[:]:
        wave["life"] -= 1
        if wave["life"] <= 0: SHOCKWAVES.remove(wave)
        else:
            current_radius = SHOCKWAVE_RADIUS + (SHOCKWAVE_MAX_RADIUS - SHOCKWAVE_RADIUS) * (1 - wave["life"] / SHOCKWAVE_DURATION)
            for asteroid in ASTEROIDS:
                dx, dy = asteroid.x - Raumschiff.x, asteroid.y - Raumschiff.y
                distance = math.hypot(dx, dy)
                if distance == 0: asteroid.vx -= SHOCKWAVE_FORCE; asteroid.vy -= SHOCKWAVE_FORCE
                elif distance < current_radius:
                    push = (current_radius - distance) / current_radius * SHOCKWAVE_FORCE * 0.4
                    nx, ny = dx / distance, dy / distance
                    asteroid.vx += nx * push
                    asteroid.vy += ny * push
    
    for asteroid in ASTEROIDS[:]:
        asteroid.x += asteroid.vx; asteroid.y += asteroid.vy; asteroid.angle += asteroid.rotation_speed
        if not (-100 < asteroid.x < WIDTH + 100 and -100 < asteroid.y < HEIGHT + 100): ASTEROIDS.remove(asteroid)
    
    for laser in LASERS[:]:
        laser["x"] += laser["vx"]; laser["y"] += laser["vy"]
        if not (0 <= laser["x"] <= WIDTH and 0 <= laser["y"] <= HEIGHT): LASERS.remove(laser); continue
        for asteroid in ASTEROIDS[:]:
            if math.hypot(laser["x"]-asteroid.x, laser["y"]-asteroid.y) < 30:
                ASTEROIDS.remove(asteroid) if asteroid in ASTEROIDS else None
                LASERS.remove(laser) if laser in LASERS else None
                break
    check_collision()

pgzrun.go()
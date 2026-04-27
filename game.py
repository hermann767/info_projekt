import pgzrun

#globale Variablen
WIDTH = 1280
HEIGHT = 720

MOVE_SPEED_RAUMSCHIFF = 6
MOVE_SPEED_ASTEROIDEN = 3
MOVE_SPEED_SCHUSS = 10

#Raumschiff
raumschiff = Actor("raumschiff", anchor = ("center", "center"))
raumschiff.pos = (WIDTH / 2, HEIGHT / 2)




pgzrun.go()
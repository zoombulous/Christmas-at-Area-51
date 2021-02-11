import pygame, sys, time, math, random
from pygame.locals import *

pygame.init()
canvasWidth = 1280
canvasHeight = 700
win = pygame.display.set_mode((canvasWidth, canvasHeight))

pygame.display.set_caption("Christmas at Area 51")

#sound input
boom1 = pygame.mixer.Sound("assets/sfx/boom1.wav")
boom2 = pygame.mixer.Sound("assets/sfx/boom2.wav")
bunkerHitSound = pygame.mixer.Sound("assets/sfx/bunker_hit.wav")
collect = pygame.mixer.Sound("assets/sfx/collect.wav")
laserSound = pygame.mixer.Sound("assets/sfx/laser.wav")
gameOver = pygame.mixer.Sound("assets/sfx/game_over.wav")
#sound volume
pygame.mixer.Sound.set_volume(laserSound, 0.8)
pygame.mixer.Sound.set_volume(boom1, 2)
pygame.mixer.Sound.set_volume(boom2, .5)
pygame.mixer.Sound.set_volume(collect, 9)
pygame.mixer.Sound.set_volume(bunkerHitSound, 3)

starList = [pygame.image.load("assets/images/star_1.png"),
            pygame.image.load("assets/images/star_2.png"),
            pygame.image.load("assets/images/star_3.png"),
            pygame.image.load("assets/images/star_4.png")]

cloud1 = [pygame.image.load('assets/images/cloud1.png')]

arial = pygame.font.SysFont('arial.ttf', 40)

hpBag = [pygame.image.load("assets/images/hp_1_open_chute.png"),
         pygame.image.load("assets/images/hp_1_green.png"),
         pygame.image.load("assets/images/hp_1_white.png")]

sleigh1 = [
    [pygame.image.load("assets/images/sleigh_crash_no_fire.png"), pygame.image.load("assets/images/sleigh_crash_little_fire.png"),
     pygame.image.load("assets/images/sleigh_crash_more_fire.png"), pygame.image.load("assets/images/sleigh_crash_most_fire.png")],
    [pygame.image.load("assets/images/sleigh_1_1.png"), pygame.image.load("assets/images/sleigh_1_2.png")], 
    [pygame.image.load("assets/images/sleigh_2_1.png"), pygame.image.load("assets/images/sleigh_2_2.png")],
    [pygame.image.load("assets/images/sleigh_3_1.png"), pygame.image.load("assets/images/sleigh_3_2.png")],
    [pygame.image.load("assets/images/sleigh_4_1.png"), pygame.image.load("assets/images/sleigh_4_2.png")],
    [pygame.image.load("assets/images/sleigh_5_1.png"), pygame.image.load("assets/images/sleigh_5_2.png")]]
startIMG = [pygame.image.load("assets/images/start.png")]

bunker_hit = [pygame.image.load("assets/images/bunker_red.png"), pygame.image.load("assets/images/bunker_pink.png")]
bunker_1 = [[pygame.image.load("assets/images/bunker_0.png"),bunker_hit[0], bunker_hit[1],bunker_hit[0], bunker_hit[1]],
            
            [pygame.image.load("assets/images/bunker_1.png"),bunker_hit[0], bunker_hit[1],bunker_hit[0], bunker_hit[1]],
            
            [pygame.image.load("assets/images/bunker_2.png"),bunker_hit[0], bunker_hit[1],bunker_hit[0], bunker_hit[1]],
            
            [pygame.image.load("assets/images/bunker_3.png"),bunker_hit[0], bunker_hit[1],bunker_hit[0], bunker_hit[1]]
            ]
base_center = [pygame.image.load("assets/images/base_center.png"),
               pygame.image.load("assets/images/base_dead.png")]

presentEnd = [pygame.image.load("assets/images/present_1_death_4.png"),
              pygame.image.load("assets/images/present_1_death_5.png")]

present1 = [
    [pygame.image.load("assets/images/present_1_open_chute.png"),
     pygame.image.load("assets/images/present_1_death_1.png"),
     pygame.image.load("assets/images/present_1_death_2.png"),
     pygame.image.load("assets/images/present_1_death_3.png"),
     presentEnd[0],
     presentEnd[1]],
    [pygame.image.load("assets/images/big_present_open_chute.png"),
     pygame.image.load("assets/images/big_present_death_1.png"),
     pygame.image.load("assets/images/big_present_death_2.png"),
     pygame.image.load("assets/images/big_present_death_3.png"),
     presentEnd[0],
     presentEnd[1]],
    [pygame.image.load("assets/images/tall_present_open_chute.png"),
     pygame.image.load("assets/images/tall_present_death_1.png"),
     pygame.image.load("assets/images/tall_present_death_2.png"),
     pygame.image.load("assets/images/tall_present_death_3.png"),
     presentEnd[0],
     presentEnd[1]]]

background = [pygame.image.load("assets/images/background.png"),
              pygame.image.load("assets/images/background_evil.png")]

rapidFire = [pygame.image.load("assets/images/rapidFire.png")]

noFire = pygame.image.load("assets/images/no_fire.png")

fireState = False
fireSafety = False
fireTime = 0
gun = [pygame.image.load("assets/images/gun.png")]
gunX = math.floor(canvasWidth / 2)
gunY = canvasHeight - 175
gunAng = 0
gunRect = gun[0].get_rect(center = (gunX,gunY))
laserDistance = 2000
laserWidth = 4
wave = 0
baseAlive = 0


def vectCoors(a, d, x, y):
    x -= math.sin(a * math.pi / 180) * d
    y -= math.cos(a * math.pi / 180) * d
    return (x, y)

class starClass(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.anim = 0
        self.size = size
        self.nextBlink = tickStart + random.randint(2, 50)

class bunker(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = 3
        self.anim = 0
        self.blink = False

class enemy(object):
    def __init__(self, y, hp):
        self.y = y
        self.width = 40 * (hp + 1)
        self.height = 75
        self.vel = (random.randint(-2, 2) + 12 * (random.randint(0,1) - .5) * 2) + hp
        self.yvel = 0
        self.rate = 12000
        self.rand = 0
        self.lastDrop = 0
        self.hp = hp
        self.anim = 0
        self.x = 0-self.width

class projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 200
        self.direction = gunAng

class presentClass(object):
    def __init__(self, x, y, width, height, da, num, alive):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if num == 2:
            self. vel = 7 + (5 + random.randint(-3, 3))
        else:
            self. vel = 5 + random.randint(-3, 3)
        self.alive = alive
        self.anim = 0
        self.hpAnim = 0
        self.da = da
        self.num = num

class behind(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 70

class start(object):
    def __init__(self):
        self.x = canvasWidth / 2 - 150
        self.y = canvasHeight / 2 - 50
        self.width = 300
        self.height = 100

class cloud(object):
    def __init__(self):
        self.x = 200

def globalDraw():
    win.blit(background[0], (back.x, back.y))
    for star in stars:
        if len(presents) < 75:
            if star.nextBlink == ticks and star.anim < 2:
                star.anim += 1
            elif star.nextBlink == ticks - 1 and star.anim < 2:
                star.anim += random.randint(0,1)
                star.nextBlink += random.randint(70, 150)
            elif star.anim > 0:
                star.anim -= 1
        else:
            star.anim = 0
        win.blit(starList[star.anim + star.size], (star.x, star.y))
    if ticks % waveTotal >= (waveTotal-waveLen)-33 and ticks % waveTotal <= (waveTotal-waveLen)+33 and game and cloud_1.x > -200:
        cloud_1.x -= 3
    elif ((ticks % waveTotal < 33 or ticks % waveTotal > waveTotal-33) or not game) and cloud_1.x < 0:
        cloud_1.x += 3
    elif ticks % waveTotal >= (waveTotal-waveLen)+33 and ticks % waveTotal <= waveTotal-33 and game:
        cloud_1.x = -200
    else:
        cloud_1.x = 0
    win.blit(cloud1[0], (canvasWidth + cloud_1.x, 50))

    if fireState:
        pygame.draw.line(win, (random.randint(200,255),0,0), (gunX, gunY), (fireX, fireY), laserWidth)
    gunRotated = pygame.transform.rotate(gun[0], gunAng)
    win.blit(gunRotated, gunRotated.get_rect(center = (gunX, gunY)))
    
    fireRotated = pygame.transform.rotate(rapidFire[0], gunAng)
    
    #if fireState:
    #    win.blit(fireRotated, fireRotated.get_rect(center = (gunX, gunY)))

    for present in presents:
        win.blit(present1[present.num][present.anim],(present.x, present.y))
    for healPack in healPacks:
        win.blit(hpBag[healPack.anim], (healPack.x, healPack.y))
    for bunker in bunkers:
        if bunker.x < canvasWidth / 2:
            win.blit(pygame.transform.flip(bunker_1[bunker.hp][bunker.anim], True, False), (bunker.x, bunker.y))
        else:
            win.blit(bunker_1[bunker.hp][bunker.anim], (bunker.x, bunker.y))
    win.blit(base_center[baseAlive], (canvasWidth / 2 - 74, 475))
    for sleigh in sleighs:
        #if ticks % 4 == 0:
            #sleigh.anim += 1
        sleighImage = sleigh1[sleigh.hp][math.floor(sleigh.anim)]
        if sleigh.hp == 0:
            sleighImage = pygame.transform.rotate(sleighImage, sleigh.yvel * -1)
            if sleigh.anim < 3:
                sleigh.anim += .3
                
        if sleigh.vel < 0:
            win.blit(pygame.transform.flip(sleighImage, True, False), ((sleigh.x + sleigh.hp *40)  - 330, sleigh.y))
        else:
            win.blit(sleighImage, (sleigh.x, sleigh.y))
    #win.blit(present1[0], (firstPresent.x, firstPresent.y))

    if menu or afterGame:
        win.blit(startIMG[0], startIMG[0].get_rect(center = (canvasWidth / 2, canvasHeight / 2)))
    
    if game:
        scoring = arial.render('SCORE: ' + str(math.floor((ticks - tickStart)/6) + score), True, (255, 0, 0))
        win.blit(scoring, (gunX - 100, gunY + 125))
    pygame.display.update()

bunkers = [bunker(50, 560, 148, 80), bunker(300, 560, 148, 80), bunker(canvasWidth - 450, 560, 148, 80), bunker(canvasWidth - 200, 560, 148, 80)]
sleighs = []
#firstPresent = presentClass(50, 50, 64, 64)
presents = []
healPacks = []
back = behind(0, 0, 0, 0)
spawnStart = 50
spawn = spawnStart
tickStart = 10000
ticks = tickStart
menu = True
afterGame = False
sb = start()
game = True
endGameTicks = 0
score = 0
hpScore = 100
totalHP = 12
starDist = 32
stars = [starClass(random.randint(0, canvasWidth - 32), random.randint(0, math.floor(canvasHeight * 3/4)), random.randint (0,1))]
cloud_1 = cloud()

waveTotal = 800
waveLen = 300

for i in range (0, 25):
    placed = False
    while not placed:
        placed = True
        x = random.randint(0, canvasWidth - 32)
        y = random.randint(0, math.floor(canvasHeight * 3/4))
        for star in stars:
            if x + starDist > star.x and x < star.x + starDist and y + starDist > star.y and y < star.y + starDist:
                placed = False
    stars.append(starClass(x, y, random.randint(0,1)))
pygame.mixer.music.load("assets/sfx/menu_music_intro.wav")
pygame.mixer.music.play(1)
pygame.mixer.music.set_endevent(1)
while menu:
    for event in pygame.event.get():
        if event.type == 1:
            pygame.mixer.music.load("assets/sfx/menu_music_loop.wav")
            pygame.mixer.music.play(-1)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            fireState = True
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > sb.x and mouse_x < sb.x + sb.width and mouse_y > sb.y and mouse_y < sb.y + sb.height:
                menu = False
    fireX, fireY = vectCoors(gunAng, laserDistance, gunX, gunY)
    globalDraw()
pygame.mixer.music.load("assets/sfx/main_music_intro.wav")
pygame.mixer.music.play(1)
pygame.mixer.music.set_endevent(1)
while game:
    pygame.time.delay(40)
    ticks += 1
    fireSafety = False
    for event in pygame.event.get():
        if event.type == 1:
            pygame.mixer.music.load("assets/sfx/main_music_loop.wav")
            pygame.mixer.music.play(-1)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            pygame.mixer.Sound.play(laserSound)
            fireState = True
            fireSafety = True
            fireTime = ticks
            
        
        if fireTime < ticks:
            fireState = False
                
            
    keys = pygame.key.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - gunX, gunY - mouse_y
    gunAng = (180 / math.pi) * -math.atan2(rel_x, rel_y)
    
    if keys[pygame.K_SPACE] and ticks - fireTime > 2:
        fireState = True
        fireSafety = True
        fireTime = ticks

    if ticks % spawn == 0:
        if ticks < 7000:
            if wave == 1:
                sleighs.append(enemy(50 + 100 * random.randint(1,3), math.ceil((ticks - tickStart) / 1000) + random.randint(0,1)))
            sleighs.append(enemy(50 + 100 * random.randint(0,2), math.ceil((ticks - tickStart) / 1000) + random.randint(0,1)))
        else:
            sleighs.append(enemy(50 + 100 * random.randint(0,2), 5))
        if ticks % 7 == 0 and spawn > 1:
            spawn -= 1
        
    for sleigh in sleighs:       #sleigh physics
        sleigh.x += sleigh.vel
        sleigh.y += (math.sin(ticks / 5) * 2) + sleigh.yvel
        if sleigh.hp == 0:
            sleigh.x += sleigh.vel * sleigh.yvel / 20
            sleigh.yvel += 2.5
        if sleigh.x > canvasWidth and sleigh.hp > 0:
            sleigh.x = 0 - (sleigh.width)
        elif sleigh.x < 0 - sleigh.width and sleigh.hp > 0:
            sleigh.x = canvasWidth

        if ticks - sleigh.lastDrop > math.ceil(sleigh.rate / ticks) + sleigh.rand and sleigh.x > 0 and sleigh.x < canvasWidth - sleigh.width and sleigh.y < 560:
            if random.randint(0,math.ceil(5/ticks)) == 0 and wave == 1:
                num = 1
            else:
                if sleigh.y < 68:
                    regPres = 0
                    tallPres = 1
                    randomPres = random.randint(0,1)
                    if randomPres == 0:
                        num = 0
                    if randomPres == 1:
                        num = 2
                else:
                    num = 0
            if sleigh.hp == 0:
                temp = False
            else:
                temp = True
            if sleigh.vel > 0:
                presents.append(presentClass(sleigh.x, sleigh.y + sleigh.height - 25, 32, 32, False, num, temp))
            else:
                presents.append(presentClass(sleigh.x + sleigh.width - 32, sleigh.y + sleigh.height - 25, 32, 32, False, num, temp))
            if ticks % waveTotal > waveTotal - waveLen:
                sleigh.rand = random.randint(0, math.ceil(100000 / (ticks * 1.75)))
                wave = 1
            else:
                sleigh.rand = random.randint(0, math.ceil(100000 / ticks))
                wave = 0
            
            sleigh.lastDrop = ticks
        elif sleigh.x < 0 or sleigh.x > canvasWidth - sleigh.width:
            sleigh.lastDrop = ticks

    if len(sleighs) > 0:
        sleighlist = []
        for i in range(0, len(sleighs)):
            if sleighs[i].y > canvasHeight:
                sleighlist.append(i - len(sleighlist))
        for sleigh in sleighlist:
            sleighs.pop(sleigh)
            
    if math.floor((ticks - tickStart)/6) + score > hpScore:
        hpScore += 100
        healPacks.append(presentClass(random.randint(0,canvasWidth), -50, 32, 32, True, 0, True))
            
    if len(presents) > 0:
        presList = []
        for i in range(0, len(presents)):
            if not presents[i].alive:
                if presents[i].anim == 5 or (len(presents) > 50 and not totalHP == 0):
                    presList.append(i - len(presList))
                else:
                    presents[i].anim += 1
            for bunker in bunkers:
                if bunker.hp > 0 and presents[i].x + presents[i].width > bunker.x and presents[i].x < bunker.x + bunker.width and presents[i].y > bunker.y and presents[i].y < bunker.y + bunker.height and presents[i].alive:
                    bunker.hp -= 1
                    pygame.mixer.Sound.play(bunkerHitSound)
                    
                    bunker.blink = True
                    
                    if presents[i].num == 1 and bunker.hp > 0:
                        bunker.hp -= 1
                        bunker.blink = True
                        
                    presList.append(i - len(presList))
            presents[i].y += presents[i].vel
            if presents[i].y >= canvasHeight - 95:
                presList.append(i - len(presList))
        for gift in presList:
            if len(presList) > 0:
                presents.pop(gift)
    if len(healPacks) > 0:
        hpl = []
        for i in range(0, len(healPacks)):
            if not healPacks[i].alive:
                if healPacks[i].anim == 2:
                    hpl.append(i - len(hpl))
                    bunkerList = []
                    for bunker in bunkers:
                        if bunker.hp < 3:
                            bunkerList.append(bunker)
                    if len(bunkerList) > 0:
                        bunkerChosen = bunkerList[random.randint(0, len(bunkerList) - 1)]
                        bunkerChosen.hp += 1
                        pygame.mixer.Sound.play(collect)
                    else:
                        score += 10
                        pygame.mixer.Sound.play(collect)
                else:
                    healPacks[i].anim += 1
            healPacks[i].y += healPacks[i].vel
            if healPacks[i].y > canvasHeight - 95:
                hpl.append(i - len(hpl))
        for gift in hpl:
            healPacks.pop(gift)

    for bunker in bunkers:
        if bunker.blink:
            if bunker.anim < 4:
                bunker.anim += 1
                
            else:
                bunker.anim = 0
                bunker.blink = False
                
        
    if fireSafety:
        laserDistance = 2000
        if (len(presents) > 0 or len(sleighs) > 0) and fireState:
            for d in range(3, 100):
                x,y = vectCoors(gunAng, d * 10, gunX, gunY)
                for sleigh in sleighs:
                    if x < sleigh.x + sleigh.width and x > sleigh.x and y < sleigh.y + sleigh.height and y > sleigh.y and sleigh.hp > 0:
                        if d * 10 < laserDistance:
                            laserDistance = d*10
                            if sleigh.vel < 0:
                                sleigh.x += 40
                            sleigh.hp -=1
                            if sleigh.hp == 0:
                                pygame.mixer.Sound.play(boom2)
                            else:
                                pygame.mixer.Sound.play(boom1)
                            score += 2
                for present in presents:
                    if x < present.x + present.width and x > present.x and y < present.y + present.height and y > present.y and present.alive:
                        if d * 10 < laserDistance:
                            laserDistance = d*10
                            present.alive = False
                            pygame.mixer.Sound.play(boom1)
                            score += 1
                for healPack in healPacks:
                    if x < healPack.x + healPack.width + 20 and x > healPack.x - 20 and y < healPack.y + healPack.height + 20 and y > healPack.y - 20 and healPack.alive:
                        if d * 10 < laserDistance:
                            laserDistance = d*10
                            healPack.alive = False

    fireX, fireY = vectCoors(gunAng, laserDistance, gunX, gunY)
    totalHP = 0
    for bunker in bunkers:
        totalHP += bunker.hp
    if totalHP == 0 and endGameTicks == 0:
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(gameOver)
        baseAlive = 1
        cloud_1.x = -200
        for present in presents:
            present.alive = False
        endGameTicks = ticks + 10
    if not endGameTicks == 0:
        if ticks == endGameTicks:
            afterGame = True
            pygame.mixer.music.load("assets/sfx/menu_music_intro.wav")
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_endevent(1)
            for star in stars:
                star.nextBlink = tickStart + random.randint(2, 50)
            while afterGame:
                for event in pygame.event.get():
                    if event.type == 1:
                        pygame.mixer.music.load("assets/sfx/menu_music_loop.wav")
                        pygame.mixer.music.play(-1)
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        fireState = True
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if mouse_x > sb.x and mouse_x < sb.x + sb.width and mouse_y > sb.y and mouse_y < sb.y + sb.height:
                            afterGame = False
                            for bunker in bunkers:
                                bunker.hp = 3
                            ticks = tickStart
                            sleighs = []
                            presents = []
                            endGameTicks = 0
                            spawn = spawnStart
                            score = 0
                            baseAlive = 0
                            pygame.mixer.music.load("assets/sfx/main_music_intro.wav")
                            pygame.mixer.music.play(1)
                            pygame.mixer.music.set_endevent(1)
                fireX, fireY = vectCoors(gunAng, laserDistance, gunX, gunY)
                globalDraw()
    globalDraw()


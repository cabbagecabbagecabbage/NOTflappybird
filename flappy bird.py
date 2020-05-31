from pygame import *
from random import randint
init()
screen = display.set_mode((800,600))
score = 0
ingame = 0
clock = time.Clock()

myfont = font.SysFont("Century Gothic", 30)
ufo = image.load("ufo.png")
ufo = transform.scale(ufo, (50,50))
m = image.load("menu.png")
m = transform.scale(m, (800,600))

class bird:
    def __init__(self, coor, size, jumping, jumpvelo, jumpacc):
        self.coor = coor
        self.size = size
        self.birdrect = Rect(self.coor[0], self.coor[1], self.size, self.size)
        self.jumping = jumping
        self.initvelo = jumpvelo
        self.jumpvelo = jumpvelo
        self.jumpacc = jumpacc
        
    def getcoor(self):
        return self.coor
    
    def draw(self):
        draw.rect(screen, (255,0,0), self.birdrect)
        
    def fall(self):
        global gravity
        if (not self.jumping):
            if self.coor[1]+gravity < 600-self.size:
                self.coor[1] += gravity
                gravity += gravityacc
            else:
                self.coor[1] = 600-self.size
                gravity = 1
        self.birdrect = Rect(self.coor[0], self.coor[1], self.size, self.size)
        
    def resetvelo(self):
        self.jumpvelo = self.initvelo

    def jump(self):
        global jumpcount
        if self.coor[1] - self.jumpvelo > 0:
            jumpcount -= 1
            self.coor[1] -= self.jumpvelo
            self.jumpvelo -= self.jumpacc
            self.birdrect = Rect(self.coor[0], self.coor[1], self.size, self.size)
        else:
            self.jumping = 0


class obstacles:
    def __init__(self, left, hole):
        self.left = left
        self.hole = hole
        self.toprect = Rect(left, 0, 100, 100*hole)
        self.bottomrect = Rect(left, 100*(hole+2), 100, 600)
        self.velo = 5
        self.color = (randint(0,255),randint(0,255),randint(0,255))
    def move(self):
        self.left -= self.velo+score
        self.toprect = Rect(self.left, 0, 100, 100*self.hole)
        self.bottomrect = Rect(self.left, 100*(self.hole+2), 100, 600)

    def collide(self, rect):
        if self.toprect.colliderect(rect) or self.bottomrect.colliderect(rect):
            return True
        return False


player = bird([100,200],50,0,20,4)
gravity = 1
gravityacc = 1
jumpcount = 5
obstacleq = [obstacles(600, randint(0,4))]

def main():
    global player, ingame, running, score, jumpcount, gravity, gravityacc, obstacleq
    screen.fill((255,255,255))
    player.draw()
    screen.blit(ufo, player.coor)
    player.fall()
    keys = key.get_pressed()
    
    if keys[K_p]:
        ingame = 0
        
    if keys[K_r]:
        print("Your score was "+str(score))
        player = bird([100,200],50,0,20,4)
        obstacleq = [obstacles(600, randint(0,4))]
        gravity = 1
        score = 0
        
    if mouse.get_pressed()[0] or keys[K_SPACE]:
        gravity = 1
        player.jumping = 1
        player.resetvelo()
        jumpcount = 5
        
    if player.jumping:
        if jumpcount >=0:
            player.jump()
        else:
            player.jumping = 0


    if obstacleq[-1].left < 500 and len(obstacleq) < 3:
        obstacleq.append(obstacles(obstacleq[-1].left+300+score*15, randint(0,4)))
    
    delete = 0
    for o in obstacleq:
        o.move()
        if o.collide(player.birdrect):
            ingame = 0
            print("Your score was "+str(score))
            player = bird([100,200],50,0,20,4)
            obstacleq = [obstacles(600, randint(0,4))]
            gravity = 1
            score = 0
            
        if o.left+100 < 0:
            delete = 1
            
        draw.rect(screen, o.color, o.toprect)
        draw.rect(screen, o.color, o.bottomrect)

    if delete:
        del obstacleq[0]
        score += 1

    text = myfont.render("Score: "+str(score)+"     PRESS R TO RESTART     PRESS P TO PAUSE", False, (0,0,0))
    screen.blit(text, (30,30))


def menu():
    global ingame
    screen.fill((100,200,255))
    screen.blit(m, (0,0))
    title = myfont.render("NOT", False, (0,0,0))
    screen.blit(title, (200,50))
    text = myfont.render("PRESS SPACE TO START/RESUME", False, (0,0,0))
    screen.blit(text, (30,500))
    if key.get_pressed()[K_SPACE]:
        ingame = 1

        
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    
    if ingame == 0:
        menu()
    if ingame == 1:
        main()
    
    clock.tick(30)
    display.flip()

quit()

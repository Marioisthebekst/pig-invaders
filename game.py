import random, pygame, os

pygame.init()
width = 900
height = 500
WIN = pygame.display.set_mode((width, height))

BG = pygame.transform.scale(pygame.image.load(os.path.join("space2.png")), (width, height))
MAIN_BG = pygame.transform.scale(pygame.image.load(os.path.join("main background.jpg")), (width, height))
actor = pygame.transform.scale(pygame.image.load(os.path.join("spaceship_yellow.png")), (55, 40))
ACTOR = pygame.transform.rotate(actor, 180)
PIG = pygame.transform.scale(pygame.image.load(os.path.join("papapig.png")), (200, 185))
leser = pygame.transform.scale(pygame.image.load(os.path.join("bullet.jpg")), (10, 7))
LASER = pygame.transform.rotate(leser, 90)
MED_KIT = pygame.transform.scale(pygame.image.load(os.path.join("med kit.jpg")), (20, 17))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Player:
    COOLDOWN = 30

    def __init__(self, x, y, ):
        self.x = x
        self.y = y
        self.ACTOR = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ACTOR, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 24, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ACTOR.get_width()

    def get_height(self):
        return self.ACTOR.get_height()


class SpaceShip(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ACTOR = ACTOR
        self.mask = pygame.mask.from_surface(self.ACTOR)
        self.laser_img = LASER

    def move_lasers(self, vel, objs):
        score = 0
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        pygame.display.update()
                        if laser in self.lasers:
                            self.lasers.remove(laser)

class Enemy(Player):
    PIGS = {
        "pig1": PIG
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)

        self.ACTOR = self.PIGS[color]
        self.mask = pygame.mask.from_surface(self.ACTOR)

    def movement(self, vel):
        self.y += vel

class Consumables(Player):
    CONSUMABLES = {
        "med kit": MED_KIT
    }

    def __init__(self, x, y, Type):
        super().__init__(x, y)
        self.ACTOR = self.CONSUMABLES[Type]
        self.mask = pygame.mask.from_surface(self.ACTOR)

    def movement(self,vel):
        self.y += vel


def collide(object1, object2):
    distance_x = object2.x - object1.x
    distance_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (distance_x, distance_y)) is not None


def while_play():
    ACTOR_VEL = 3
    player = SpaceShip(x=430, y=400)
    LASER_VEL = 3
    health = 100
    PIG_VEL = 1
    enemies = []
    consumables_vel = 2
    consumables = []
    wave = 0

    run = True
    while run:

        clock = pygame.time.Clock()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if len(enemies) == 0:
            wave += 1
            consumable = Consumables(random.randrange(100,750),random.randrange(-10000,-3000),"med kit")
            consumables.append(consumable)
            for i in range(wave):
                enemy = Enemy(random.randrange(100, 750), random.randrange(-500,-100), "pig1")
                enemies.append(enemy)


        for enemy in enemies[:]:
            enemy.movement(PIG_VEL)
            if enemy.y + enemy.get_height() > 600:
                enemies.remove(enemy)
                health -= 5
            if collide(enemy, player):
                enemies.remove(enemy)
                health -= 10

        for consumable in consumables[:]:
            consumable.movement(consumables_vel)
            if collide(consumable,player):
                consumables.remove(consumable)
                health += 5
        if health == 0:
            dead = bigger_font.render("You Died!!!", 1, (255, 255, 255))
            WIN.blit(dead, (310, 230))
            pygame.display.update()
            pygame.time.delay(5000)
            main()
            health = 10
            wave = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and player.x - ACTOR_VEL > 0:
            player.x -= ACTOR_VEL
        if key[pygame.K_d] and player.x + ACTOR_VEL + player.get_width() < width:
            player.x += ACTOR_VEL
        if key[pygame.K_w] and player.y - ACTOR_VEL > 0:
            player.y -= ACTOR_VEL
        if key[pygame.K_s] and player.y + ACTOR_VEL + player.get_height() < height:
            player.y += ACTOR_VEL
        if key[pygame.K_SPACE]:
            player.shoot()
        player.move_lasers(-LASER_VEL, enemies)

        WIN.blit(BG, (0, 0))
        wave_label = font.render(f"Level: {wave}", 1, (255, 255, 255))
        WIN.blit(wave_label, (20, 15))
        Health = font.render(f"Health: {health}", 1, (255, 255, 255))
        WIN.blit(Health, (740, 15))
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for consumable in consumables:
            consumable.draw(WIN)
        pygame.display.update()

font = pygame.font.SysFont("comicsans", 40)
bigger_font = pygame.font.SysFont("comicsans", 80)

def main():
    run = True
    while run:
        WIN.blit(MAIN_BG, (0, 0))
        a = bigger_font.render("Press Space To Enter", 1, (255, 255, 255))
        WIN.blit(a, (180, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            while_play()

        pygame.display.update()

if __name__ == '__main__':
    main()

import pygame
import random


pygame.init()

clock = pygame.time.Clock()
FPS = 60
WIDTH, HEIGHT = 1500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Bunny")

start = True
run = False
game_over = False




player_walk_right = [pygame.image.load("images/player_animations/walk/right1.png"), pygame.image.load("images/player_animations/walk/right2.png"),
                     pygame.image.load("images/player_animations/walk/right3.png"), pygame.image.load("images/player_animations/walk/right4.png"),
                     pygame.image.load("images/player_animations/walk/right5.png"), pygame.image.load("images/player_animations/walk/right6.png")]
player_walk_left = [pygame.image.load("images/player_animations/walk/left1.png"), pygame.image.load("images/player_animations/walk/left2.png"),
                     pygame.image.load("images/player_animations/walk/left3.png"), pygame.image.load("images/player_animations/walk/left4.png"),
                     pygame.image.load("images/player_animations/walk/left5.png"), pygame.image.load("images/player_animations/walk/left6.png")]

player_idle_right = [pygame.image.load("images/player_animations/idle/right1.png"), pygame.image.load("images/player_animations/idle/right2.png"),
                     pygame.image.load("images/player_animations/idle/right3.png"), pygame.image.load("images/player_animations/idle/right4.png")]

player_attack_right = pygame.image.load("images/player_animations/attack/right2.png")
player_attack_left = pygame.image.load("images/player_animations/attack/left2.png")

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images//Ball.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - ground.height - self.rect.height
        self.side = random.randint(1, 2)
        if self.side == 1:
            self.rect.x = 0 - self.rect.width
        elif self.side == 2:
            self.rect.x = WIDTH
        self.speed = random.randint(4,7)



    def update(self):
        if self.side == 1:
            self.rect.x += self.speed
        elif self.side == 2:
            self.rect.x -= self.speed




    def draw(self):
        screen.blit(self.image, self.rect)



class BallManager:
    def __init__(self):
        self.balls = []
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= random.randint(70, 200):
            self.balls.append(Ball())
            self.timer = 0


        for ball in self.balls:
            ball.update()
            if ball.side == 1 and ball.rect.x > WIDTH:
                self.balls.remove(ball)
            if ball.side == 2 and ball.rect.x < 0:
                self.balls.remove(ball)

    def draw(self):
        for ball in self.balls:
            ball.draw()


class objects(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height

    def animation(self):
        screen.blit(self.image, (0, HEIGHT - self.height))



class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = 4
        self.left = False
        self.right = True
        self.walk = False
        self.idle = False
        self.attack= False
        self.jump = False
        self.fall = False
        self.walk_count = 0
        self.idle_count = 0
        self.hp_count = 3
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y == HEIGHT - ground.height - self.height:
            self.jump = True
        elif self.jump:
            if self.rect.y > HEIGHT - ground.height - self.height - 100:
                self.rect.y -= 6
            if self.rect.y > HEIGHT - ground.height - self.height - 130:
                self.rect.y -= 4
            if self.rect.y > HEIGHT - ground.height - self.height - 150:
                self.rect.y -= 3
            if self.rect.y > HEIGHT - ground.height - self.height - 165:
                self.rect.y -= 2
            if self.rect.y == HEIGHT - ground.height - self.height - 164:
                self.jump = False
                self.fall = True
        elif self.fall:
            if self.rect.y > HEIGHT - ground.height - self.height - 165:
                self.rect.y += 2
            if self.rect.y > HEIGHT - ground.height - self.height - 150:
                self.rect.y += 2
            if self.rect.y > HEIGHT - ground.height - self.height - 130:
                self.rect.y += 3
            if self.rect.y > HEIGHT - ground.height - self.height - 100:
                self.rect.y += 5
            if self.rect.y >= HEIGHT - ground.height - self.height:
                self.fall = False
                self.rect.y = HEIGHT - ground.height - self.height
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.walk = True
            self.left = True
            self.right = False
            self.idle = False
            self.attack = False
            self.idle_count = 0
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.walk = True
            self.left = False
            self.right = True
            self.idle = False
            self.attack = False
            self.idle_count = 0
        elif keys[pygame.K_SPACE]:
            self.attack = True
            self.walk = False
            self.idle = False
            self.walk_count = 0
        else:
            self.walk = False
            self.attack = False
            self.idle = True
            self.walk_count = 0

        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x + self.width >= WIDTH:
            self.rect.x = WIDTH - self.width
        if self.hp_count >= 3:
            self.hp_count = 3

    def animation(self):
        if self.idle_count + 1 >= FPS:
            self.idle_count = 0
        if self.walk_count + 1 >= FPS:
            self.walk_count = 0
        if self.walk == True and self.left == True:
            screen.blit(player_walk_left[self.walk_count // 10], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.walk == True and self.right == True:
            screen.blit(player_walk_right[self.walk_count // 10], (self.rect.x, self.rect.y))
            self.walk_count += 1
        if self.attack == True and self.left == True:
            screen.blit(player_attack_left, (self.rect.x - 21, self.rect.y))
        elif self.attack == True and self.right == True:
            screen.blit(player_attack_right,(self.rect.x, self.rect.y))
        if self.idle == True:
            screen.blit(player_idle_right[self.idle_count // 15], (self.rect.x, self.rect.y))
            self.idle_count += 1


class Hp(pygame.sprite.Sprite):
    def __init__(self):
        self.image1 = pygame.image.load('images/1Hp.png').convert_alpha()
        self.image2 = pygame.image.load('images/2Hp.png').convert_alpha()
        self.image3 = pygame.image.load('images/3Hp.png').convert_alpha()
        self.rect = self.image1.get_rect()
        self.rect.topright = WIDTH - 50, 50
    def update(self):
        pass
    def draw(self):
        if player.hp_count == 1:
            screen.blit(self.image1, self.rect)
        elif player.hp_count == 2:
            screen.blit(self.image2, self.rect)
        elif player.hp_count == 3:
            screen.blit(self.image3, self.rect)






class Heal(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images//heal.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - ground.height - self.rect.height - 10
        self.rect.x = x

    def update(self):
        pass

    def draw(self):
        screen.blit(self.image, self.rect)

class HealManager:
    def __init__(self):
        self.heals = []
    def add_heal(self, meteor):
        chance = random.randint(1, 100)
        if chance <= 25:
            heal = Heal(meteor.rect.x)
            self.heals.append(heal)


    def update(self):
        for heal in self.heals:
            heal.update()

    def draw(self):
        for heal in self.heals:
            heal.draw()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 25
        self.y = 25
        self.score_count = 0
        self.font = pygame.font.SysFont('arial', 52)

    def update(self):
        if self.score_count <= 0:
            self.score_count = 0
        self.text = self.font.render(str(self.score_count), True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)



def collisions(self):
    for ball in ball_manager.balls:
        if ball.side == 1 and ball.rect.x + ball.rect.width >= player.rect.x and player.attack and player.left and ball.rect.x + ball.rect.width <= player.rect.x + 20:
            heal_manager.add_heal(ball)
            score.score_count += 1
            ball_manager.balls.remove(ball)
        elif ball.side == 2 and ball.rect.x <= player.rect.x + player.rect.width and player.attack and player.right and ball.rect.x >= player.rect.x + player.rect.width - 20:
            heal_manager.add_heal(ball)
            score.score_count += 1
            ball_manager.balls.remove(ball)
        elif ball.rect.colliderect(player.rect):
            player.hp_count -= 1
            score.score_count -= 3
            ball_manager.balls.remove(ball)
    for heal in heal_manager.heals:
        if player.rect.colliderect(heal.rect):
            player.hp_count += 1
            score.score_count += 1
            heal_manager.heals.remove(heal)




ground = objects('images/ground.png', 0, 0)
player = Player('images/player_animations/idle/right1.png', WIDTH // 2, HEIGHT - 87 - ground.height)
ball_manager = BallManager()
hp = Hp()
score = Score()
heal_manager = HealManager()








while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    background_image = pygame.transform.scale(pygame.image.load("images/start.png"), (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        start = False
        run = True



    pygame.display.update()
    clock.tick(FPS)



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if player.hp_count == 0:
        run = False
        game_over = True


    background_image = pygame.transform.scale(pygame.image.load("images/background.webp"), (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    ground.update()
    player.update()
    ball_manager.update()
    ground.animation()
    player.animation()
    ball_manager.draw()
    hp.draw()
    collisions(player)
    heal_manager.update()
    heal_manager.draw()
    score.update()
    score.draw(screen)


    pygame.display.update()
    clock.tick(FPS)


while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    background_image = pygame.transform.scale(pygame.image.load("images/game_over.png"), (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_over = False


    pygame.display.update()
    clock.tick(FPS)
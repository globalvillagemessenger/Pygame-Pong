import pygame
import sys
import random

#Initialize pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

#create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#title and icon
pygame.display.set_caption("Pong")
icon = pygame.image.load("atari.png")
pygame.display.set_icon(icon)


#sound effect
beep = pygame.mixer.Sound('beep.wav')


# colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#draw text function
font_name = pygame.font.match_font('courier')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#sprite classes
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 70))
        self.image.fill((WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = HEIGHT/2
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedy = 0
        if keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_s]:
            self.speedy = 4

        #player speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #player y-axis boundary
        if self.rect.top > HEIGHT - 70:
            self.rect.top = HEIGHT - 70
        if self.rect.bottom < 0 + 70:
            self.rect.bottom = 0 + 70


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 70))
        self.image.fill((WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 40
        self.rect.y = HEIGHT/2
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedy = 0
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4

        #player speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #player y-axis boundary
        if self.rect.top > HEIGHT - 70:
            self.rect.top = HEIGHT - 70
        if self.rect.bottom < 0 + 70:
            self.rect.bottom = 0 + 70        

# lists of ball speeds from which to randomly select from 
ballspeeds1 = [-4, 4]
ballspeeds2 = [-4, 0, 4]
            
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = 0
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        #ball speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #ball movement
        if self.rect.y <= 0:
            self.speedy = 4
            self.speedx = random.choice(ballspeeds1)
        elif self.rect.y >= HEIGHT - 20:
            self.speedy = -4
            self.speedx = random.choice(ballspeeds1)
        
        #score
        if self.rect.x <= 20:
            self.rect.x = WIDTH/2
            self.rect.y = 0
            global player2_score
            player2_score +=1
            #print("Player 2 score: ", player2_score)
            
        if self.rect.x >= WIDTH - 20:
            self.rect.x = WIDTH/2
            self.rect.y = 0
            global player1_score
            player1_score += 1
            #print("Player 1 score: ", player1_score)
            

# create variable for player score, set initial score to zero
player1_score = 0
player2_score = 0     


# create sprites
all_sprites = pygame.sprite.Group()

player1 = Player1()
all_sprites.add(player1)

player2 = Player2()
all_sprites.add(player2)

ball = pygame.sprite.Group()
for i in range(1):
    b = Ball()
    all_sprites.add(b)
    ball.add(b)



# game loop
game_over = False
running = True
while running:
    
    # update screen
    all_sprites.update()
    
    
    
    # checks to see if ball hits player1
    hits1 = pygame.sprite.spritecollide(player1, ball, False)
    if hits1:
        b.speedx = 4
        b.speedy = random.choice(ballspeeds2)
        beep.play()

    # checks to see if ball hits player2
    hits2 = pygame.sprite.spritecollide(player2, ball, False)
    if hits2:
        b.speedx = -4
        b.speedy = random.choice(ballspeeds2)
        beep.play()

    
    # draw screen, sprites, and player scores
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(player1_score), 18, WIDTH / 4, 10)
    draw_text(screen, str(player2_score), 18, 3 * WIDTH / 4, 10)

    
    pygame.display.flip()

    # quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
 
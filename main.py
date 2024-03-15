import pygame
import time
import random
import sys
from game_data import *

#INITIALIZING MODULES
pygame.font.init()
pygame.mixer.init()

#CREATING SPECIAL OBJECTS 
DISPLAY = pygame.display
SCREEN = DISPLAY.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('COMMIE BUSTERS')
BG_MUSIC = pygame.mixer.music
CLOCK = pygame.time.Clock()

#LOADING MEDIA AND DATA
BG = pygame.transform.scale(pygame.image.load('bg.png'), (WIDTH, HEIGHT)).convert_alpha()
FLAG = pygame.transform.scale(pygame.image.load('flag.png'), (WIDTH, HEIGHT - PATRIOT_HEIGHT * 2)).convert_alpha()
FLAG.set_alpha(32)
BOX_IMAGE = pygame.image.load('a.png').convert_alpha()
COMMIE_IMG = pygame.transform.scale_by(pygame.image.load('commie.png'), 0.03).convert_alpha()
BG_MUSIC.load('patriotic.flac')

SIGNS = pygame.font.SysFont('BELL MT', 30)

PATRIOT = pygame.transform.scale(BOX_IMAGE, (PATRIOT_WIDTH, PATRIOT_HEIGHT))

def writeText(text, size=30, color='white', AA=True):
    return pygame.font.SysFont('BELL MT', size).render(text, AA, color)

def draw(patriot, elapsed, commies, border, commies_captured):
    SCREEN.blit(BG, (0,0))
    SCREEN.blit(FLAG, (0,0))
    
    border_text = SIGNS.render('DO NOT CROSS THE BERLIN WALL', 1, 'black')
    pygame.draw.rect(SCREEN, (160, 0, 0), border)
    SCREEN.blit(writeText(f'Time is: {round(elapsed)} \n {commies_captured} commies Captured'), (300, 10))
    SCREEN.blit(border_text, (WIDTH//2 - border_text.get_width()//2 - 10, HEIGHT - PATRIOT_HEIGHT * 1.9))
    SCREEN.blit(PATRIOT, patriot)
    for commie in commies:
        SCREEN.blit(COMMIE_IMG, commie)
    pygame.display.update()

def checkExit(events):
    for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()                  

def main():
    BG_MUSIC.play(loops=1, start=0)
    commies_captured = 0
    run=True
    game_active = True
    start_time = time.time()
    add_increment = 2000
    commies = []
    period = 0
    commies_captured = 0
    elapsed = 0
    
    patriot = PATRIOT.get_rect(x = 200 - PATRIOT.get_width()//2, y = HEIGHT - PATRIOT.get_height())
    border = pygame.Rect(0, HEIGHT - PATRIOT.get_height() * 2, WIDTH, PATRIOT.get_height() //2)
    while run:
        events = pygame.event.get()
        checkExit(events)
        #TIMER
        if elapsed > 19:
            game_active = False
        #RUN GAME
        if game_active:
            period += CLOCK.tick(FPS)
            elapsed = time.time() - start_time
            if period > add_increment:
                for _ in range(4):
                    commie_x = random.randint(0, WIDTH - COMMIE_WIDTH)
                    commie = COMMIE_IMG.get_rect()
                    commie.x = commie_x
                    commies.append(commie)
                add_increment = max(200, add_increment - 50)
                period = 0

            #MOVEMENT DETECTION
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and patriot.x - PATRIOT_VEL >= 0:
                patriot.x -= PATRIOT_VEL/2
            if keys[pygame.K_RIGHT] and patriot.x + PATRIOT_VEL + PATRIOT.get_width() <= WIDTH:
                patriot.x += PATRIOT_VEL/2
            if keys[pygame.K_UP] and patriot.y - PATRIOT_VEL >= border.y + border.height:
                patriot.y -= PATRIOT_VEL
            if keys[pygame.K_DOWN] and patriot.y + PATRIOT_VEL + PATRIOT.get_height() <= HEIGHT:
                patriot.y += PATRIOT_VEL
            
            #COMMIE GENERATION AND CAPTURE MECHANISM
            for commie in commies[:]:
                commie.y += COMMIE_VEL
                if commie.y > HEIGHT:
                    commies.remove(commie)
                elif (commie.y >= patriot.y) and (patriot.colliderect(commie)):
                    commies.remove(commie)
                    commies_captured += 1
                    pygame.display.update()
            draw(patriot, elapsed, commies, border, commies_captured)

        #GAME OVER SCREEN
        else:
            SCREEN.fill('black')
            game_over_txt = writeText('GAME OVER', size=100)
            score_txt = writeText(f'YOU CAPTURED {commies_captured} COMMIE-TROOPERS IN {int(elapsed)} Seconds')
            SCREEN.blit(game_over_txt, (WIDTH//2 - game_over_txt.get_width()//2, 100))
            SCREEN.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, game_over_txt.get_height() + 150))
            pygame.display.update()
            #RESTARTS GAME IF ENTER IS PRESSED
            for event in events:
                 if event.type == pygame.KEYDOWN:
                      if event.key == pygame.K_RETURN:
                           game_active = True
                           commies.clear()
                           commies_captured, elapsed, period, start_time = 0, 0, 0, time.time()
    
    pygame.quit()


if __name__ == "__main__":
    main()
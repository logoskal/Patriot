import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 640
PATRIOT_WIDTH, PATRIOT_HEIGHT = 75, 50
PATRIOT_VEL = 12
COMMIE_WIDTH = 10
COMMIE_HEIGHT = 10
COMMIE_VEL = 6
commies_captured = 0
global commie_count
commie_count = 0

FONT = pygame.font.SysFont('commicsans', 30)
SIGNS = pygame.font.SysFont('bell mt', 30)


BG = pygame.image.load('bg.png')
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
commie_img = pygame.transform.scale_by(pygame.image.load('commie.png'), 0.03).convert_alpha()
BOX_IMAGE = pygame.image.load('a.png')
pygame.display.set_caption('COMMIE BUSTERS')
BG_MUSIC = pygame.mixer.music

PATRIOT = pygame.transform.scale(BOX_IMAGE, (PATRIOT_WIDTH, PATRIOT_HEIGHT))

end_game = FONT.render(f'You Have Captured {commie_count} Commies in 30 Seconds', True, (64, 64, 64))

def draw(patriot, elapsed, commies, border, commie_count):
    WIN.blit(BG, (0,0))
    t_text = FONT.render(f'Time is: {round(elapsed)} \n {commie_count} commies Captured', 1, 'white')
    
    border_text = SIGNS.render('DO NOT CROSS THE BERLIN WALL', 1, 'black')
    pygame.draw.rect(WIN, (160, 0, 0), border)
    WIN.blit(t_text, (300, 10))
    WIN.blit(border_text, (WIDTH//2 - border_text.get_width()//2 - 10, HEIGHT - PATRIOT_HEIGHT * 1.9))
    WIN.blit(PATRIOT, patriot)

    

    for commie in commies:
        WIN.blit(commie_img, commie)

    pygame.display.update()

clock = pygame.time.Clock()
def main():
    BG_MUSIC.load('patriotic.flac')
    BG_MUSIC.play(loops=1, start=0)

    run = True
    hit = False
    commiet_time = time.time()
    commie_add_increment = 2000
    commie_count = 0
    commies = []
    commies_captured = 0
    freeze = False
    
    patriot = pygame.Rect(200 - PATRIOT_WIDTH//2, HEIGHT - PATRIOT_HEIGHT, PATRIOT_WIDTH, PATRIOT_HEIGHT)
    border = pygame.Rect(0, HEIGHT - PATRIOT_HEIGHT * 2, WIDTH, PATRIOT_HEIGHT //2)
    while run:
        commie_count += clock.tick(60)
        elapsed = time.time() - commiet_time
        if elapsed > 35:
            WIN.fill('black')
            WIN.blit(end_game, (300, 100))
            pygame.display.update()
            time.sleep(3)
            break
        if commie_count > commie_add_increment:
            for _ in range(4):
                commie_x = random.randint(0, WIDTH - COMMIE_WIDTH)
                commie = commie_img.get_rect()
                commie.x = commie_x
                #pygame.Rect(commie_x, -COMMIE_HEIGHT, COMMIE_WIDTH, COMMIE_HEIGHT)
                commies.append(commie)
            commie_add_increment = max(200, commie_add_increment - 50)
            commie_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if freeze == True:
            freeze = False
        if keys[pygame.K_LEFT] and patriot.x - PATRIOT_VEL >= 0:
            patriot.x -= PATRIOT_VEL/2
        if keys[pygame.K_RIGHT] and patriot.x + PATRIOT_VEL + PATRIOT_WIDTH <= WIDTH:
            patriot.x += PATRIOT_VEL/2
        if keys[pygame.K_UP] and patriot.y - PATRIOT_VEL >= border.y + border.height:
            patriot.y -= PATRIOT_VEL
        if keys[pygame.K_DOWN] and patriot.y + PATRIOT_VEL + PATRIOT_HEIGHT <= HEIGHT:
            patriot.y += PATRIOT_VEL

        for commie in commies[:]:
            commie.y += COMMIE_VEL
            if commie.y > HEIGHT:
                commies.remove(commie)
            elif (commie.y >= patriot.y) and (patriot.colliderect(commie)):
                commies.remove(commie)
                commies_captured += 1
                support_text = FONT.render(f'{commies_captured}Commies Captured', 1, 'white')
                WIN.blit(support_text, (WIDTH//2 - support_text.get_width()//2, HEIGHT/2 - support_text.get_height()//2))
                pygame.display.update()
                #pygame.time.delay(500)
                freeze = True
                #break
        draw(patriot, elapsed, commies, border, commies_captured)
        if elapsed > 5:
            commie_add_increment = 1000
    
    pygame.quit()


if __name__ == "__main__":
    main()
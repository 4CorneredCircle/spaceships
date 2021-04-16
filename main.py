import pygame
import os
import random

from pygame.constants import MOUSEBUTTONDOWN
pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('ariel', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

FPS = 60
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

METEOR_HAZARD_EVENT = pygame.USEREVENT + 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

MAIN_MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))

METEOR_WIDTH, METEOR_HEIGHT = 64, 64
METEOR_VEL = 3

METEOR_IMAGE = pygame.image.load(os.path.join('Assets', 'flaming_meteor.png'))
METEOR = pygame.transform.scale(METEOR_IMAGE, (METEOR_WIDTH, METEOR_HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_ship_type, yellow_ship_type, meteor_list):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for meteor in meteor_list:
        WIN.blit(METEOR, (meteor.x, meteor.y))

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    y_slow_indicator = pygame.Rect(yellow.x + yellow.width//2 - 15, yellow.y + yellow.height + 20, 10, 10)
    r_slow_indicator = pygame.Rect(red.x + red.width//2 - 8, red.y + red.height + 20, 10, 10)

    if red_ship_type == 2:
        pygame.draw.rect(WIN, RED, r_slow_indicator)

    if yellow_ship_type == 2:
        pygame.draw.rect(WIN, YELLOW, y_slow_indicator)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow, yellow_vel):
    if keys_pressed[pygame.K_a] and yellow.x - yellow_vel > 0: # LEFT
            yellow.x -= yellow_vel
    if keys_pressed[pygame.K_d] and yellow.x + yellow_vel + yellow.width < BORDER.x: # RIGHT
            yellow.x += yellow_vel
    if keys_pressed[pygame.K_w] and yellow.y - yellow_vel > 0: # UP
            yellow.y -= yellow_vel
    if keys_pressed[pygame.K_s] and yellow.y + yellow_vel + yellow.height < HEIGHT - 10: # DOWN
            yellow.y += yellow_vel

def red_handle_movement(keys_pressed, red, red_vel):
    if keys_pressed[pygame.K_LEFT] and red.x - red_vel > BORDER.x + BORDER.width: # LEFT
            red.x -= red_vel
    if keys_pressed[pygame.K_RIGHT] and red.x + red_vel + red.width < WIDTH: # RIGHT
            red.x += red_vel
    if keys_pressed[pygame.K_UP] and red.y - red_vel > 0: # UP
            red.y -= red_vel
    if keys_pressed[pygame.K_DOWN] and red.y + red_vel + red.height < HEIGHT - 10: # DOWN
            red.y += red_vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def handle_meteors(meteor_list, yellow, red):
    for meteor in meteor_list:
        meteor.y += METEOR_VEL
        if red.colliderect(meteor):
            pygame.event.post(pygame.event.Event(RED_HIT))
            meteor_list.remove(meteor)
        if yellow.colliderect(meteor):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            meteor_list.remove(meteor)
        elif meteor.y > HEIGHT:
            meteor_list.remove(meteor)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    main_menu()

def hazard_function():
    pygame.time.set_timer(METEOR_HAZARD_EVENT, 15000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_ship_type = 1
    yellow_ship_type = 1

    red_vel = 5
    yellow_vel = 5

    red_max_bullets = 3
    yellow_max_bullets = 3

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    meteor_list = []

    counter = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # firing bullets
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < yellow_max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < red_max_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                #handles switching ship types
                if event.key == pygame.K_LSHIFT and yellow_ship_type == 1:
                    yellow_vel = 3
                    yellow_max_bullets = 6
                    yellow_ship_type = 2

                elif event.key == pygame.K_LSHIFT and yellow_ship_type ==2:
                    yellow_vel = 5
                    yellow_max_bullets = 3
                    yellow_ship_type = 1

                if event.key == pygame.K_RSHIFT and red_ship_type == 1:
                    red_vel = 3
                    red_max_bullets = 6
                    red_ship_type = 2

                elif event.key == pygame.K_RSHIFT and red_ship_type == 2:
                    red_vel = 5
                    red_max_bullets = 3
                    red_ship_type = 1

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == METEOR_HAZARD_EVENT:
                while counter < random.randint(2, 4):
                    meteor_rect = pygame.Rect(random.randrange(1, WIDTH - METEOR_WIDTH, 10), 0, METEOR_WIDTH, METEOR_HEIGHT)
                    meteor_list.append(meteor_rect)
                    counter += 1
                counter = 0

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, yellow_vel)
        red_handle_movement(keys_pressed, red, red_vel)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        handle_meteors(meteor_list, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_ship_type, yellow_ship_type, meteor_list)
    
    main()

def main_menu():
    hazards = False

    click = False

    menu_open = True
    while menu_open:
        WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))

        title_background = pygame.Rect(295, 25, 310, 100)
        pygame.draw.rect(WIN, BLACK, title_background)

        title_text = HEALTH_FONT.render("SPACESHIPS", 1, WHITE)
        subheading_text = HEALTH_FONT.render("Choose your options:", 1, WHITE)
        WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2 - 200))
        WIN.blit(subheading_text, (WIDTH//2 - subheading_text.get_width()//2, HEIGHT//2 - subheading_text.get_height()//2 - 150))

        mx, my = pygame.mouse.get_pos()

        hazard_button = pygame.Rect(350, 200, 200, 50)
        no_hazard_button = pygame.Rect(350, 300, 200, 50)
        start_button = pygame.Rect(350, 400, 200, 50)
        #check to see if the mouse has collided with the button and if the mouse is also being clicked
        if hazard_button.collidepoint((mx, my)):
            if click:
                hazards = True
        if no_hazard_button.collidepoint((mx, my)):
            if click:
                hazards = False
        if start_button.collidepoint((mx, my)):
            if click:
                if hazards == True:
                    hazard_function()
                    main()
                elif hazards == False:
                    main()
        pygame.draw.rect(WIN, BLACK, hazard_button)
        pygame.draw.rect(WIN, BLACK, no_hazard_button)
        pygame.draw.rect(WIN, BLACK, start_button)

        hazard_text = HEALTH_FONT.render("Hazards on", 1, WHITE)
        no_hazard_text = HEALTH_FONT.render("Hazards off", 1, WHITE)
        start_text = HEALTH_FONT.render("Start", 1, WHITE)
        WIN.blit(hazard_text, (hazard_button.x + 20, hazard_button.y + 10))
        WIN.blit(no_hazard_text, (no_hazard_button.x + 20, no_hazard_button.y + 10))
        WIN.blit(start_text, (start_button.x + 65, start_button.y + 10))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()

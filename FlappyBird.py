# Referfence : https://www.pygame.org/docs/

import pygame
import sys
import random

# __________________________FUNCTIONS_____________________


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos-100))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    pipe_visibility = [pipe for pipe in pipes if pipe.right >= 15]
    return pipe_visibility


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Reference (check_collision) : https://www.youtube.com/watch?v=1_H7InPMjaY&t=316s
def check_collision(pipes):
    global is_score_possible
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            is_score_possible = True
            return False


    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        is_score_possible = True
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(60, bird_rect.centery))
    return new_bird, new_bird_rect


def display_score(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            str(int(score)), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score :{int(score)}', False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score :{int(high_score)}', False, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 410))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def score_check():
    global score,is_score_possible
    
    if pipe_list:
        for pipe in pipe_list:
            if 55 < pipe.centerx < 65 and is_score_possible:
                score += 1
                score_sound.play()
                is_score_possible = False
            if pipe.centerx < 0:
                is_score_possible = True


pygame.init()
pygame.display.set_caption('Flappy Birds')
icon = pygame.image.load('imgs/bird-house.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/GameFont.ttf', 30)
  
# ___________________________GAME VARIABLES____________________________

gravity = 0.40
bird_movement = 0
game_active = True
score = 0
high_score = 0
is_score_possible = True

# BACKGROUND SURFACE
back_surface = pygame.image.load('imgs/background.png').convert()

# FLOOR
floor_surface = pygame.image.load('imgs/base.png').convert()
floor_x_pos = 0

# BIRD
bird_down = pygame.image.load('imgs/bird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('imgs/bird-midflap.png').convert_alpha()
bird_up = pygame.image.load('imgs/bird-upflap.png').convert_alpha()

bird_frames = [bird_down, bird_mid, bird_up]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(60, 220))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# PIPE
pipe_surface = pygame.image.load('imgs/pipe.png')
pipe_list = []
MAKEPIPE = pygame.USEREVENT
pygame.time.set_timer(MAKEPIPE, 1200)
pipe_height = [200, 250, 280, 330]

game_over_surface = pygame.image.load('imgs/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 240))

# SOUNDS
# Reference : https://www.sounds-resource.com/mobile/flappybird/sound/5309/

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# EVENT LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (60, 220)
                bird_movement = 0
                score = 0

        if event.type == MAKEPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(back_surface, (0, 0))

    if game_active:
        
        # Bird Animations
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe Animations
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)

        #Score Updates
        score_check()
        display_score('main_game')
        
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        display_score('game_over')

    # Floor Animations
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)

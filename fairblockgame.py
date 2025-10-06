import pygame, random

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 650))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pip_list):
    for pipe in pip_list:
        if pipe.bottom >= 600:  
            screen.blit(pipe_surface, pipe)
        else:  
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  
            screen.blit(flip_pipe, pipe)

def check_collision(pip_list):
    for pipe in pip_list:
        if mushroom_rect.colliderect(pipe):
            return False
    if mushroom_rect.top <= -75 or mushroom_rect.bottom >= 650:  
        return False
    return True

def rotate_mushroom(mushroom):
    new_mushroom = pygame.transform.rotozoom(mushroom, -mushroom_movement * 3, 1)     
    return new_mushroom

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = pygame.font.Font(None, 36).render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = pygame.font.Font(None, 36).render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = pygame.font.Font(None, 36).render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 500))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
gravity = 0.25
mushroom_movement = 0
game_active = True
score = 0
high_score = 0

bg = pygame.image.load("assets/background.jpg")
bg = pygame.transform.scale(bg, (216, 384))
bg = pygame.transform.scale2x(bg)
floor = pygame.image.load("assets/floor.png")
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

mushroom = pygame.image.load("assets/mushroom.png")
mushroom = pygame.transform.scale(mushroom, (34, 24))
mushroom = pygame.transform.scale2x(mushroom)
mushroom_rect = mushroom.get_rect(center=(100, 384))

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pip_list = []
pipe_height = [200, 300, 350]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                mushroom_movement = 0
                mushroom_movement -= 11
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pip_list.clear()
                mushroom_rect.center = (100, 384)
                mushroom_movement = 0
                score = 0
        if event.type == spawnpipe:
            pip_list.extend(create_pipe())
            
            
    screen.blit(bg, (0, 0))
    if game_active:
        mushroom_movement += gravity
        rotated_mushroom = rotate_mushroom(mushroom)
        mushroom_rect.centery += int(mushroom_movement)
        screen.blit(rotated_mushroom, mushroom_rect)
        game_active = check_collision(pip_list)
        
        pip_list = move_pipes(pip_list)
        draw_pipe(pip_list)
        score += 0.01
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

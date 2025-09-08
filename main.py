''' ---------- GAME SETTINGS ---------- '''

import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()
import asyncio

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Game window
win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

# Fonts
font = pg.font.Font(None, 30)
large_font = pg.font.Font(None, 72)

# Game variables
speed = 7
score = 0
health = 5
running = True 
game_over = False
player_size = 55
player_pos = [win_width / 2, win_height - player_size * 2]
obj_size = 60
obj_data = []
spawn_timer = 0
spawn_delay = 300 # milliseconds

# Try to load images with error handling
try:
    player_image = pg.image.load('./assets/images/Goomba-PNG-File.png')
    player_image = pg.transform.scale(player_image, (player_size, player_size))
except:
    # Create a placeholder if image fails to load
    player_image = pg.Surface((player_size, player_size))
    player_image.fill((0, 255, 0))  # Green square

try:
    obj = pg.image.load('./assets/images/mario.png')
    obj = pg.transform.scale(obj, (obj_size, obj_size))
except:
    obj = pg.Surface((obj_size, obj_size))
    obj.fill((255, 0, 0))  # Red square

try:
    bg_image = pg.image.load('./assets/images/background.png')
    bg_image = pg.transform.scale(bg_image, (win_width, win_height))
except:
    bg_image = pg.Surface((win_width, win_height))
    bg_image.fill((0, 0, 50))  # Dark blue background

def create_object(obj_data):
    current_time = pg.time.get_ticks()
    global spawn_timer
    
    if current_time - spawn_timer > spawn_delay and len(obj_data) < 10:
        x = random.randint(0, win_width - obj_size)
        y = -obj_size  # Start above the screen
        obj_data.append([x, y, obj])
        spawn_timer = current_time
        # Gradually increase difficulty by reducing spawn delay
       
def update_objects(obj_data):
    global score
    
    for object in obj_data[:]:  # Iterate over a copy of the list
        x, y, image_data = object
        
        if y < win_height:
            y += speed 
            object[1] = y
            screen.blit(image_data, (x, y))
        else: 
            obj_data.remove(object)
            score += 1

def collision_check(obj_data, player_pos):
    global health, running, game_over
    
    player_x, player_y = player_pos[0], player_pos[1]
    player_rect = pg.Rect(player_x, player_y, player_size, player_size)

    for object in obj_data[:]:
        x, y, image_data = object
        obj_rect = pg.Rect(x, y, obj_size, obj_size)

        if player_rect.colliderect(obj_rect):
            obj_data.remove(object)
            health -= 1
            if health <= 0:
                game_over = True
                running = False

def draw_health():
    health_text = f'Health: {health}'
    health_surface = font.render(health_text, True, black)
    screen.blit(health_surface, (20, 20))

def draw_score():
    score_text = f'Score: {score}'
    score_surface = font.render(score_text, True, black)
    screen.blit(score_surface, (win_width - 150, 20))

def draw_game_over():
    screen.fill(black)
    game_over_text = large_font.render('GAME OVER', True, red)
    score_text = font.render(f'Final Score: {score}', True, white)
    restart_text = font.render('Press R to restart or Q to quit', True, white)
    
    screen.blit(game_over_text, (win_width//2 - game_over_text.get_width()//2, win_height//2 - 100))
    screen.blit(score_text, (win_width//2 - score_text.get_width()//2, win_height//2))
    screen.blit(restart_text, (win_width//2 - restart_text.get_width()//2, win_height//2 + 100))

def reset_game():
    global score, health, running, game_over, obj_data, player_pos, spawn_delay
    score = 0
    health = 5
    running = True
    game_over = False
    obj_data = []
    player_pos = [win_width / 2, win_height - player_size * 2]
    spawn_delay = 300

# Main game loop
async def main():
    while True:
        global game_over, player_pos

        if not game_over:
            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.KEYDOWN:
                    x, y = player_pos[0], player_pos[1]
                    if event.key == pg.K_LEFT and x > 0:
                        x -= 30
                    elif event.key == pg.K_RIGHT and x < win_width - player_size:
                        x += 30
                    elif event.key == pg.K_UP and y > 0:
                        y -= 30
                    elif event.key == pg.K_DOWN and y < win_height - player_size:
                        y += 30
                    player_pos = [x, y]

            # Game logic
            screen.blit(bg_image, (0, 0))
            create_object(obj_data)
            update_objects(obj_data)
            collision_check(obj_data, player_pos)
            
            # Drawing
            screen.blit(player_image, (player_pos[0], player_pos[1]))
            draw_health()
            draw_score()
            
        else:
            # Game over screen
            draw_game_over()
            
            # Event handling for game over screen
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        reset_game()
                    elif event.key == pg.K_q:
                        pg.quit()

        pg.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

asyncio.run(main())

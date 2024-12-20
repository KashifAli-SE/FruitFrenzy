def final_main_game(difficulty):
    import pygame
    import random
    import os
    from pygame import mixer

    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

    pygame.init()

    # Screen dimensions
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    game_window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FRUIT-FRENZY")

    # Background image
    background_image = pygame.image.load('game_bg.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Background music
    mixer.music.load("bg_music.mp3")
    mixer.music.play(-1)

    # Colors
    yellow = (255, 255, 0)

    # Basket attributes
    basket_width = 160
    basket_length = 128

    # Adjust settings based on difficulty
    if difficulty == "EASY":
        fruit_speed = 3
        bomb_speed = 3
        fruit_spawn_interval = 2500  # 2.5 seconds
        bomb_spawn_interval = 3000  # 3 seconds
    elif difficulty == "MEDIUM":
        fruit_speed = 5
        bomb_speed = 4
        fruit_spawn_interval = 2000  # 2 seconds
        bomb_spawn_interval = 2500  # 2.5 seconds
    elif difficulty == "HARD":
        fruit_speed = 7
        bomb_speed = 6
        fruit_spawn_interval = 1500  # 1.5 seconds
        bomb_spawn_interval = 2000  # 2 seconds

    # Game variables
    fruits = []
    bombs = []
    basket_x = 700
    basket_y = screen_height - 128
    score = 0
    gameover = False
    
    clock = pygame.time.Clock()

    # Load images
    basket_img = pygame.image.load('basket.png').convert_alpha()
    bomb_image = pygame.image.load('bomb.png').convert_alpha()
    basket_image = pygame.transform.scale(basket_img, (basket_width, basket_length))

    fruit_images =[
        pygame.image.load(f'{fruit}.png')
        for fruit in ['apple', 'orange', 'mango', 'watermelon','strawberry','banana']
    ]

    def create_fruits(num_fruits):
        for _ in range(num_fruits):
            fruit_x = random.randint(5, screen_width - 128)
            fruit_y = random.randint(-100, -20)
            fruit_image = random.choice(fruit_images)
            fruits.append([fruit_x, fruit_y, fruit_image])

    def create_bomb():
        bomb_x = random.randint(25, screen_width - 25)
        bomb_y = random.randint(-100, -20)
        bombs.append([bomb_x, bomb_y])

    def catch_fruits(score):
        for fruit in fruits[:]:
            fruit_x, fruit_y, _ = fruit
            if (basket_x-10 <= fruit_x <= basket_x + basket_width+10 and
                    basket_y - 128 <= fruit_y <= basket_y):
                fruit_collect_sound = mixer.Sound("pop.mp3")
                fruit_collect_sound.play()
                fruits.remove(fruit)
                score += 1
        return score

    def check_bomb_collision():
        for bomb in bombs[:]:
            bomb_x, bomb_y = bomb
            if basket_x - 80 <= bomb_x <= basket_x + basket_width and basket_y-80<= bomb_y <= basket_y+10:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                return True
        return False

    # Main game loop
    last_fruit_spawn_time = pygame.time.get_ticks()
    last_bomb_spawn_time = pygame.time.get_ticks()
    
    move_right=False
    move_left=False
        
    while not gameover:
        current_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        move_right = True
                    if event.key == pygame.K_LEFT:
                        move_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                    
        if move_right:
            basket_x = min(screen_width - basket_width, basket_x + 20)
        
        if move_left:
            basket_x = max(0, basket_x - 20)

        # Spawn fruits
        if current_time - last_fruit_spawn_time >= fruit_spawn_interval:
            create_fruits(3) # spawn three fruits
            last_fruit_spawn_time = current_time

        # Spawn bombs
        if current_time - last_bomb_spawn_time >= bomb_spawn_interval:
            create_bomb()
            last_bomb_spawn_time = current_time

        # Update positions
        for fruit in fruits:
            fruit[1] += fruit_speed
        for bomb in bombs:
            bomb[1] += bomb_speed

        # Remove off-screen objects
        fruits = [fruit for fruit in fruits if fruit[1] <= screen_height]
        bombs = [bomb for bomb in bombs if bomb[1] <= screen_height]

        # Collision checks
        score = catch_fruits(score)
        if check_bomb_collision():
            gameover = True
            break

        # Draw everything
        game_window.blit(background_image, (0, 0))
        for fruit in fruits:
            game_window.blit(fruit[2], (fruit[0], fruit[1]))
        for bomb in bombs:
            game_window.blit(bomb_image, (bomb[0], bomb[1]))
        game_window.blit(basket_image, (basket_x, basket_y))

        # Display score
        font = pygame.font.Font("Komigo3D-Regular.ttf", 64)
        score_text = font.render(f"Score : {score}", True, yellow)
        game_window.blit(score_text, (40, 20))
        pygame.display.update()
        clock.tick(60)

    # Game Over screen
    if gameover:
        font = pygame.font.Font("Komigo3D-Regular.ttf", 128)
        text = font.render("GAME OVER!", True, yellow)
        game_window.blit(text, (screen_width // 2 - 300, screen_height // 2 - 100))
        pygame.mixer.music.stop()
        pygame.display.update()
        pygame.time.wait(3000)

    pygame.quit()

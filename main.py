import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Explorer: Educational Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
current_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(current_dir, "images")
snd_dir = os.path.join(current_dir, "sounds")

# Load a single background image
background = pygame.image.load(os.path.join(img_dir, "space_background1.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

astronaut_img = pygame.image.load(os.path.join(img_dir, "astronaut.png")).convert_alpha()
astronaut_img = pygame.transform.scale(astronaut_img, (40, 60))

# Load and resize planets
planets = [
    pygame.image.load(os.path.join(img_dir, f"planet{i}.png")).convert_alpha()
    for i in range(1, 5)
]
planets = [pygame.transform.scale(planet, (80, 40)) for planet in planets]

asteroid_img = pygame.image.load(os.path.join(img_dir, "asteroid.png")).convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 30))

base_img = pygame.image.load(os.path.join(img_dir, "base.png")).convert_alpha()
base_img = pygame.transform.scale(base_img, (WIDTH, 40))

# Load star image
star_img = pygame.image.load(os.path.join(img_dir, "star.png")).convert_alpha()
star_img = pygame.transform.scale(star_img, (30, 30))

# Load sound effects
jump_sound = pygame.mixer.Sound(os.path.join(snd_dir, "jump.wav"))
collect_star_sound = pygame.mixer.Sound(os.path.join(snd_dir, "collect_star.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join(snd_dir, "game_over.wav"))

# Load background music and play it on loop
pygame.mixer.music.load(os.path.join(snd_dir, "background_music.mp3"))
pygame.mixer.music.play(-1)  # Loop the music

# Player
player_width, player_height = 40, 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_speed = 5
player_jump = -10
player_velocity = 0

# Platforms and Obstacles
platform_width, platform_height = 60, 20
platforms = []
asteroids = []
stars = []

# Base
base_height = 40
base = pygame.Rect(0, HEIGHT - base_height, WIDTH, base_height)
base_active = True

# Space facts
space_facts = [
    "The Sun is so big that approximately 1.3 million Earths could fit inside it.",
    "There are more stars in the universe than grains of sand on all the beaches on Earth.",
    "The footprints on the Moon will be there for 100 million years.",
    "One day on Venus is longer than one year on Earth.",
    "The largest known star, VY Canis Majoris, is about 2,000 times larger than our Sun."
    "The largest mountain in the whole universe is on Mars",
    "The Boomerang Nebula is the coldest place known, with a temperature of about -458 degrees Fahrenheit (-272 degrees Celsius), just a degree above absolute zero.",
    "Unlike sound waves, which require a medium to travel through, space is a vacuum and does not transmit sound, making it completely silent.",
    "The observable universe is about 93 billion light-years in diameter and contains an estimated two trillion galaxies."
]
random.shuffle(space_facts)  # Shuffle space facts to avoid repetition

# Font
font = pygame.font.Font(None, 24)

def create_platform(x, y):
    return {
        "rect": pygame.Rect(x, y, platform_width, platform_height),
        "image": random.choice(planets)
    }

def create_asteroid(x, y, speed):
    return {"rect": pygame.Rect(x, y, 30, 30), "speed": speed}

def create_star(x, y):
    return pygame.Rect(x, y, 30, 30)

def create_initial_platforms():
    platforms.clear()
    for i in range(10):
        x = random.randint(0, WIDTH - platform_width)
        y = HEIGHT - (i * 60) - 100
        platforms.append(create_platform(x, y))

def create_initial_stars():
    stars.clear()
    for _ in range(3):  # Start with 3 stars
        x = random.randint(0, WIDTH - 30)
        y = random.choice(platforms)["rect"].top - 30
        stars.append(create_star(x, y))

# Game states
MENU, PLAYING, GAME_OVER = 0, 1, 2
game_state = MENU
score = 0
current_fact = ""

asteroid_speed = 1  # Start speed for asteroids
level = 1  # Initial game level

def reset_game():
    global player_x, player_y, player_velocity, score, current_fact, asteroids, base_active, asteroid_speed, level
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 50
    player_velocity = 0
    score = 0
    current_fact = ""
    asteroids = []
    base_active = True
    asteroid_speed = 1  # Reset asteroid speed
    level = 1  # Reset level
    create_initial_platforms()
    create_initial_stars()

reset_game()

# Game loop
running = True
clock = pygame.time.Clock()
star_spawn_timer = 0

# Background scrolling parameters
bg_y1 = 0
bg_y2 = -HEIGHT

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                elif game_state == GAME_OVER:
                    reset_game()
                    game_state = PLAYING

    if game_state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            if player_x + player_width < 0:
                player_x = WIDTH
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            if player_x > WIDTH:
                player_x = -player_width

        # Apply gravity
        player_velocity += 0.5
        player_y += player_velocity

        # Create player rectangle for collision detection
        player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Check for collisions with platforms
        for platform in platforms:
            if player_velocity > 0 and player.colliderect(platform["rect"]):
                player_velocity = player_jump
                jump_sound.play()
                score += 1
                base_active = False

        # Check for collision with base
        if base_active and player_velocity > 0 and player.colliderect(base):
            player_velocity = player_jump
            jump_sound.play()

        # Check for collisions with asteroids
        for asteroid in asteroids:
            if player.colliderect(asteroid["rect"]):
                game_over_sound.play()
                game_state = GAME_OVER

        # Check for collisions with stars
        for star in stars:
            if player.colliderect(star):
                collect_star_sound.play()
                current_fact = space_facts.pop() if space_facts else ""  # Show fact, avoid repetition
                stars.remove(star)

        # Move screen up
        if player_y < HEIGHT // 2:
            scroll = HEIGHT // 2 - player_y
            player_y = HEIGHT // 2
            for platform in platforms:
                platform["rect"].y += scroll
                if platform["rect"].y > HEIGHT:
                    platforms.remove(platform)
                    x = random.randint(0, WIDTH - platform_width)
                    platforms.append(create_platform(x, 0))

                    # Add asteroid with 20% chance
                    if random.random() < 0.2:
                        asteroids.append(create_asteroid(random.randint(0, WIDTH - 30), 0, asteroid_speed))

            # Move asteroids
            for asteroid in asteroids:
                asteroid["rect"].y += scroll
                if asteroid["rect"].y > HEIGHT:
                    asteroids.remove(asteroid)

            # Move stars
            for star in stars:
                star.y += scroll
                if star.y > HEIGHT:
                    stars.remove(star)

            # Move base if active
            if base_active:
                base.y += scroll
                if base.top > HEIGHT:
                    base_active = False

        # Increase difficulty by increasing asteroid speed
        asteroid_speed = 1 + score // 10

        # Spawn new stars periodically
        star_spawn_timer += 1
        if star_spawn_timer >= 120:
            if len(stars) < 2:
                star_spawn_timer = 0
                x = random.randint(0, WIDTH - 30)
                y = random.choice(platforms)["rect"].top - 30
                stars.append(create_star(x, y))

        # Check for game over
        if player_y > HEIGHT:
            game_state = GAME_OVER
            game_over_sound.play()

    # Draw scrolling background
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))

    # Update background positions
    bg_y1 += 1  # Move the first background down
    bg_y2 += 1  # Move the second background down

    # Reset background positions when they move out of view
    if bg_y1 >= HEIGHT:
        bg_y1 = bg_y2 - HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = bg_y1 - HEIGHT

    # Draw everything
    if game_state == MENU:
        title_text = font.render("Space Explorer: Educational Edition", True, WHITE)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    elif game_state == PLAYING:
        for platform in platforms:
            screen.blit(platform["image"], platform["rect"])

        for asteroid in asteroids:
            screen.blit(asteroid_img, asteroid["rect"])

        for star in stars:
            screen.blit(star_img, (star.x, star.y))

        if base_active:
            screen.blit(base_img, base)

        screen.blit(astronaut_img, (player_x, player_y))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if current_fact:
            fact_lines = [current_fact[i:i + 40] for i in range(0, len(current_fact), 40)]
            for i, line in enumerate(fact_lines):
                fact_text = font.render(line, True, WHITE)
                screen.blit(fact_text, (10, HEIGHT - 60 + i * 20))
    elif game_state == GAME_OVER:
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

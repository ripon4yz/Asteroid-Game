import pygame
import random

pygame.init()

# Screen dimensions
dis_width = 800
dis_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Dynamic Asteroids with Direct Movement")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("bahnschrift", 35)

# Spaceship properties
ship_width = 30
ship_height = 30
ship_speed = 5

# Asteroid properties
asteroid_min_speed = 2
asteroid_max_speed = 6
asteroid_min_size = 20
asteroid_max_size = 50

# Bullet properties
bullet_speed = 10
bullet_width = 5
bullet_height = 10


def message(msg, color, y_offset=0):
    """Displays a message on the screen."""
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 + y_offset])


def create_asteroids(num_asteroids):
    """Create a list of asteroids with random positions and speeds."""
    asteroids = []
    for _ in range(num_asteroids):
        size = random.randint(asteroid_min_size, asteroid_max_size)
        x = random.randint(0, dis_width - size)
        y = random.randint(-600, -50)
        speed = random.uniform(asteroid_min_speed, asteroid_max_speed)
        asteroids.append({"rect": pygame.Rect(x, y, size, size), "speed": speed})
    return asteroids


# Main game loop
def game_loop():
    # Spaceship position
    ship_x = dis_width / 2
    ship_y = dis_height / 2

    # Bullet list
    bullets = []

    # Asteroids list
    asteroids = create_asteroids(5)

    # Game state
    running = True
    score = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move the spaceship
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < dis_width - ship_width:
            ship_x += ship_speed
        if keys[pygame.K_UP] and ship_y > 0:
            ship_y -= ship_speed
        if keys[pygame.K_DOWN] and ship_y < dis_height - ship_height:
            ship_y += ship_speed

        # Fire bullets
        if keys[pygame.K_SPACE]:
            bullets.append(
                pygame.Rect(ship_x + ship_width // 2 - bullet_width // 2, ship_y, bullet_width, bullet_height)
            )

        # Update bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Update asteroids
        for asteroid in asteroids[:]:
            asteroid["rect"].y += asteroid["speed"]
            if asteroid["rect"].y > dis_height:
                asteroids.remove(asteroid)
                asteroids.append(
                    {
                        "rect": pygame.Rect(
                            random.randint(0, dis_width - asteroid_max_size),
                            random.randint(-600, -50),
                            random.randint(asteroid_min_size, asteroid_max_size),
                            random.randint(asteroid_min_size, asteroid_max_size),
                        ),
                        "speed": random.uniform(asteroid_min_speed, asteroid_max_speed),
                    }
                )

        # Check collisions between bullets and asteroids
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if asteroid["rect"].colliderect(bullet):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10
                    asteroids.append(
                        {
                            "rect": pygame.Rect(
                                random.randint(0, dis_width - asteroid_max_size),
                                random.randint(-600, -50),
                                random.randint(asteroid_min_size, asteroid_max_size),
                                random.randint(asteroid_min_size, asteroid_max_size),
                            ),
                            "speed": random.uniform(asteroid_min_speed, asteroid_max_speed),
                        }
                    )
                    break

        # Check collision between spaceship and asteroids
        ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
        for asteroid in asteroids:
            if ship_rect.colliderect(asteroid["rect"]):
                message("Game Over! Press R to Restart or Q to Quit", red)
                pygame.display.update()
                pygame.time.delay(2000)
                return

        # Clear the screen
        dis.fill(black)

        # Draw spaceship
        pygame.draw.rect(dis, white, ship_rect)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(dis, red, bullet)

        # Draw asteroids
        for asteroid in asteroids:
            pygame.draw.ellipse(dis, green, asteroid["rect"])

        # Draw score
        score_text = font.render(f"Score: {score}", True, white)
        dis.blit(score_text, (10, 10))

        # Update display
        pygame.display.update()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    quit()


# Run the game
game_loop()

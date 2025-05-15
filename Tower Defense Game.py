import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900  # Increased height for the plant pool
LANE_COUNT = 5
LANE_HEIGHT = 100
CELL_WIDTH = 100  # Grid cell width
GRID_COLUMNS = SCREEN_WIDTH // CELL_WIDTH
PLANT_POOL_HEIGHT = 100  # Height of the plant pool menu

# Colors
WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Game Clock
clock = pygame.time.Clock()

# Load Sprites
plant_image = pygame.image.load("assets/plant.png")
plant_image = pygame.transform.scale(plant_image, (CELL_WIDTH - 10, LANE_HEIGHT - 10))

freezing_plant_image = pygame.image.load("assets/freezing_plant.png")
freezing_plant_image = pygame.transform.scale(freezing_plant_image, (CELL_WIDTH - 10, LANE_HEIGHT - 10))

small_plant_image = pygame.image.load("assets/small_plant.png")
small_plant_image = pygame.transform.scale(small_plant_image, (CELL_WIDTH - 10, LANE_HEIGHT - 10))

zombie_image = pygame.image.load("assets/zombie.png")
zombie_image = pygame.transform.scale(zombie_image, (CELL_WIDTH - 30, LANE_HEIGHT - 20))

zombie_2_image = pygame.image.load("assets/zombie_2.png")
zombie_2_image = pygame.transform.scale(zombie_2_image, (CELL_WIDTH - 30, LANE_HEIGHT - 20))

zombie_3_image = pygame.image.load("assets/zombie_3.png")
zombie_3_image = pygame.transform.scale(zombie_3_image, (CELL_WIDTH - 30, LANE_HEIGHT - 20))

freezed_zombie_image = pygame.image.load("assets/freezed_zombie.png")
freezed_zombie_image = pygame.transform.scale(freezed_zombie_image, (CELL_WIDTH - 30, LANE_HEIGHT - 20))

bullet_image = pygame.image.load("assets/bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (50, 50))

ice_bullet_image = pygame.image.load("assets/ice_bullet.png")
ice_bullet_image = pygame.transform.scale(ice_bullet_image, (50, 50))

small_bullet_image = pygame.image.load("assets/small_bullet.png")
small_bullet_image = pygame.transform.scale(small_bullet_image, (50, 50))

# Game objects
shooter_plants = [[None for _ in range(GRID_COLUMNS)] for _ in range(LANE_COUNT)]
zombies = []
bullets = []

# Drag-and-drop mechanics
dragging_plant = False
dragged_plant_pos = None
plant_type_dragged = None

# Shooter Plant Class
class ShooterPlant:
    def __init__(self, lane, col):
        self.lane = lane
        self.col = col
        self.x = col * CELL_WIDTH
        self.y = lane * LANE_HEIGHT + 5
        self.shoot_timer = 0

    def auto_shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= 90:  # Shoot every 1.5 seconds
            for zombie in zombies:
                if zombie.lane == self.lane:
                    bullets.append(Bullet(self.x + CELL_WIDTH, self.y + LANE_HEIGHT // 2 - 5))
                    self.shoot_timer = 0
                    break

    def draw(self):
        screen.blit(plant_image, (self.x + 5, self.y))


# Freezing Plant Class
class FreezingPlant(ShooterPlant):
    def auto_shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= 120:  # Shoot every 2 seconds
            for zombie in zombies:
                if zombie.lane == self.lane:
                    bullets.append(IceBullet(self.x + CELL_WIDTH, self.y + LANE_HEIGHT // 2 - 5))
                    self.shoot_timer = 0
                    break

    def draw(self):
        screen.blit(freezing_plant_image, (self.x + 5, self.y))


# Small Plant Class
class SmallPlant(ShooterPlant):
    def auto_shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= 60:  # Shoot every 1 second
            for zombie in zombies:
                if zombie.lane == self.lane:
                    bullets.append(SmallBullet(self.x + CELL_WIDTH, self.y + LANE_HEIGHT // 2 - 5))
                    self.shoot_timer = 0
                    break

    def draw(self):
        screen.blit(small_plant_image, (self.x + 5, self.y))


# Bullet Class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.x += self.speed

    def draw(self):
        screen.blit(bullet_image, (self.x, self.y))


# Ice Bullet Class
class IceBullet(Bullet):
    def draw(self):
        screen.blit(ice_bullet_image, (self.x, self.y))


# Small Bullet Class
class SmallBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 2  # Twice the damage of normal bullets

    def draw(self):
        screen.blit(small_bullet_image, (self.x, self.y))


# Zombie Class
class Zombie:
    def __init__(self, lane):
        self.lane = lane
        self.x = SCREEN_WIDTH
        self.y = lane * LANE_HEIGHT + 10
        self.health = 3
        self.speed = 2
        self.frozen = False
        self.frozen_timer = 0

    def move(self):
        if not self.frozen:
            self.x -= self.speed
        else:
            self.frozen_timer += 1
            if self.frozen_timer >= 300:  # 5 seconds freeze (60 FPS * 5)
                self.frozen = False
                self.frozen_timer = 0

    def draw(self):
        if self.frozen:
            screen.blit(freezed_zombie_image, (self.x, self.y))
        else:
            screen.blit(zombie_image, (self.x, self.y))


# Zombie Type 2 Class
class Zombie2(Zombie):
    def draw(self):
        if self.frozen:
            screen.blit(freezed_zombie_image, (self.x, self.y))
        else:
            screen.blit(zombie_2_image, (self.x, self.y))


# Zombie Type 3 Class
class Zombie3(Zombie):
    def draw(self):
        if self.frozen:
            screen.blit(freezed_zombie_image, (self.x, self.y))
        else:
            screen.blit(zombie_3_image, (self.x, self.y))


# Check for losing condition
def check_loss():
    for zombie in zombies:
        if zombie.x <= 0:
            return True
    return False


# Draw the grid
def draw_background():
    screen.fill(GREEN)  # Fill the entire screen with the game background color

    # Draw the grid lanes
    for i in range(LANE_COUNT):
        lane_color = DARK_GREEN if i % 2 == 0 else GREEN
        pygame.draw.rect(screen, lane_color, (0, i * LANE_HEIGHT, SCREEN_WIDTH, LANE_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, i * LANE_HEIGHT), (SCREEN_WIDTH, i * LANE_HEIGHT), 2)
        for j in range(GRID_COLUMNS):
            pygame.draw.line(screen, BLACK, (j * CELL_WIDTH, 0), (j * CELL_WIDTH, LANE_HEIGHT * LANE_COUNT), 2)

    # Fill the plant pool area
    pygame.draw.rect(screen, WHITE, (0, LANE_COUNT * LANE_HEIGHT, SCREEN_WIDTH, PLANT_POOL_HEIGHT))


# Draw the plant pool
def draw_plant_pool():
    pool_y = LANE_COUNT * LANE_HEIGHT
    screen.fill(WHITE, rect=(0, pool_y, SCREEN_WIDTH, PLANT_POOL_HEIGHT))

    # Normal plant
    screen.blit(plant_image, (CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2))
    pygame.draw.rect(screen, BLACK, (CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT), 2)

    # Freezing plant
    screen.blit(freezing_plant_image, (3 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2))
    pygame.draw.rect(screen, BLACK, (3 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT), 2)

    # Small plant
    screen.blit(small_plant_image, (5 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2))
    pygame.draw.rect(screen, BLACK, (5 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT), 2)

    return {
        "normal_plant": (CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT),
        "freezing_plant": (3 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT),
        "small_plant": (5 * CELL_WIDTH // 2, pool_y + (PLANT_POOL_HEIGHT - LANE_HEIGHT) // 2, CELL_WIDTH, LANE_HEIGHT),
    }


# Spawn zombies randomly
def spawn_zombies():
    if random.randint(0, 100) < 2:  # 2% chance each frame to spawn a zombie
        lane = random.randint(0, LANE_COUNT - 1)
        zombie_type = random.choice([Zombie, Zombie2, Zombie3])
        zombies.append(zombie_type(lane))


# Main game loop
def main():
    global dragging_plant, dragged_plant_pos, plant_type_dragged

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start dragging a plant
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                plant_pool_positions = draw_plant_pool()

                # Check which plant is being dragged
                for plant_type, (x, y, w, h) in plant_pool_positions.items():
                    if x <= mx <= x + w and y <= my <= y + h:
                        dragging_plant = True
                        dragged_plant_pos = (mx, my)
                        plant_type_dragged = plant_type

            # Drop the plant onto the grid
            if event.type == pygame.MOUSEBUTTONUP and dragging_plant:
                mx, my = pygame.mouse.get_pos()
                lane = my // LANE_HEIGHT
                col = mx // CELL_WIDTH
                if 0 <= lane < LANE_COUNT and 0 <= col < GRID_COLUMNS and not shooter_plants[lane][col]:
                    if plant_type_dragged == "normal_plant":
                        shooter_plants[lane][col] = ShooterPlant(lane, col)
                    elif plant_type_dragged == "freezing_plant":
                        shooter_plants[lane][col] = FreezingPlant(lane, col)
                    elif plant_type_dragged == "small_plant":
                        shooter_plants[lane][col] = SmallPlant(lane, col)
                dragging_plant = False

        # Draw the game elements
        draw_background()

        # Draw plant pool
        draw_plant_pool()

        # Draw dragged plant
        if dragging_plant:
            mx, my = pygame.mouse.get_pos()
            if plant_type_dragged == "normal_plant":
                screen.blit(plant_image, (mx - CELL_WIDTH // 2, my - LANE_HEIGHT // 2))
            elif plant_type_dragged == "freezing_plant":
                screen.blit(freezing_plant_image, (mx - CELL_WIDTH // 2, my - LANE_HEIGHT // 2))
            elif plant_type_dragged == "small_plant":
                screen.blit(small_plant_image, (mx - CELL_WIDTH // 2, my - LANE_HEIGHT // 2))

        # Update and draw shooter plants
        for lane in shooter_plants:
            for plant in lane:
                if plant:
                    plant.auto_shoot()
                    plant.draw()

        # Update and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.x > SCREEN_WIDTH:
                bullets.remove(bullet)

        # Update and draw zombies
        for zombie in zombies[:]:
            zombie.move()
            zombie.draw()
            # Check for collisions with bullets
            for bullet in bullets[:]:
                if zombie.x < bullet.x < zombie.x + CELL_WIDTH - 30 and zombie.y < bullet.y < zombie.y + LANE_HEIGHT - 20:
                    if isinstance(bullet, IceBullet):
                        zombie.frozen = True
                        zombie.frozen_timer = 0
                    else:
                        zombie.health -= getattr(bullet, 'damage', 1)  # Default damage is 1
                    bullets.remove(bullet)
                    if zombie.health <= 0:
                        zombies.remove(zombie)
                        break

        # Spawn new zombies
        spawn_zombies()

        # Check for losing condition
        if check_loss():
            font = pygame.font.Font(None, 72)
            text = font.render("You Lose!", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

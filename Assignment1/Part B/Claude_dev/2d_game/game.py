import pygame
import random
from game_state import GameState

def load_and_scale_image(file_path, size):
    image = pygame.image.load(file_path).convert_alpha()
    return pygame.transform.scale(image, size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_scale_image("2d_game/assets/player.png", (80,80))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_scale_image("2d_game/assets/collectible.png", (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 780)
        self.rect.y = random.randint(0, 580)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_scale_image("2d_game/assets/obstacle.png", (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 770)
        self.rect.y = random.randint(0, 570)

class Game:
    def __init__(self, screen, font, sound_manager):
        self.screen = screen
        self.font = font
        self.sound_manager = sound_manager
        self.player = Player()
        self.collectibles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.score = 0
        self.level = 1
        self.spawn_collectibles()
        self.spawn_obstacles()

    def spawn_collectibles(self):
        for _ in range(5):
            self.collectibles.add(Collectible())

    def spawn_obstacles(self):
        for _ in range(self.level):
            self.obstacles.add(Obstacle())

    def draw(self):
        self.screen.fill((0, 0, 100))  # Dark blue background
        self.screen.blit(self.player.image, self.player.rect)
        self.collectibles.draw(self.screen)
        self.obstacles.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

    def run(self):
        self.player.update()
        self.draw()

        collided = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        if collided:
            self.sound_manager.play_collect_sound()
            self.score += len(collided)
            self.spawn_collectibles()

        if pygame.sprite.spritecollideany(self.player, self.obstacles):
            return GameState.GAME_OVER

        if self.score >= self.level * 10:
            self.level += 1
            self.obstacles.empty()
            self.spawn_obstacles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU

        return GameState.GAME
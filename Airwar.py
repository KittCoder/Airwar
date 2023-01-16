# Fly a jet through a missile barrage
import pygame
import random

# Define a few constant variables that we will use
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SKY_BLUE = (135,206,250)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the images and process for use
jet_image = pygame.image.load('./Images/jet.png').convert()
missile_image = pygame.image.load('./Images/missile.png').convert()
cloud_image = pygame.image.load('./images/cloud.png').convert()

# Define a player sprite and add the ability to move it around
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = jet_image
        self.surf.set_colorkey(WHITE, pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        
# Define an enemy missile as a sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = missile_image
        self.surf.set_colorkey(WHITE, pygame.RLEACCEL)
        
        # Randomly position each missile on the screen
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100), random.randint(0,SCREEN_HEIGHT)))
        self.speed = (random.randint(5,20))
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
            
# Define a cloud object as a sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = cloud_image
        self.surf.set_colorkey(BLACK, pygame.RLEACCEL)
        
        # The starting position of every cloud will be determined at random
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100), random.randint(0,SCREEN_HEIGHT)))
        
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill()

# Create custom events that will trigger adding a cloud
ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)

ADDENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 250)

# Create 1 player
player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
allsprites.add(player)

# Define our game loop
RUNNING = True

while RUNNING:
    # Look at what events have been generated
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
        elif event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == ADDCLOUD:
            # We are proccessing an ADDCLOUD event
            # we need to create a new cloud and put
            # it into the lists we created
            new_cloud = Cloud()
            clouds.add(new_cloud)
            allsprites.add(new_cloud)
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            allsprites.add(new_enemy)
        
    # Get all pressed keys
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    # Update our sprites
    clouds.update()
    enemies.update() 
    
    screen.fill(SKY_BLUE)
        
    for sprite in allsprites:
            screen.blit(sprite.surf, sprite.rect)
        
    # Check whether there has been a collision
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        RUNNING = False
    # Flip the screen
    pygame.display.flip()
            
    # Target 30 fps
    clock.tick(30)
            
pygame.quit()
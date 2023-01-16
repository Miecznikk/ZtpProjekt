import pygame

FRAMES = 60
TMP_SPRITE = pygame.image.load('assets/images/player.png')

BULLET_SPRITE = pygame.image.load('assets/images/bullet_player.png')
TRIPLE_BULLET_SPRITE = pygame.image.load('assets/images/triple_bullet.png')

BACKGROUND_IMAGE = pygame.image.load('assets/images/background.jpg')

ENEMY_SPRITES = {
    'easy': pygame.image.load('assets/images/enemy_easy.png'),
    'medium': pygame.image.load('assets/images/enemy_medium.png'),
    'hard': pygame.image.load('assets/images/enemy_hard.png'),
}

UPGRADE_SPRITES = {
    'health': pygame.image.load('assets/images/health_upgrade.png'),
    'attack': pygame.image.load('assets/images/attack_upgrade.png'),
    'triple_shot': pygame.image.load('assets/images/triple_shot.png')
}

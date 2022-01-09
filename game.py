import pygame


class Player(pygame.sprite.Sprite):
    image = pygame.image.load("sprites/player_idle.png")

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.player_idle = Player.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if not pygame.sprite.collide_mask(self, level):
            self.rect = self.rect.move(0, 5)
        else:
            return 'collide'


class Level(pygame.sprite.Sprite):
    image = pygame.image.load('levels/lvl1.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Level.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class CameraTarget(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/camera_target.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = CameraTarget.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, target):
        if target.rect.x >= self.rect.x <= self.rect.x + 10:
            self.rect.x += 5


if __name__ == '__main__':
    def main_movement():
        global JUMP_COUNT
        if keys[pygame.K_LEFT]:
            player.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            player.rect.x += SPEED
        if keys[pygame.K_UP]:
            if not JUMP_COUNT >= 250:
                player.rect.y -= JUMP_HIGH
                JUMP_COUNT += JUMP_HIGH
            else:
                return


    all_sprites = pygame.sprite.Group()
    pygame.init()
    pygame.display.set_caption('war')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True

    level = Level()

    SPEED = 5
    JUMP_COUNT = 0
    JUMP_HIGH = 15

    camera = Camera()

    camera_target = CameraTarget(400, 190)

    clock = pygame.time.Clock()
    player = Player(200, 0)
    while running:
        screen.fill((16, 173, 197))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        main_movement()

        result = player.update()
        if result == 'collide':
            JUMP_COUNT = 0

        # изменяем ракурс камеры
        camera_target.update(player)
        camera.update(camera_target)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)
        pygame.display.flip()
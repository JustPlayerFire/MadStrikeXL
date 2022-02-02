import pygame
import random
from math import hypot


class Player(pygame.sprite.Sprite):
    image = pygame.image.load("sprites/player_idle_right.png")

    idle_right = pygame.image.load("sprites/player_idle_right.png")
    idle_left = pygame.image.load("sprites/player_idle_left.png")

    run_right = [pygame.image.load('sprites/player_run_rightshoot1.png'),
                 pygame.image.load('sprites/player_run_rightshoot2.png'),
                 pygame.image.load('sprites/player_run_rightshoot3.png'),]

    run_left = [pygame.image.load('sprites/player_run_leftshoot1.png'),
                 pygame.image.load('sprites/player_run_leftshoot2.png'),
                 pygame.image.load('sprites/player_run_leftshoot3.png'), ]

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.sprite = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.side = 'right'
        self.reload = 0
        self.health = 500
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        global running
        stand = False
        if self.health <= 0:
            self.kill()
            self.rect.x = -10
            self.rect.y = -30
        for i in range(len(obstacles)):
            if pygame.sprite.collide_mask(self, obstacles[i]):
                stand = True
                break
        if stand:
            return 'collide'
        if pygame.sprite.collide_mask(self, jet):
            running = False
            print('Level Complete!')
        if not pygame.sprite.collide_mask(self, level):
            self.rect = self.rect.move(0, 5)
        else:
            return 'collide'

    def animation(self, command):
        global ANIM_COUNT
        if ANIM_COUNT + 1 >= 15:
            ANIM_COUNT = 0

        if command == 'left':
            player.image = player.run_left[ANIM_COUNT // 5]
            self.side = 'left'
            ANIM_COUNT += 1
        elif command == 'right':
            player.image = player.run_right[ANIM_COUNT // 5]
            self.side = 'right'
            ANIM_COUNT += 1
        elif command == 'idle_left':
            player.image = player.idle_left
            self.side = 'left'
        elif command == 'idle_right':
            player.image = player.idle_right
            self.side = 'right'


class BulletEnemy(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/bullet_enemy.png')
    image2 = pygame.image.load('sprites/bullet_enemy_small.png')

    def __init__(self, x, y, bullet_size='big'):
        super().__init__(all_sprites)
        if bullet_size == 'small':
            self.image = BulletEnemy.image2
        elif bullet_size == 'big':
            self.image = BulletEnemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 10
        self.rect.x = x
        self.rect.y = y + 20
        self.reload = 0
        self.dir = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        length = hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

    def update(self):
        if self.rect.x >= 800 or self.rect.x <= 0:
            self.kill()
            return

        if pygame.sprite.collide_mask(self, player):
            player.health -= 1
            self.kill()
            return

        self.rect.x = self.rect.x + self.dir[0] * self.speed
        self.rect.y = (self.rect.y + self.dir[1] * self.speed) + 1


class BulletPlayer(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/bullet.png')

    def __init__(self, x, y,  side):
        super().__init__(all_sprites)
        self.image = BulletPlayer.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.side = side
        self.speed = 20
        self.rect.x = x + 25
        self.rect.y = y + 20

    def update(self):
        if self.side == 'left':
            self.rect.x -= self.speed
        elif self.side == 'right':
            self.rect.x += self.speed
        if self.rect.x >= 800 or self.rect.x <= 0:
            self.kill()
            return
        for i in range(len(obstacles)):
            try:
                if pygame.sprite.collide_mask(self, obstacles[i].tesla):
                    obstacles[i].tesla.health -= 1
                    obstacles[i].tesla.update()
                    self.update()
                    self.kill()
            except AttributeError:
                pass
            if pygame.sprite.collide_mask(self, obstacles[i]):
                self.kill()


class Tesla(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/tesla_idle1.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Tesla.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.reload = 0
        self.health = 20
        self.rect.x = x + random.randrange(20, 50)
        self.rect.y = y - 70

    def update(self):
        if self.health <= 0:
            self.mask.clear()
            self.kill()
            self.rect.x = -30
            self.rect.y = -30


class Drone(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/drone.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Drone.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.reload = 0
        self.rect.x = x
        self.rect.y = y
        self.side = 'left'
        self.count_move = 1500
        self.speed = 5

    def move(self):
        if self.count_move <= 0:
            if self.side == 'left':
                self.side = 'right'
                self.count_move = 1500
            elif self.side == 'right':
                self.side = 'left'
                self.count_move = 1500
        if self.side == 'left':
            self.rect.x -= self.speed
        elif self.side == 'right':
            self.rect.x += self.speed
        self.count_move -= 2


class Obstacle(pygame.sprite.Sprite):
    image = pygame.image.load('level_decor/fly_ground.png')

    def __init__(self, x, y, spawn_tesla=False):
        super().__init__(all_sprites)
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.x = x
        self.rect.y = y
        if spawn_tesla:
            self.tesla = Tesla(self.rect.x, self.rect.y)


class Level(pygame.sprite.Sprite):
    image = pygame.image.load('level_decor/ground.png')
    bg = pygame.image.load('level_decor/bg.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Level.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height
        self.bg_x = 0

    def load_bg(self):
        screen.blit(Level.bg, (self.bg_x, 0))


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
        if target.rect.x >= self.rect.x <= self.rect.x + 10 <= 3200:
            self.rect.x += 5
            level.bg_x -= 1


class EndLVL(pygame.sprite.Sprite):
    image = pygame.image.load('level_decor/jet.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = EndLVL.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height
        self.rect.x = 4100


if __name__ == '__main__':
    def main_movement():
        global JUMP_COUNT, ANIM_COUNT, command
        if keys[pygame.K_SPACE]:
            if player.reload <= 0:
                player_bullets.append(BulletPlayer(player.rect.x, player.rect.y, player.side))
                player.reload = 15
        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speed
            command = 'left'
        elif keys[pygame.K_RIGHT]:
            player.rect.x += player.speed
            command = 'right'
        else:
            if command == 'right':
                command = 'idle_right'
            elif command == 'left':
                command = 'idle_left'
        if keys[pygame.K_UP]:
            if not JUMP_COUNT >= 250:
                player.rect.y -= JUMP_HIGH
                JUMP_COUNT += JUMP_HIGH
            else:
                return
        player.animation(command)

    all_sprites = pygame.sprite.Group()
    pygame.init()
    pygame.display.set_caption('war')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True

    level = Level()


    JUMP_COUNT = 0
    JUMP_HIGH = 14
    ANIM_COUNT = 0
    command = ''

    camera = Camera()

    obstacles = [Obstacle(700, 200, True),
                 Obstacle(830, 150),
                 Obstacle(1000, 100, True),
                 Obstacle(1200, 100),
                 Obstacle(1400, 100, True),
                 Obstacle(1800, 250, True),
                 Obstacle(2000, 200),
                 Obstacle(2200, 150, True),
                 Obstacle(2400, 100, True),
                 Obstacle(3000, 200),
                 Obstacle(3200, 150, True)]

    drones = [Drone(3000, 20)]

    player_bullets = []

    enemy_bullets = []

    jet = EndLVL()

    camera_target = CameraTarget(400, 190)

    clock = pygame.time.Clock()
    player = Player(200, 0)
    while running:
        level.load_bg()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        main_movement()

        result = player.update()

        if player.reload > 0:
            player.reload -= 1

        if result == 'collide':
            JUMP_COUNT = 0

        for bullet in player_bullets:
            bullet.update()

        for bullet in enemy_bullets:
            bullet.update()

        for i in range(len(drones)):
            drones[i].move()
            if drones[i].reload <= 0:
                enemy_bullets.append(BulletEnemy(drones[i].rect.x, drones[i].rect.y, 'small'))
                drones[i].reload = 15
            if drones[i].reload > 0:
                drones[i].reload -= 1

        for i in range(len(obstacles)):
            try:
                if obstacles[i].tesla.reload > 0:
                    obstacles[i].tesla.reload -= 1
                if obstacles[i].tesla.reload <= 0:
                    enemy_bullets.append(BulletEnemy(obstacles[i].tesla.rect.x, obstacles[i].tesla.rect.y))
                    obstacles[i].tesla.reload = 80
            except AttributeError:
                continue

        # изменяем ракурс камеры
        camera_target.update(player)
        camera.update(camera_target)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)
        pygame.display.flip()
import pygame
import random
from math import hypot
from button import Button
import sys


class Player(pygame.sprite.Sprite):
    image = pygame.image.load("sprites/player_idle_right.png")

    idle_right = pygame.image.load("sprites/player_idle_right.png")
    idle_left = pygame.image.load("sprites/player_idle_left.png")

    run_right = [pygame.image.load('sprites/player_run_rightshoot1.png'),
                 pygame.image.load('sprites/player_run_rightshoot2.png'),
                 pygame.image.load('sprites/player_run_rightshoot3.png')]

    run_left = [pygame.image.load('sprites/player_run_leftshoot1.png'),
                pygame.image.load('sprites/player_run_leftshoot2.png'),
                pygame.image.load('sprites/player_run_leftshoot3.png')]

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.sprite = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.side = 'right'
        self.reload = 0
        self.health = 150
        self.score = 0
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        global running, jet, mouse
        stand = False
        if self.health <= 0 or self.rect.y >= 360:
            self.kill()
            mouse.destroy()
            over_screen('game over')
        for i in range(len(obstacles)):
            if pygame.sprite.collide_mask(self, obstacles[i]):
                stand = True
                break
        if stand:
            return 'collide'
        if pygame.sprite.collide_mask(self, jet):
            lvl_loader.clear_level()
            mouse.destroy()
            over_screen('complete')
        if not pygame.sprite.collide_mask(self, level):
            self.rect = self.rect.move(0, 5)
        else:
            return 'collide'

    def animation(self):
        global ANIM_COUNT, command
        command = command
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

    def hurt(self, dmg):
        self.health -= dmg


class BulletEnemy(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/bullet_enemy.png')
    image2 = pygame.image.load('sprites/bullet_enemy_small.png')

    def __init__(self, x, y, bullet_size='big', collide=True):
        super().__init__(all_sprites)
        if bullet_size == 'small':
            self.image = BulletEnemy.image2
        elif bullet_size == 'big':
            self.image = BulletEnemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.collide = collide
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
        if self.collide:
            if self.rect.x >= 800 or self.rect.x <= 0:
                self.kill()
                return
        else:
            if self.rect.x <= 0:
                self.kill()
                return

        if pygame.sprite.collide_mask(self, player):
            player.hurt(1)
            self.kill()

        self.rect.x = self.rect.x + self.dir[0] * self.speed
        self.rect.y = (self.rect.y + self.dir[1] * self.speed)


class BulletPlayer(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/bullet.png')

    def __init__(self, x, y, side):
        super().__init__(all_sprites)
        self.image = BulletPlayer.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.side = side
        self.speed = 20
        self.rect.x = x + 25
        self.rect.y = y + 20
        self.dir = (pygame.mouse.get_pos()[0] - self.rect.x, pygame.mouse.get_pos()[1] - self.rect.y)
        length = hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

    def update(self):
        self.rect.x = self.rect.x + self.dir[0] * self.speed
        self.rect.y = (self.rect.y + self.dir[1] * self.speed) + 1
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
                    player.score += 1
            except AttributeError:
                pass
        if pygame.sprite.collide_mask(self, boss):
            boss.health -= 1
            player.score += 1
            boss.update()
            self.update()
            self.kill()


class Spike(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/spike.png')

    def __init__(self, x, y, count=1):
        super().__init__(all_sprites)
        self.image = Spike.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            player.hurt(10)
            self.mask.clear()
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


class BossTesla(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/Tesla_wall.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BossTesla.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.reload = 0
        self.health = 300
        self.rect.x = 3500
        self.rect.y = 0

    def update(self):
        if self.health <= 0:
            self.mask.clear()
            self.kill()
            self.rect.x = -50
            self.rect.y = -50


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

    def __init__(self, x, y, spawn_tesla='False'):
        super().__init__(all_sprites)
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.x = x
        self.rect.y = y
        if spawn_tesla == 'True':
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
        self.bg_x = -100

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


class Border(pygame.sprite.Sprite):
    image = pygame.image.load('level_decor/ground_borders.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Border.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        # self.mask = pygame.mask.from_surface(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()


class CameraTarget(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/camera_target.png')
    image_invisible = pygame.image.load('sprites/camera_target_invisible.png')

    def __init__(self, x, y, side):
        super().__init__(all_sprites)
        self.image = CameraTarget.image
        self.rect = self.image.get_rect()
        self.image = CameraTarget.image_invisible
        self.rect.x = x
        self.rect.y = y
        self.side = side

    def update(self, target, other):
        if self.side == 'right':
            if target.rect.x >= self.rect.x <= self.rect.x + 10 <= 3200:
                self.rect.x += player.speed
                other.rect.x += player.speed
                level.bg_x -= 1
        elif self.side == 'left':
            if target.rect.x <= self.rect.x <= self.rect.x + 10:
                self.rect.x -= player.speed
                other.rect.x -= player.speed
                level.bg_x += 1


class Mouse(pygame.sprite.Sprite):
    image = pygame.image.load('sprites/mouse.png')

    def __init__(self):
        super().__init__(arrow)
        self.image = Mouse.image
        self.rect = self.image.get_rect()

    def focus(self, coord):
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            self.rect.x = coord[0]
            self.rect.y = coord[1]

    def destroy(self):
        pygame.mouse.set_visible(True)


class EndLVL(pygame.sprite.Sprite):
    image = pygame.image.load('level_decor/jet.png')

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = EndLVL.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height
        self.rect.x = x


class LevelLoader:
    def __init__(self):
        self.current_lvl = 1

    def clear_level(self):
        global obstacles, drones, jet, lvl_process
        obstacles = []
        drones = []
        jet = None
        lvl_process = True

    def load_level(self, num):
        global obstacles, drones, jet, lvl_process, spikes
        obs = open('level_params/level' + str(num) + '/fly_ground_param.txt', 'r').readlines()
        obs = [str(i).split() for i in obs]
        obstacles = []
        for i in range(len(obs)):
            try:
                third_p = obs[i][2]
            except IndexError:
                obstacles.append(Obstacle(int(obs[i][0]), int(obs[i][1])))
                continue
            obstacles.append(Obstacle(int(obs[i][0]), int(obs[i][1]), third_p))

        dron = open('level_params/level' + str(num) + '/drones_param.txt', 'r').readlines()
        dron = [str(i).split() for i in dron]
        drones = [Drone(int(dron[i][0]), int(dron[i][1])) for i in range(len(dron))]

        spik = open('level_params/level' + str(num) + '/spikes_coord.txt', 'r').readlines()
        spik = [str(i).split() for i in spik]
        for i in range(len(spik)):
            try:
                distance_plus = 30
                for j in range(int(spik[i][2])):
                    spikes.append(Spike(int(spik[i][0]) + (distance_plus * j), int(spik[i][1])))
            except IndexError:
                spikes.append(Spike(int(spik[i][0]), int(spik[i][1])))

        jet1 = open('level_params/level' + str(num) + '/jet_coord.txt', 'r').readlines()
        jet = EndLVL(int(jet1[0]))
        lvl_process = False


def place_text(text, x, y, font_size=36):
    font = pygame.font.Font(None, font_size)
    text = font.render(str(text), False, (0, 0, 0))
    screen.blit(text, (x, y))


def main_menu():
    menu_running = True
    while menu_running:
        mouse_pos = pygame.mouse.get_pos()

        bg = pygame.image.load('sprites/bg_menu.png')
        title = pygame.image.load('sprites/title.png')
        menu_rect = title.get_rect(center=(400, 50))

        start_button = Button(image=pygame.image.load("sprites/button_start.png"), pos=(400, 200))

        screen.blit(bg, (0, 0))
        screen.blit(title, menu_rect)

        start_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos):
                    menu_running = False

        pygame.display.update()


def over_screen(stype):
    bg = pygame.image.load('sprites/bg_menu.png')
    if stype == 'complete':
        title = pygame.image.load('sprites/title_passed.png')
    elif stype == 'game over':
        title = pygame.image.load('sprites/title_over.png')
    menu_rect = title.get_rect(center=(400, 50))

    exit_button = Button(image=pygame.image.load("sprites/button_exit.png"), pos=(400, 300))
    complete_running = True
    while complete_running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))
        screen.blit(title, menu_rect)

        exit_button.update(screen)

        place_text('Счёт: ' + str(player.score + player.health), 350, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    arrow = pygame.sprite.Group()
    pygame.init()
    pygame.display.set_caption('Mad Strike XL')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    main_menu()

    def camera_move():
        global command
        if command == 'right':
            camera_target_right.update(player, camera_target_left)
            camera.update(camera_target_right)
        elif command == 'left':
            camera_target_left.update(player, camera_target_right)
            camera.update(camera_target_left)

        if command == 'idle_left' or command == 'idle_right':
            pass
        else:
            for sprite in all_sprites:
                camera.apply(sprite)


    def shoot():
        if player.reload <= 0:
            player_bullets.append(BulletPlayer(player.rect.x, player.rect.y, player.side))
            player.reload = 15


    def main_movement():
        global JUMP_COUNT, ANIM_COUNT, command
        if keys[pygame.K_a]:
            if pygame.sprite.collide_mask(player, border_right):
                player.rect.x += 10
                return
            player.rect.x -= player.speed
            command = 'left'
        elif keys[pygame.K_d]:
            if pygame.sprite.collide_mask(player, boss):
                return
            if pygame.sprite.collide_mask(player, border_left):
                player.rect.x -= 10
                return
            player.rect.x += player.speed
            command = 'right'
        else:
            if command == 'right':
                command = 'idle_right'
            elif command == 'left':
                command = 'idle_left'
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if not JUMP_COUNT >= 250:
                player.rect.y -= JUMP_HIGH
                JUMP_COUNT += JUMP_HIGH
        if keys[pygame.K_u]:
            print(player.rect.x, player.rect.y)
        player.animation()

    JUMP_COUNT = 0
    JUMP_HIGH = 14
    ANIM_COUNT = 0
    command = 'right'

    jet = None

    obstacles = []

    drones = []

    spikes = []

    level = Level()
    lvl_loader = LevelLoader()
    mouse = Mouse()
    lvl_loader.load_level(1)

    do_shoot = False

    lvl_process = True

    player_bullets = []

    enemy_bullets = []

    camera = Camera()

    camera_target_right = CameraTarget(200, 190, 'right')
    camera_target_left = CameraTarget(200, 190, 'left')

    clock = pygame.time.Clock()

    player = Player(200, 200)
    running = True

    boss = BossTesla()

    border_left = Border(0, 300)
    border_right = Border(4000, 300)
    mouse.focus(pygame.mouse.get_pos())
    while running:
        level.load_bg()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                do_shoot = True
            if event.type == pygame.MOUSEBUTTONUP:
                do_shoot = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mouse.focus(event.pos)

        keys = pygame.key.get_pressed()
        if do_shoot:
            shoot()

        main_movement()
        player.animation()

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

        for spike in spikes:
            spike.update()

        for i in range(len(obstacles)):
            try:
                if obstacles[i].tesla.reload > 0:
                    obstacles[i].tesla.reload -= 1
                if obstacles[i].tesla.reload <= 0:
                    enemy_bullets.append(BulletEnemy(obstacles[i].tesla.rect.x, obstacles[i].tesla.rect.y))
                    obstacles[i].tesla.reload = 80
            except AttributeError:
                continue

        if boss.reload <= 0:
            enemy_bullets.append(BulletEnemy(boss.rect.x + 10, boss.rect.y + 120, 'big', False))
            enemy_bullets.append(BulletEnemy(boss.rect.x + 10, boss.rect.y + 180, 'big', False))
            boss.reload = 40
        if boss.reload > 0:
            boss.reload -= 1

        place_text('Здоровье: ' + str(player.health), 50, 20)
        place_text('Счёт: ' + str(player.score), 50, 50)
        camera_move()

        all_sprites.draw(screen)
        arrow.draw(screen)
        pygame.display.flip()
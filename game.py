import pygame
import time
import random

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

LASER_COL = (124, 252, 0)
NEW_COLOR = (0, 191, 255)
TOMATO = (255, 99, 71)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_RED = (255, 20, 147)
DEEP_SKY = (0, 255, 127)

LASER_HEIGHT = 37

intro_picture = pygame.image.load("pics/intro.jpg")
beetle = pygame.image.load('pics/beatles.png')
beetle1 = pygame.image.load('pics/beatle1.png')
background_image = pygame.image.load("pics/background.jpg")
carImg = pygame.image.load('pics/wing.png')

RECORD_POINTS = 0
with open('record_table.txt', 'r') as record_table:
    r = record_table.readline()
    RECORD_POINTS = int(r) if r else 0

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Жуки атакуют')
clock = pygame.time.Clock()


def point_count(count):
    font = pygame.font.SysFont('FreeSansBold.ttf', 25)
    text = font.render('Жуков: ' + str(count), True, BLACK)
    gameDisplay.blit(text, (10, 10))


def aim(count):
    font = pygame.font.SysFont('FreeSansBold.ttf', 25)
    text = font.render('Подбил: ' + str(count), True, WHITE)
    gameDisplay.blit(text, (700, 10))


def button(msg, x, y, w, h, i_color, a_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(num_buttons=3)
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, a_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            pygame.mixer.music.stop()
            action()
    else:
        pygame.draw.rect(gameDisplay, i_color, (x, y, w, h))
    small_text = pygame.font.Font('FreeSansBold.ttf', 20)
    text_surf, text_rect = text_object(msg, small_text)
    text_rect.center = (x + w / 2, y + h / 2)
    gameDisplay.blit(text_surf, text_rect)


def laser(laser_x, laser_y, laser_color):
    pygame.draw.rect(gameDisplay, laser_color, (laser_x, laser_y, 5, LASER_HEIGHT))


def game_intro():
    intro = True
    with open('record_table.txt', 'r') as r_table:
        RECORD_POINTS = int(r_table.readline())
    while intro:
        gameDisplay.blit(intro_picture, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        large_text = pygame.font.Font('FreeSansBold.ttf', 75)
        small_text = pygame.font.Font('FreeSansBold.ttf', 25)

        rec_surf, rec_rect = text_object('Рекорд убийств: '+str(RECORD_POINTS), small_text)
        text_surf, text_rect = text_object('Жуки атакуют', large_text)

        text_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2.5)
        rec_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 1.8)

        gameDisplay.blit(text_surf, text_rect)
        gameDisplay.blit(rec_surf, rec_rect)

        button('Начать!', 120, 450, 150, 100, NEW_COLOR, DEEP_SKY, game_loop)
        button('Выйти', 520, 450, 150, 100, TOMATO, BRIGHT_RED, quit)

        pygame.display.update()
        clock.tick(45)


def things(picture, thingx, thingy):
    gameDisplay.blit(picture, (thingx, thingy))


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


car_width = carImg.get_width()


def text_object(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('FreeSansBold.ttf', 75)
    text_surf, text_rect = text_object(text, large_text)
    text_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)
    game_intro()


def things_dodged(count):
    font = pygame.font.SysFont('FreeSansBold', 25)
    text = font.render('Dodged: ' + str(count), True, BLACK)
    gameDisplay.blit(text, (0, 0))


def crash(points):
    if points > RECORD_POINTS:
        with open('record_table.txt', 'w') as r_table:
            r_table.write(str(points))
    pygame.mixer.music.load('music/fail.mp3')
    pygame.mixer.music.play()
    message_display('Ты съеден!')

    time.sleep(5)


def game_loop():
    laser_int = 0
    dodge = 0  # СЧЁТ ВСЕХ ЖУКОВ
    points = 0  # СЧЁТ ПОДБИТЫХ ЖУКОВ
    laser_y = 490  # СТАРТОВАЯ ТОЧКА ЛАЗЕРА ПО Y (ИЗ НОСА МАШИНЫ)
    x = DISPLAY_WIDTH * 0.45
    y = DISPLAY_HEIGHT * 0.8
    x_change = 0

    things_start_x = random.randrange(2, DISPLAY_WIDTH - 70)  # минус ширина картинки
    things_start_y = -600
    thing_speed = 5
    thing_width = beetle.get_width()
    thing_height = beetle.get_height()

    pygame.mixer.music.load('music/music.ogg.mp3')
    pygame.mixer.music.play(-1)

    game_exit = False

    while not game_exit:

        gameDisplay.blit(background_image, [0, 0])
        for event in pygame.event.get():
            # НА СЛУЧАЙ НАЖАТИЯ КРЕСТИКА
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # ДВИЖЕНИЕ
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -10
                if event.key == pygame.K_d:
                    x_change = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
                # СТРЕЛЬБА ЧЕРЕЗ ПРОБЕЛ
                if event.key == pygame.K_SPACE:
                    if laser_int != 0:  # ЕСЛИ ЛАЗЕР УЖЕ ЗАПУЩЕН, ТО У НЕГО СТАТИЧЕСКИЙ Х
                        pass
                    else:
                        laser_int = x + 38  # СТРЕЛЬБА ИЗ СЕРЕДИНЫ ОБЬЕКТА

        # ДВИЖЕНИЕ С ПОМОЩЬЮ КЛАВИШ
        x += x_change

        # ОЧКИ ПОДБИТЫХ И ВООБЩЕ ВСЕХ
        point_count(dodge)
        aim(points)

        if laser_int != 0:  # ДВИЖЕНИЕ ЛАЗЕРА ПО ИГРИКУ
            laser(laser_int, laser_y, LASER_COL)
            laser_y -= 14
        if laser_y < 0 - LASER_HEIGHT:  # ОБНУЛЕНИЕ ЛАЗЕРА ПРИ ВЫХОДЕ ЗА ГРАНИЦЫ
            laser_int = 0
            laser_y = 490
        # things(thingx, thingy, thingw, thingh, color)

        things(beetle, things_start_x, things_start_y)  # СОЗДАНИЕ ЖУКА

        things_start_y += thing_speed  # ИЗМЕНЕНИЕ СКОРОСТИ
        thing_speed += 0.000001

        car(x, y)

        # ВРЕЗАНИЕ ЛАЗЕРА В ЖУКА
        if laser_y < things_start_y and laser_int != 0:  # ПРОВЕРКА ПО ОСИ Y
            if things_start_x <= laser_int <= things_start_x + 70:  # ПРОВЕРКА ГРАНИЦЫ ПО ОСИ Х
                dodge += 1
                things_start_y = 0 - thing_height - 10  # СОЗДАНИЕ ЖУКА (Y)
                things_start_x = random.randrange(0, DISPLAY_WIDTH - thing_width)  # СОЗДАНИЕ ЖУКА (Х)
                laser_y = 490  # ОБНУЛЕНИЕ ЛАЗЕРА ПО ОСИ У
                laser_int = 0  # ОБНУЛЕНИЕ ЛАЗЕРА ПО ОСИ Х
                points += 1  # КОЛИЧЕСТВО ПОДБИТЫХ +1

        # СТОЛКНОВЕНИЕ С ЖУКОМ ТАЧКИ
        if y <= things_start_y + thing_height - 25:  # -25, чтобы немного наложить жука на тачку
            if (
                    x + 10 < things_start_x < x + car_width - 10 or
                    x + 10 < things_start_x + thing_width < x + car_width - 10):
                crash(points)

        # СОЗДАНИЕ ЖУКА ПРИ ЕГО ВЫХОДЕ ЗА ГРАНИЦЫ
        if things_start_y >= DISPLAY_HEIGHT:
            things_start_y = 0 - thing_height - 10
            things_start_x = random.randrange(2, DISPLAY_WIDTH - thing_width - 1)
            dodge += 1

        # ВРЕЗАНИЕ В ГРАНИЦЫ
        if x >= DISPLAY_WIDTH - car_width - 1:
            x = DISPLAY_WIDTH - car_width - 4
        elif x < 0:
            x = 4

        pygame.display.update()
        clock.tick(60)


game_intro()
pygame.quit()
quit()

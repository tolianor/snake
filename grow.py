import pygame
import pygame_menu
import random
import sys
import top

pygame.init()

SIZE_BLOCK = 20
COUNT_BLOCKS = 20
MARGIN = 1

DISPLAY = (109, 235, 131)
WHITE = (212, 248, 218)
BLACK = (128, 128, 0)
MINT = (180, 235, 189)
HEADER_COLOR = (127, 255, 0)
TOP_BACK_COLOR = (192, 192, 192)
SNAKE_COLOR = (255, 69, 0)
YELLOW = (255, 215, 0)

WIDTH = SIZE_BLOCK * COUNT_BLOCKS + MARGIN * COUNT_BLOCKS + 2 * SIZE_BLOCK
HEADER_MARGIN = 70
HEIGHT = SIZE_BLOCK * COUNT_BLOCKS + MARGIN * COUNT_BLOCKS + HEADER_MARGIN + 2 * SIZE_BLOCK


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
a = pygame.image.load('screen.png')
pygame.display.set_icon(a)
clock = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)
courier1 = pygame.font.SysFont('courier', 18)


def draw_block(color, column, row):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def start_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 9), SnakeBlock(10, 9)]
    d_row = buf_row = 0
    d_col = buf_col = 1
    apple = get_random_empty_block()
    total = 0
    speed = 1

    while True:
        # Держим цикл на правильной скорости
        clock.tick(2 + speed)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                if event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                if event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                if event.key == pygame.K_ESCAPE:
                    get_menu()

        screen.fill(DISPLAY)

        pygame.draw.rect(screen, HEADER_COLOR, (0, 0, WIDTH, HEADER_MARGIN))

        text_total = courier.render(f'Total score: {total}', True, BLACK)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (column + row) % 2 == 0:
                    color = WHITE
                else:
                    color = MINT
                draw_block(color, column, row)

        draw_block(YELLOW, apple.x, apple.y)

        head = snake_blocks[-1]
        if not head.is_inside():
            for name in get_name().values():
                top.in_top(name, total)
            break

        # drawing snake
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()
        if apple == head:
            snake_blocks.append(apple)
            apple = get_random_empty_block()
            total += 1
            speed = total//5 + 1

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_col, head.y + d_row)

        if new_head in snake_blocks:
            for name in get_name().values():
                top.in_top(name, total)
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)


def top_players():
    while True:
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, TOP_BACK_COLOR, (100, 160, 250, 350))

        header_text = courier1.render("Топ игроков: ", True, BLACK)
        screen.blit(header_text, (120, 170))

        get_top = top.output_top()
        count = 1
        height_text_top = 200
        for one_in_top in get_top:
            text_total = courier1.render(f'{count}. {one_in_top[0]} - {one_in_top[1]} баллов', True, BLACK)
            screen.blit(text_total, (120, height_text_top))
            height_text_top += 20
            count += 1

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    get_menu()

        pygame.display.flip()


def get_name():
    return menu.get_input_data()


background = pygame.image.load('Background.jpg')

menu = pygame_menu.Menu(300, 400, '', theme=pygame_menu.themes.THEME_GREEN, menu_position=(50, 70))

menu.add_text_input('Имя: ', default='игрок')
menu.add_button('Играть', start_game)
menu.add_button('топ', top_players)
menu.add_button('Выход', pygame_menu.events.EXIT)


def get_menu():
    while True:

        screen.blit(background, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()


get_menu()

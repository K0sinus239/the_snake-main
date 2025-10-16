"""Игра 'Змейка'. Автор: Константин Белов, 125 когорта"""
from random import randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """
    Класс для представления игрового объекта.

    Атрибуты:
    ----------
    position
        Координаты объекта.
    body_color
        Цвет объекта.

    Методы:
    --------
    def draw(self):
        Отрисовка объекта.
    """

    def __init__(self, body_color=None) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта."""
        return NotImplementedError(
            "Потомок должен реализовать родительский класс draw")

    def draw_rect(self, position):
        """Отрисовка прямоугольника."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс для представления яблочка.
    Наследуется от класса GameObject.
    """

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.new_position = None

    def randomize_position(self, snake):
        """Размещение в случайном месте игрового поля."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake.positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблочка."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """
    Класс для представления змейки.
    Наследуется от класса GameObject.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.last = None

    def reset(self):
        """Сброс змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        pg.display.update()

    def update_direction(self):
        """Обновление направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop() if len(self.positions) > self.length
            else None
        )

    def get_head_position(self):
        """Вернуть положение головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions:
            self.draw_rect(position)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Событие: нажатие кнопки направления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный модуль."""
    pg.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            return
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

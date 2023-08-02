import pygame as pg
import pygame.gfxdraw as gfx
import sys

from entyties import *
from settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.event.clear()
        pg.event.set_blocked(None)
        pg.event.set_allowed(pg.KEYDOWN)

        self.sc = pg.display.set_mode(SCREEN, flags=pg.NOFRAME)
        self.clock = pg.time.Clock()

        self.font = pg.font.SysFont('calibri', 24)

        self.score = 0
        self.max_score = 0

        self.new_game()

    def new_game(self):
        self.snake = Snake(self)
        self.apple = Apple(self)

        self.score = 0
        self.running = True

    def update_score(self):
        self.score = self.snake.lenght - 1
        self.max_score = max(self.max_score, self.score)

    def new_apple(self):
        new_apple = Apple(self)
        while new_apple in self.snake.body:
            new_apple = Apple(self)
        self.apple = new_apple
        self.update_score()

    def handle_events(self):
        for event in pg.event.get():
            if event.key == pg.K_ESCAPE:
                self.running = False
            self.snake.control(event)

    def update(self):
        self.clock.tick(FPS)
        self.snake.update()
        # pg.display.set_caption(f'{self.clock.get_fps() : .0f}')

    def draw(self):
        self.sc.fill(BG)
        # grid
        [gfx.vline(self.sc, x, 0, HEIGHT, GRAY) for x in range(0, WIDTH, TILE)]
        [gfx.hline(self.sc, 0, WIDTH, y, GRAY) for y in range(0, HEIGHT, TILE)]

        self.apple.draw()
        self.snake.draw()

        text = f'Score: {self.score}   Record: {self.max_score}'
        render = self.font.render(text, True, 'orange')
        self.sc.blit(render, (1, 1))

        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()

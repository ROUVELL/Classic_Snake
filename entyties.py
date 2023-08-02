import pygame as pg
from random import randint, random

from settings import *


def get_random_rect() -> pg.Rect:
    x = randint(0, FIELD_W - 1) * TILE + 1
    y = randint(0, FIELD_H - 1) * TILE + 1
    return pg.Rect(x, y, TILE - 1, TILE - 1)


class Apple:
    def __init__(self, game):
        self.sc = game.sc
        self.rect = get_random_rect()

    def draw(self):
        pg.draw.rect(self.sc, RED, self.rect)


class Snake:
    def __init__(self, game):
        self.game = game

        self.rect = get_random_rect()
        self.body = []
        self.lenght = 1
        self.direction = pg.Vector2()
        self.directions = {'left': True, 'right': True, 'up': True, 'down': True}
        self.last_move = 0

    def can_move(self):
        now = pg.time.get_ticks()
        if now - self.last_move >= MOVE_TIME:
            self.last_move = now
            return True
        return False

    def movement(self):
        if self.can_move():
            self.check_collision()

    def check_collision(self):
        if self.rect.centerx < 0 or self.rect.centerx > WIDTH:
            return self.game.new_game()
        if self.rect.centery < 0 or self.rect.centery > HEIGHT:
            return self.game.new_game()

        # check selfeating
        if len(self.body) != len(set(seg.center for seg in self.body)):
            self.game.new_game()

        if self.rect.center == self.game.apple.rect.center:
            self.lenght += 1
            self.game.new_apple()

    def control(self, event: pg.event.Event):
        match event.key:
            case pg.K_w:
                if self.directions['up']:
                    self.directions = {'left': True, 'right': True, 'up': True, 'down': False}
                    self.direction = pg.Vector2(0, -TILE)
            case pg.K_s:
                if self.directions['down']:
                    self.directions = {'left': True, 'right': True, 'up': False, 'down': True}
                    self.direction = pg.Vector2(0, TILE)
            case pg.K_a:
                if self.directions['left']:
                    self.directions = {'left': True, 'right': False, 'up': True, 'down': True}
                    self.direction = pg.Vector2(-TILE, 0)
            case pg.K_d:
                if self.directions['right']:
                    self.directions = {'left': False, 'right': True, 'up': True, 'down': True}
                    self.direction = pg.Vector2(TILE, 0)

    def update(self):
        if self.can_move():
            self.check_collision()
            self.body.append(self.rect.copy())
            self.rect.move_ip(self.direction)
            self.body = self.body[-self.lenght:]

    def draw(self):
        [pg.draw.rect(self.game.sc, GREEN, seg) for seg in self.body]

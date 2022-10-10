import pygame
from Square import *


def color(c):
    colors = {"BLACK": (0, 0, 0),
              "WHITE": (255, 255, 255),
              "GREY": (127, 127, 127),
              "GREEN": (0, 255, 0),
              "RED": (255, 0, 0),
              "BLUE": (0, 0, 255),
              "YELLOW": (255, 185, 15),
              "BEIGE": (255, 250, 205),
              "LIME": (124, 252, 0)
              }
    return colors[c]


class Board:
    def __init__(self, height, width):
        self.board = []

        for h in range(height):
            self.board.append([])

        for i in range(height):
            for j in range(width):
                self.board[i].append(Square())
        pygame.init()
        size = pygame.display.Info()
        pygame.font.init()
        window_height = size.current_h
        window_width = size.current_w
        self.board_len = size.current_h
        print(window_height, window_width)
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
        self.screen.fill(color("WHITE"))
        self.block_height = self.board_len // height
        self.block_width = self.board_len // width
        self.board_height = height
        self.board_width = width
        self.window_height = window_height
        self.window_width = window_width

        bomb = pygame.image.load('img/bomb.png').convert()
        self.bomb_png = pygame.transform.scale(bomb, (self.block_width, self.block_height))

        other_bomb = pygame.image.load('img/other bomb.png').convert()
        self.other_bomb_png = pygame.transform.scale(other_bomb, (self.block_width, self.block_height))

        unreveal = pygame.image.load('img/unrevealed.png').convert()
        self.unrevealed_png = pygame.transform.scale(unreveal, (self.block_width, self.block_height))

        flag = pygame.image.load('img/flag.png').convert()
        self.flag_png = pygame.transform.scale(flag, (self.block_width, self.block_height))

        self.legend = pygame.font.SysFont('calibri', self.block_height // 2).render("Press R to reset!", True,
                                                                                    color("BLACK"))

        self.bombs = []

        self.non_bomb = 0
        self.cleared = 0

        for i in range(height):
            for j in range(width):
                curr = self.board[i][j]
                bombs = 0
                if curr.bomb:
                    self.bombs.append(curr)
                if not curr.bomb:
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            if i == k and j == l:
                                continue
                            if 0 <= k < height and 0 <= l < height:
                                if self.board[k][l].bomb:
                                    bombs += 1
                    curr.populate(bombs, self.block_height, self.block_width)
                    self.non_bomb += 1

        for i in range(height):
            for j in range(width):
                curr = self.board[i][j]
                ls = []
                if curr.number == 0:
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            if i == k and j == l:
                                continue
                            if 0 <= k < height and 0 <= l < height:
                                ls.append(self.board[k][l])
                    curr.link_zeros(ls)

    def printBoard(self):
        for r in self.board:
            str_ = "("
            for sq in r:
                str_ += sq.str() + ", "
            str_ += ")"
            print(str_)

    def draw_grid(self):
        for h in range(self.board_height):
            for w in range(self.board_width):
                curr = self.board[h][w]
                rect = self.draw_rect(h * self.block_height, w * self.block_width, color("BLACK"), color("GREY"))
                if curr.revealed:
                    if curr.bomb:
                        if curr.the_bomb:
                            self.screen.blit(self.bomb_png, self.bomb_png.get_rect(center=rect.center))
                        else:
                            self.screen.blit(self.other_bomb_png, self.bomb_png.get_rect(center=rect.center))
                    else:
                        self.screen.blit(curr.text, curr.text.get_rect(center=rect.center))
                else:
                    if curr.flagged:
                        self.screen.blit(self.flag_png, self.flag_png.get_rect(center=rect.center))
                    else:
                        self.screen.blit(self.unrevealed_png, self.unrevealed_png.get_rect(center=rect.center))

        legend = self.draw_rect(50, self.board_len + 200, color("WHITE"), color("WHITE"))
        self.screen.blit(self.legend, self.legend.get_rect(center=legend.center))

    def draw_rect(self, x, y, border_color, fill_color):
        screen = self.screen
        rect = pygame.Rect(y, x, self.block_width, self.block_height)
        screen.fill(fill_color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)
        return rect

    def game_over(self):
        for bomb in self.bombs:
            bomb.reveal(True)

    def reveal(self, x, y):
        return self.board[x][y].reveal()

    def flag_down(self, x, y):
        self.board[x][y].flag_down()

    def clear(self, num_cleared):
        self.cleared += num_cleared

    def win(self):
        return self.cleared == self.non_bomb

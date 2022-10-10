import random as rand
import pygame as pygame

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


class Square:
    def __init__(self):
        self.bomb = rand.random() < 0.2
        self.the_bomb = False
        self.number = 0
        self.text = None
        self.image = None
        self.ls_of_zero = None
        self.revealed = False
        self.flagged = False

    def str(self):
        if self.bomb:
            return "b"
        else:
            return str(self.number)

    def populate(self, bombs, block_height, block_width):
        pygame.font.init()
        self.number = bombs
        if bombs == 0:
            self.text = pygame.font.SysFont('calibri', block_height // 2).render("", True, color("BLACK"))
        else:
            self.text = pygame.font.SysFont('calibri', block_height // 2).render(str(bombs), True, color("BLACK"))

    def link_zeros(self, ls_of_square):
        if not self.revealed:
            self.ls_of_zero = ls_of_square

    def reveal(self, bombed: bool = False):
        if self.revealed:
            return 0
        if self.bomb:
            self.revealed = True
            if not bombed:
                self.the_bomb = True
            return -1
        if self.number == 0:
            self.revealed = True
            num_revealed = 1
            for sq in self.ls_of_zero:
                num_revealed += sq.reveal()
            return num_revealed

        self.revealed = True
        return 1

    def flag_down(self):
        self.flagged = True
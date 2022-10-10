import pygame
from pygame.locals import *
import random as rand
import sys as sys
from Board import *
from Square import *


def main():
    height = 20
    width = 20

    b = Board(height, width)

    pygame.init()
    pygame.font.init()

    game_over = False

    while True:
        b.draw_grid()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_r:
                    b = Board(height, width)
                    game_over = False
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                x = mouse_pos[0] // b.block_width
                y = mouse_pos[1] // b.block_height
                if x >= b.board_width or y >= b.board_height:
                    continue
                if button_pressed[0]:
                    reveal = b.reveal(y, x)
                    if reveal == -1:
                        b.game_over()
                        print("You Lose!")
                    else:
                        b.clear(reveal)
                        if b.win():
                            game_over = True
                            print("You Win!")
                elif button_pressed[2]:
                    b.flag_down(x, y)


if __name__ == "__main__":
    main()

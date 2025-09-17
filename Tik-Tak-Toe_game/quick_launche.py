import pygame
from game import *

token1 = "themes/tokens/classic1.png"
token2 = "themes/tokens/classic2.png"
game_background = "themes/background/classic-back.png"

if __name__ == '__main__' :
    pygame.init()
    grid_pos = []
    clock = pygame.time.Clock()
    src = pygame.display.set_mode()
    pygame.display.set_caption("Ultimate tic tac toe")
    game_state = game_state(src,token1,token2,game_background)
    game_state.server = True
    game_state.IP ="192.168.228.30"
    game_state.port = 2020
    victor = tic_tac_toe(game_state)
    print(victor)
    print("end")
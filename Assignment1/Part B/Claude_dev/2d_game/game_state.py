from enum import Enum

class GameState(Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3
    QUIT = 4
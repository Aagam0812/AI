import pygame
import sys
from game_state import GameState
from menu import Menu
from game import Game
from game_over import GameOver
from sound_manager import SoundManager
from high_score import HighScore

class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2D Pygame Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.sound_manager = SoundManager()
        self.high_score = HighScore()
        self.state = GameState.MENU
        self.menu = Menu(self.screen, self.font, self.sound_manager, self.high_score)
        self.game = Game(self.screen, self.font, self.sound_manager)
        self.game_over = GameOver(self.screen, self.font, self.high_score)

    def run(self):
        self.sound_manager.play_background_music()
        while True:
            if self.state == GameState.MENU:
                self.state = self.menu.run()
            elif self.state == GameState.GAME:
                self.state = self.game.run()
            elif self.state == GameState.GAME_OVER:
                self.state = self.game_over.run(self.game.score)
                if self.state == GameState.GAME:
                    self.game = Game(self.screen, self.font, self.sound_manager)
            elif self.state == GameState.QUIT:
                self.sound_manager.stop_background_music()
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = MainGame()
    game.run()
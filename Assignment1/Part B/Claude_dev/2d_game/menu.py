import pygame
from game_state import GameState
from high_score import HighScore

class Menu:
    def __init__(self, screen, font, sound_manager, high_score):
        self.screen = screen
        self.font = font
        self.sound_manager = sound_manager
        self.high_score = high_score
        self.options = ["Start Game", "Instructions", "High Scores", "Settings", "Exit"]
        self.selected = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Treasure Island Adventure", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (400 - text.get_width() // 2, 250 + i * 50))

    def show_instructions(self):
        self.screen.fill((0, 0, 0))
        instructions = [
            "Use arrow keys to move",
            "Collect yellow items",
            "Avoid red obstacles",
            "Reach the target score to advance levels",
            "",
            "Press any key to return to menu"
        ]
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (400 - text.get_width() // 2, 100 + i * 50))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    waiting = False
        return GameState.MENU

    def show_high_scores(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("High Scores", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, 50))

        high_scores = self.high_score.get_high_scores()
        if high_scores:
            for i, hs in enumerate(high_scores):
                score_text = self.font.render(f"{i+1}. {hs['name']}: {hs['score']}", True, (255, 255, 255))
                self.screen.blit(score_text, (400 - score_text.get_width() // 2, 100 + i * 40))
        else:
            no_scores = self.font.render("No high scores yet!", True, (255, 255, 255))
            self.screen.blit(no_scores, (400 - no_scores.get_width() // 2, 300))

        back_text = self.font.render("Press any key to return to menu", True, (255, 255, 255))
        self.screen.blit(back_text, (400 - back_text.get_width() // 2, 550))

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    waiting = False
        return GameState.MENU

    def show_settings(self):
        self.screen.fill((0, 0, 0))
        settings = [
            "Music: ON" if pygame.mixer.get_busy() else "Music: OFF",
            "Sound: ON" if self.sound_manager.sound_volume > 0 else "Sound: OFF",
            "",
            "Press M to toggle music",
            "Press S to toggle sound effects",
            "Press any other key to return to menu"
        ]
        for i, line in enumerate(settings):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (400 - text.get_width() // 2, 100 + i * 50))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.sound_manager.toggle_music()
                    elif event.key == pygame.K_s:
                        self.sound_manager.toggle_sound()
                    else:
                        waiting = False
        return GameState.MENU

    def run(self):
        self.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        return GameState.GAME
                    elif self.selected == 1:
                        return self.show_instructions()
                    elif self.selected == 2:
                        return self.show_high_scores()
                    elif self.selected == 3:
                        return self.show_settings()
                    elif self.selected == 4:
                        return GameState.QUIT
        return GameState.MENU
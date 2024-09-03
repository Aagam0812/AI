import pygame
from game_state import GameState

class GameOver:
    def __init__(self, screen, font, high_score):
        self.screen = screen
        self.font = font
        self.high_score = high_score

    def draw(self, score):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = self.font.render("Press SPACE to restart", True, (255, 255, 255))
        menu_text = self.font.render("Press ESC for main menu", True, (255, 255, 255))

        self.screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 100))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 200))
        self.screen.blit(restart_text, (400 - restart_text.get_width() // 2, 300))
        self.screen.blit(menu_text, (400 - menu_text.get_width() // 2, 350))

        high_scores = self.high_score.get_high_scores()
        if high_scores:
            high_score_text = self.font.render("High Scores:", True, (255, 255, 255))
            self.screen.blit(high_score_text, (50, 450))
            for i, hs in enumerate(high_scores[:5]):
                hs_text = self.font.render(f"{i+1}. {hs['name']}: {hs['score']}", True, (255, 255, 255))
                self.screen.blit(hs_text, (50, 500 + i * 30))

    def is_high_score(self, score):
        high_scores = self.high_score.get_high_scores()
        if len(high_scores) < 10:
            return True
        return score > min(hs['score'] for hs in high_scores)

    def run(self, score):
        if self.is_high_score(score):
            name = self.get_player_name(score)
            self.high_score.add_score(name, score)

        waiting = True
        while waiting:
            self.draw(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return GameState.GAME
                    elif event.key == pygame.K_ESCAPE:
                        return GameState.MENU
            pygame.display.flip()
        return GameState.GAME_OVER

    def get_player_name(self, score):
        name = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
            self.screen.fill((0, 0, 0))
            name_prompt = self.font.render("New High Score! Enter your name:", True, (255, 255, 255))
            name_text = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(name_prompt, (400 - name_prompt.get_width() // 2, 250))
            self.screen.blit(name_text, (400 - name_text.get_width() // 2, 300))
            pygame.display.flip()
        return name
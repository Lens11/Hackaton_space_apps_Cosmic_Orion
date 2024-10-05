import pygame
import utils


class MCQGame(utils.Game):
    def __init__(self, screen, menu, game_key, level):
        super().__init__()
        self.screen = screen
        self.menu = menu
        self.game_key = game_key
        self.level = level
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.background = utils.AssetManager.load_image('background.png', 'menu', self.screen.get_width(), self.screen.get_height())

    def load_questions(self):
        # This method should load questions based on game_key and level
        # For now, we'll use a placeholder set of questions
        return [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            },
            {
                "question": "What color is the sky?",
                "options": ["Red", "Green", "Blue", "Yellow"],
                "correct": 2
            }
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    self.check_answer(event.key - pygame.K_1)
        return True

    def check_answer(self, answer):
        if answer == self.questions[self.current_question]["correct"]:
            self.score += 1
        self.current_question += 1
        if self.current_question >= len(self.questions):
            return self.end_game()

    def end_game(self):
        if self.score >= len(self.questions) * 0.7:  # 70% correct to pass
            self.menu.unlock_next_level(self.game_key)
            return "win"
        else:
            return "lose"

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.draw_text(question["question"], self.screen.get_width() // 2, 100)
            for i, option in enumerate(question["options"]):
                self.draw_text(f"{i+1}. {option}", self.screen.get_width() // 2, 200 + i * 50)
        else:
            self.draw_text(f"Game Over. Your score: {self.score}/{len(self.questions)}", self.screen.get_width() // 2, self.screen.get_height() // 2)
        pygame.display.flip()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            result = self.handle_events()
            if result == "quit":
                return "quit"
            self.draw()
            self.clock.tick(60)
            if self.current_question >= len(self.questions):
                return self.end_game()
        return "menu"
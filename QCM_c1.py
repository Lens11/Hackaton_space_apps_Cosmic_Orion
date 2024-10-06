import pygame
import random
import utils

class QCMGame(utils.Game):
    def __init__(self, screen, questions, correct_answers):
        super().__init__()
        self.screen = screen
        self.questions = questions
        self.correct_answers = correct_answers
        self.current_question = 0
        self.score = 0
        self.user_choice = None
        self.feedback_message = None
        self.feedback_time = 0
        self.game_over = False
        
        # Load background image
        self.background = utils.AssetManager.load_image('background.jpg', 'menu', utils.WIDTH, utils.HEIGHT)
        
        # Initialize fonts
        self.question_font = pygame.font.SysFont("Lucida Console", int(utils.HEIGHT * 0.035))
        self.option_font = pygame.font.SysFont("Lucida Console", int(utils.HEIGHT * 0.025))
        self.feedback_font = pygame.font.SysFont("Lucida Console", int(utils.HEIGHT * 0.025))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    self.user_choice = str(event.key - pygame.K_0)
                    self.check_answer()
        return True

    def update(self):
        current_time = pygame.time.get_ticks()
        if (self.feedback_message == "Very good!" and 
            current_time - self.feedback_time > 1000):
            self.next_question()

        if self.is_finished():
            self.game_over = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if not self.game_over:
            self.display_question()
        else:
            self.display_final_score()
        
        pygame.display.flip()

    def display_question(self):
        question_text, options = self.questions[self.current_question]
        self.draw_text_simple(question_text, self.question_font, utils.WHITE, 
                              utils.WIDTH // 2, utils.HEIGHT * 0.2)

        option_spacing = utils.HEIGHT * 0.1
        start_y = utils.HEIGHT * 0.4

        for i, option in enumerate(options):
            self.draw_text_bubble(f"{i + 1}. {option}", self.option_font, utils.WHITE,
                                  utils.WIDTH // 2, start_y + i * option_spacing)

        if self.feedback_message:
            color = utils.GREEN if self.feedback_message == "Very good!" else utils.RED
            self.draw_text_simple(self.feedback_message, self.feedback_font, color,
                                  utils.WIDTH // 2, utils.HEIGHT * 0.85)

        self.draw_text_simple("Type the number of the correct answer on your keyboard.",
                              self.option_font, utils.YELLOW,
                              utils.WIDTH // 2, utils.HEIGHT * 0.95)

    def display_final_score(self):
        final_score_text = f"Final Score: {self.score}/{len(self.questions)}"
        self.draw_text_simple(final_score_text, self.question_font, utils.WHITE,
                              utils.WIDTH // 2, utils.HEIGHT // 2)

    def check_answer(self):
        if self.user_choice == self.correct_answers[self.current_question]:
            self.score += 1
            self.feedback_message = "Very good!"
        else:
            self.feedback_message = "Wrong answer! Try again."
        self.feedback_time = pygame.time.get_ticks()

    def next_question(self):
        self.current_question += 1
        self.user_choice = None
        self.feedback_message = None

    def is_finished(self):
        return self.current_question >= len(self.questions)

    def draw_text_simple(self, text, font, color, x, y):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            test_text = ' '.join(current_line)
            if font.size(test_text)[0] > utils.WIDTH * 0.8:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        line_height = font.get_height()
        total_height = line_height * len(lines)
        current_y = y - (total_height / 2)
        
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(x, current_y))
            self.screen.blit(text_surface, text_rect)
            current_y += line_height

    def draw_text_bubble(self, text, font, color, x, y):
        padding = int(utils.WIDTH * 0.015)
        text_surface = font.render(text, True, color)
        bubble_surface = pygame.Surface((text_surface.get_width() + padding * 2, 
                                         text_surface.get_height() + padding * 2), 
                                         pygame.SRCALPHA)
        pygame.draw.rect(bubble_surface, (255, 255, 255, 40), 
                         bubble_surface.get_rect(), 
                         border_radius=int(padding/2))
        bubble_surface.blit(text_surface, (padding, padding))
        text_rect = bubble_surface.get_rect(center=(x, y))
        self.screen.blit(bubble_surface, text_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(utils.FPS)
            if self.score == len(self.questions):
                return "ok"

        return "ok" if self.score == len(self.questions) else "game_over"
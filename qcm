import pygame
import sys

# Initialiser pygame
pygame.init()

# Obtenir la résolution de l'écran
info = pygame.display.Info()
# Définir la taille de la fenêtre à 80% de la résolution de l'écran
#WIDTH = int(info.current_w * 0.8)
#HEIGHT = int(info.current_h * 0.8)
WIDTH = 800
HEIGHT = 600

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60

# Calculer les tailles de police en fonction de la hauteur de la fenêtre
QUESTION_FONT_SIZE = int(HEIGHT * 0.035)  # Réduit pour mieux s'adapter
OPTION_FONT_SIZE = int(HEIGHT * 0.025)    # Réduit pour mieux s'adapter
FEEDBACK_FONT_SIZE = int(HEIGHT * 0.025)   # Même taille que les options

# Charger l'image de fond
background_image = pygame.image.load(r"C:\Users\Picard\Desktop\espace.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Configurer l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de QCM - Thème de l'espace")

# Initialiser les différentes polices
question_font = pygame.font.SysFont("Lucida Console", QUESTION_FONT_SIZE)
option_font = pygame.font.SysFont("Lucida Console", OPTION_FONT_SIZE)
feedback_font = pygame.font.SysFont("Lucida Console", FEEDBACK_FONT_SIZE)

def create_text_bubble(text, font, color, padding=20):
    # Ajuster le padding en fonction de la taille de l'écran
    padding = int(WIDTH * 0.015)  # Padding proportionnel à la largeur
    text_surface = font.render(text, True, color)
    bubble_surface = pygame.Surface((text_surface.get_width() + padding * 2, 
                                   text_surface.get_height() + padding * 2), 
                                   pygame.SRCALPHA)
    pygame.draw.rect(bubble_surface, (255, 255, 255, 40), 
                    bubble_surface.get_rect(), 
                    border_radius=int(padding/2))
    bubble_surface.blit(text_surface, (padding, padding))
    return bubble_surface

def draw_text_simple(text, font, color, surface, x, y):
    # Fonction pour wrapper le texte si nécessaire
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_text = ' '.join(current_line)
        if font.size(test_text)[0] > WIDTH * 0.8:  # Si la ligne est trop longue
            current_line.pop()  # Retirer le dernier mot
            if current_line:  # Si la ligne n'est pas vide
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:  # Ajouter la dernière ligne
        lines.append(' '.join(current_line))
    
    # Afficher chaque ligne
    line_height = font.get_height()
    total_height = line_height * len(lines)
    current_y = y - (total_height / 2)
    
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(x, current_y))
        surface.blit(text_surface, text_rect)
        current_y += line_height

def draw_text_bubble(text, font, color, surface, x, y):
    text_bubble = create_text_bubble(text, font, color)
    text_rect = text_bubble.get_rect(center=(x, y))
    surface.blit(text_bubble, text_rect)

class QCMGame:
    def __init__(self, questions, correct_answers):
        self.questions = questions
        self.correct_answers = correct_answers
        self.current_question = 0
        self.score = 0
        self.user_choice = None
        self.feedback_message = None
        self.feedback_time = 0

    def display_question(self):
        screen.blit(background_image, (0, 0))
        
        # Affiche la question
        question_text, options = self.questions[self.current_question]
        draw_text_simple(question_text, question_font, WHITE, screen, 
                        WIDTH // 2, HEIGHT * 0.2)  # Déplacé plus haut

        # Calcul de l'espacement vertical entre les options
        option_spacing = HEIGHT * 0.1  # 10% de la hauteur de l'écran
        start_y = HEIGHT * 0.4  # Commence à 40% de la hauteur

        # Affiche les options
        for i, option in enumerate(options):
            draw_text_bubble(f"{i + 1}. {option}", option_font, WHITE, screen,
                           WIDTH // 2, start_y + i * option_spacing)

        # Affiche le feedback
        if self.feedback_message:
            color = GREEN if self.feedback_message == "Very good!" else RED
            draw_text_simple(self.feedback_message, feedback_font, color, screen,
                           WIDTH // 2, HEIGHT * 0.85)

        # Affiche la consigne
        draw_text_simple("Type the number of the correct answer on your keyboard.",
                        option_font, YELLOW, screen,
                        WIDTH // 2, HEIGHT * 0.95)

        pygame.display.flip()

    def check_answer(self):
        if self.user_choice == self.correct_answers[self.current_question]:
            self.score += 1
            self.feedback_message = "Very good!"
            self.feedback_time = pygame.time.get_ticks()
        else:
            self.feedback_message = "Wrong answer! Try again."

    def next_question(self):
        current_time = pygame.time.get_ticks()
        if (self.feedback_message == "Very good!" and 
            current_time - self.feedback_time > 1000):
            self.current_question += 1
            self.user_choice = None
            self.feedback_message = None

    def is_finished(self):
        return self.current_question >= len(self.questions)

# Fonction principale
def main():
    clock = pygame.time.Clock()

    # Différents ensembles de questions et réponses: c'est là où je vais créer les QCM!!!
# Fonction principale
def main():
    clock = pygame.time.Clock()

    # Différents ensembles de questions et réponses
    # QCM pour Gas Giant
    qcm_1_gasgiant = [
        ("What are gas giants primarily composed of?", ["Rock and ice", "Hydrogen and helium", "Metal and dust", "Water and carbon dioxide"]),
    ]
    correct_answers_gasgiant_1 = ["2"]  # B) Hydrogen and helium

    qcm_2_gasgiant = [
        ("Which two planets in our solar system are gas giants?", ["Earth and Mars", "Jupiter and Neptune", "Jupiter and Saturn", "Venus and Uranus"]),
        ("What is a hot Jupiter?", ["A gas giant that is far from its star", "A small, rocky planet close to its star", "A gas giant orbiting close to its star, making it extremely hot", "A gas giant with a solid surface"]),
    ]
    correct_answers_gasgiant_2 = ["3", "3"]  # C) Jupiter and Saturn, C) A gas giant orbiting close to its star

    qcm_3_gasgiant = [
        ("How many exoplanets have scientists discovered in the last 25 years?", ["Over 500", "Over 5,600", "Over 56,000", "Over 100"]),
        ("What is the name of the youngest hot Jupiter ever found?", ["HD 209458 b", "HIP 67522 b", "Kepler-22b", "WASP-12b"]),
        ("How long does it take HIP 67522 b to orbit its star?", ["365 days", "7 days", "30 days", "90 days"]),
    ]
    correct_answers_gasgiant_3 = ["2", "2", "2"]  # B) Over 5,600, B) HIP 67522 b, B) 7 days

    # QCM pour Neptunian Planet
    qcm_1_neptunian = [
        ("What type of atmosphere do Neptunian planets typically have?", ["Oxygen-rich atmosphere", "Hydrogen and helium-dominated atmosphere", "Carbon dioxide-rich atmosphere", "Sulfur-rich atmosphere"]),
    ]
    correct_answers_neptunian_1 = ["2"]  # B) Hydrogen and helium-dominated atmosphere

    qcm_2_neptunian = [
        ("What are mini-Neptunes?", ["Planets larger than Neptune", "Planets smaller than Neptune and bigger than Earth", "Gas giants with rocky surfaces", "Rocky planets with liquid water"]),
        ("Which two planets in our solar system are considered ice giants?", ["Earth and Mars", "Saturn and Jupiter", "Uranus and Neptune", "Mercury and Venus"]),
    ]
    correct_answers_neptunian_2 = ["2", "3"]  # B) Planets smaller than Neptune, C) Uranus and Neptune

    qcm_3_neptunian = [
        ("How much larger is Neptune compared to Earth?", ["Two times the size", "Four times the size", "Six times the size", "Eight times the size"]),
        ("What chemicals are commonly found in the atmospheres of Uranus and Neptune?", ["Hydrogen and oxygen", "Water, ammonia, and methane", "Carbon dioxide and nitrogen", "Helium and sulfur"]),
        ("How far away was the ice giant exoplanet discovered in 2014?", ["1,000 light-years", "10,000 light-years", "25,000 light-years", "100,000 light-years"]),
    ]
    correct_answers_neptunian_3 = ["2", "2", "3"]  # B) Four times the size, B) Water, ammonia, and methane, C) 25,000 light-years

    # QCM pour Terrestrial Planet
    qcm_1_terrestrial = [
        ("What are terrestrial planets primarily composed of?", ["Gas and ice", "Rock, silicate, water, and/or carbon", "Hydrogen and helium", "Metal and dust"]),
    ]
    correct_answers_terrestrial_1 = ["2"]  # B) Rock, silicate, water, and/or carbon

    qcm_2_terrestrial = [
        ("How many terrestrial planets are estimated to exist in the Milky Way galaxy?", ["1 billion", "5 billion", "10 billion", "20 billion"]),
        ("What are super-Earths?", ["Terrestrial exoplanets larger than Earth", "Gas giants", "Planets with no solid surface", "Exoplanets smaller than Earth"]),
    ]
    correct_answers_terrestrial_2 = ["3", "1"]  # C) 10 billion, A) Terrestrial exoplanets larger than Earth

    qcm_3_terrestrial = [
        ("How far away is the TRAPPIST-1 system from Earth?", ["10 light-years", "20 light-years", "30 light-years", "40 light-years"]),
        ("What unique feature do binary star systems provide for terrestrial planets?", ["Increased gravity", "Harmful radiation", "Reduced harmful radiation levels", "Smaller orbits"]),
        ("What is Kepler-11 b known for?", ["Being the largest terrestrial planet", "Orbiting its star very closely", "Having a solid surface", "Being part of a binary star system"]),
    ]
    correct_answers_terrestrial_3 = ["4", "3", "2"]  # D) 40 light-years, C) Reduced harmful radiation levels, B) Orbiting its star very closely

    # QCM pour Super Earth
    qcm_1_super_earth = [
        ("What is the mass range of super-Earths compared to Earth?", ["Less than Earth's mass", "1 to 2 times the mass of Earth", "2 to 10 times the mass of Earth", "More than 10 times the mass of Earth"]),
    ]
    correct_answers_super_earth_1 = ["3"]  # C) 2 to 10 times the mass of Earth

    qcm_2_super_earth = [
        ("What defines a super-Earth in terms of its mass?", ["Larger than Earth's but smaller than gas giants", "Smaller than Earth", "Equal to Earth's mass", "Larger than gas giants like Uranus and Neptune"]),
        ("What types of materials can super-Earths be composed of?", ["Only gas", "Only rock", "Gas, rock, or a combination of both", "Liquid metals"]),
    ]
    correct_answers_super_earth_2 = ["1", "3"]  # A) Larger than Earth's but smaller than gas giants, C) Gas, rock, or a combination of both

    qcm_3_super_earth = [
        ("What makes super-Earths particularly interesting to scientists?", ["They are the most massive exoplanets known", "They offer a glimpse into the diversity of planetary systems beyond our own", "They have solid surfaces only", "They have atmospheres similar to Earth"]),
        ("How does the mass of super-Earths compare to ice giants like Uranus and Neptune?", ["Heavier than ice giants", "Lighter than ice giants", "The same mass as ice giants", "None of the above"]),
        ("In addition to their mass, what characteristic is commonly studied in super-Earths?", ["Their proximity to Earth", "Their composition and atmosphere", "Their orbital speed", "Their rotation period"]),
    ]
    correct_answers_super_earth_3 = ["2", "2", "2"]  # B) They offer a glimpse into the diversity of planetary systems beyond our own, B) Lighter than ice giants, B) Their composition and atmosphere

    # ---- CHOIX DU QCM ----
    # Ici, tu peux choisir quel QCM lancer (choisir quel QCM lancer)
    #game = QCMGame(qcm_1_gasgiant, correct_answers_gasgiant_1)  
    #game = QCMGame(qcm_2_gasgiant, correct_answers_gasgiant_2)  # Different sets of questions and answers 
    #game = QCMGame(qcm_3_gasgiant, correct_answers_gasgiant_3)  # Different sets of questions and answers 

    # Quiz for Neptunian Planet
    #game = QCMGame(qcm_1_neptunian, correct_answers_neptunian_1)  # Different sets of questions and answers 
    #game = QCMGame(qcm_2_neptunian, correct_answers_neptunian_2)  # Different sets of questions and answers 
    #game = QCMGame(qcm_3_neptunian, correct_answers_neptunian_3)  # Different sets of questions and answers 

    # Quiz for Terrestrial Planet
    #game = QCMGame(qcm_1_terrestrial, correct_answers_terrestrial_1)  # Different sets of questions and answers 
    #game = QCMGame(qcm_2_terrestrial, correct_answers_terrestrial_2)  # Different sets of questions and answers 
    #game = QCMGame(qcm_3_terrestrial, correct_answers_terrestrial_3)  # Different sets of questions and answers 

    # Quiz for Super Earth
    #game = QCMGame(qcm_1_super_earth, correct_answers_super_earth_1)  # Different sets of questions and answers 
    #game = QCMGame(qcm_2_super_earth, correct_answers_super_earth_2)  # Different sets of questions and answers 
    game = QCMGame(qcm_3_super_earth, correct_answers_super_earth_3)  # Different sets of questions and answers 

    # Boucle de jeu pour le QCM sélectionné
    running = True
    while running:
        game.display_question()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game.user_choice = "1"
                elif event.key == pygame.K_2:
                    game.user_choice = "2"
                elif event.key == pygame.K_3:
                    game.user_choice = "3"
                elif event.key == pygame.K_4:
                    game.user_choice = "4"

                if game.user_choice:
                    game.check_answer()

        # Si la réponse est correcte, passer à la question suivante après une courte pause
        game.next_question()

        # Vérifier si le QCM est terminé
        if game.is_finished():
            print(f"QCM terminé ! Score final : {game.score}/{len(game.questions)}")
            running = False

        clock.tick(FPS)

if __name__ == "__main__":
    main()

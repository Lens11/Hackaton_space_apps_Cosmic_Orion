# EXOEXPLORER 🌌

## Overview
**EXOEXPLORER** is an interactive and educational game built entirely in Python. This project was created for the NASA Space Apps Hackathon 2024 in collaboration with several national space agencies. It combines learning and entertainment to make space exploration exciting and accessible to children and teenagers. Players embark on a cosmic journey, exploring exoplanets, completing mini-games, and reinforcing their knowledge through quizzes.

![Capture d'écran 2024-10-06 123227](https://github.com/user-attachments/assets/78f9e4aa-ecfd-46ff-bf77-dc5b689f0cb5)

## Features
- **Interactive Gameplay** 🎮: Engage with different levels that explore exoplanets through mini-games and quizzes.
- **Educational Content** 🧠: Learn about exoplanets with fun facts and answer quizzes to advance through the levels.
- **Multiple Difficulty Levels**: Each game comes with increasing levels of difficulty to keep players challenged.
- **Unlockable Content**: Players unlock new planets, information, and quizzes as they progress through the game.

## Game Mechanics
1. **Learn**: Players are introduced to exoplanets through engaging visual content and facts.
2. **Play**: Each level features a mini-game where players complete space missions.
3. **Quiz**: After completing the game, players must pass a multiple-choice quiz (MCQ) to unlock the next level.

![Capture d'écran 2024-10-06 123351](https://github.com/user-attachments/assets/7d959515-636d-43be-9894-c38cc539c771)

## Installation

To play EXOEXPLORER locally, follow these steps:

### Requirements
- Python 3.7+
- Pygame (install via `pip`)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EXOEXPLORER.git
    ```
2. Navigate to the project directory:
    ```bash
    cd EXOEXPLORER
    ```
3. Install the required dependencies:
    ```bash
    pip install pygame
    ```
4. Run the game:
    ```bash
    python main.py
    ```

## Gameplay Example
In **EXOEXPLORER**, you’ll start by learning about a specific exoplanet like the *51 Pegasi B* or *KELT-9B*, then proceed to play a mini-game where you engage in space missions. After completing the mission, you’ll answer a series of quiz questions, such as:

> *What are gas giants primarily composed of?*

Answer correctly, and you unlock the next level!

## Code Structure
- `main.py`: The main game loop, menu, and level progression logic.
- `space_shooter_c1.py`, `ground_fighter_c1.py`: Implementations of different mini-games.
- `image_display_c1.py`, `image_display_action_c1.py`: Modules for displaying exoplanet information and game graphics.
- `QCM_c1.py`: Handles the quiz (MCQ) functionality after each level.
- `utils.py`: Asset management and utility functions.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Made with 💫 during NASA Space Apps Hackathon 2024

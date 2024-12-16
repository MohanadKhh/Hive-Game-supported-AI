#utils_show difficulty options file
import pygame
from utils.draw_button import draw_button
from utils.constants import *

def show_difficulty_options(screen, button_font):
    screen.fill(WHITE)
    difficulty_font = pygame.font.Font(None, 48)
    difficulty_title = difficulty_font.render("Choose Difficulty", True, BLACK)
    screen.blit(difficulty_title, ((WIDTH - difficulty_title.get_width()) // 2, 50))

    difficulties = [
        "Easy",
        "Medium",
        "Hard"
    ]

    y_offset = 150
    buttons = []
    for difficulty in difficulties:
        button = draw_button(screen, difficulty, (WIDTH - button_width) // 2, y_offset, False, button_font)
        buttons.append((button, difficulty))
        y_offset += button_height + button_spacing

    back_button = draw_button(screen, "Back", WIDTH - 350, HEIGHT - 100, False, button_font)
    return buttons, back_button

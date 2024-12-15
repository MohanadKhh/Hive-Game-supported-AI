#Utils_show game options file
import pygame
from utils.draw_button import draw_button
from utils.constants import *

def show_game_options(screen, button_font):
    screen.fill(WHITE)
    options_font = pygame.font.Font(None, 48)
    options_title = options_font.render("Options", True, BLACK)
    screen.blit(options_title, ((WIDTH - options_title.get_width()) // 2, 50))

    options = [
        "Player VS Player",
        "Player VS Computer",
        "Computer VS Computer"
    ]

    y_offset = 150
    buttons = []
    for option in options:
        button = draw_button(screen, option, (WIDTH - button_width) // 2, y_offset, False, button_font)
        buttons.append((button, option))
        y_offset += button_height + button_spacing

    back_button = draw_button(screen, "Back", WIDTH - 350, HEIGHT - 100, False, button_font)
    return buttons, back_button
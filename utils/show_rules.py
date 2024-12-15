#Utils_show rules file
import pygame
from utils.draw_button import draw_button
from utils.constants import *

def show_rules(screen, button_font):
    screen.fill(WHITE)
    rules_font = pygame.font.Font(None, 28)
    rules = [
        "~Gameplay:",
        " Each player selects a color (Black or White).",
        " Players take turns placing their first piece. The first piece must touch the opponent's piece.",
        " On your turn, you can either:",
        "  -Place a new piece from your collection.",
        "  -Move an existing piece already on the board (after placing your Queen Bee).",
        "",
        "~Game Pieces:",
        " -Queen Bee: Must be placed by your fourth turn.",
        " -Ant: Moves any number of spaces.",
        " -Grasshopper: Jumps over adjacent pieces.",
        " -Beetle: Moves one space and can climb on top of other pieces.",
        " -Spider: Moves exactly three spaces.",
        "",
        "~Movement Rules:",
        " New pieces must touch only your own pieces when placed, except for the first piece.",
        " You cannot move a piece that would split the hive into two separate groups.",
        " Once placed, a piece cannot be removed from the board.",
        "",
        "~Winning the Game:",
        " The game ends when one player completely surrounds the opponent's Queen Bee with their pieces."
    ]

    y_offset = 50
    for line in rules:
        text_surface = rules_font.render(line, True, BLACK)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30

    back_button = draw_button(screen, "Back", WIDTH - 350, HEIGHT - 100, False, button_font)
    return back_button
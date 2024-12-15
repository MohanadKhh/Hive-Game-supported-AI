#Utils_show exit dialog file
import pygame
from utils.draw_button import draw_button
from utils.constants import *

def show_exit_dialog(screen, button_font):
    dialog_width, dialog_height = 800, 200
    dialog_rect = pygame.Rect((WIDTH - dialog_width) // 2, (HEIGHT - dialog_height) // 2, dialog_width, dialog_height)
    pygame.draw.rect(screen, WHITE, dialog_rect)
    pygame.draw.rect(screen, BLACK, dialog_rect, 2)

    dialog_font = pygame.font.Font(None, 36)
    text_surface = dialog_font.render("Are you sure you want to exit?", True, BLACK)
    text_rect = text_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 50))
    screen.blit(text_surface, text_rect)

    yes_button = draw_button(screen, "Yes", dialog_rect.x + 50, dialog_rect.y + 100, False, button_font)
    no_button = draw_button(screen, "No", dialog_rect.x + dialog_width - 50 - button_width, dialog_rect.y + 100, False, button_font)

    return yes_button, no_button
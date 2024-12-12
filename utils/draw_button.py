import pygame
from utils.constants import *

def draw_button(screen, text, x, y, is_hovered, button_font):
    button_rect = pygame.Rect(x, y, button_width, button_height)
    button_color = RED if is_hovered else BLACK
    pygame.draw.rect(screen, button_color, button_rect)
    text_surface = button_font.render(text, True, back_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect
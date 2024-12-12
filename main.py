# import sys
# from utils.constants import *
# from utils.draw_button import draw_button
# from utils.show_exit_dialog import show_exit_dialog
# from utils.show_rules import show_rules
# from utils.show_game_options import show_game_options
# 
# 
# # Initialize Pygame
# pygame.init()
# 
# 
# pygame.display.set_caption("Hive Game")
# 
# # Load logo image
# logo_image = pygame.image.load("assets/logo.png")  # Update with your logo path
# logo_image = pygame.transform.scale(logo_image, (450, 450))  # Scale the image if needed
# 
# 
# 
# # def draw_button(text, x, y, is_hovered):
# #     button_rect = pygame.Rect(x, y, button_width, button_height)
# #     button_color = RED if is_hovered else BLACK
# #     pygame.draw.rect(screen, button_color, button_rect)
# #     text_surface = button_font.render(text, True, back_color)
# #     text_rect = text_surface.get_rect(center=button_rect.center)
# #     screen.blit(text_surface, text_rect)
# #     return button_rect
# 
# # def show_exit_dialog():
# #     dialog_width, dialog_height = 800, 200
# #     dialog_rect = pygame.Rect((WIDTH - dialog_width) // 2, (HEIGHT - dialog_height) // 2, dialog_width, dialog_height)
# #     pygame.draw.rect(screen, WHITE, dialog_rect)
# #     pygame.draw.rect(screen, BLACK, dialog_rect, 2)
# #
# #     dialog_font = pygame.font.Font(None, 36)
# #     text_surface = dialog_font.render("Are you sure you want to exit?", True, BLACK)
# #     text_rect = text_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 50))
# #     screen.blit(text_surface, text_rect)
# #
# #     yes_button = draw_button("Yes", dialog_rect.x + 50, dialog_rect.y + 100, False)
# #     no_button = draw_button("No", dialog_rect.x + dialog_width - 50 - button_width, dialog_rect.y + 100, False)
# #
# #     return yes_button, no_button
# 
# # def show_rules():
# #     screen.fill(WHITE)
# #     rules_font = pygame.font.Font(None, 28)
# #     rules = [
# #         "~Gameplay:",
# #         " Each player selects a color (Black or White).",
# #         " Players take turns placing their first piece. The first piece must touch the opponent's piece.",
# #         " On your turn, you can either:",
# #         "  -Place a new piece from your collection.",
# #         "  -Move an existing piece already on the board (after placing your Queen Bee).",
# #         "",
# #         "~Game Pieces:",
# #         " -Queen Bee: Must be placed by your fourth turn.",
# #         " -Ant: Moves any number of spaces.",
# #         " -Grasshopper: Jumps over adjacent pieces.",
# #         " -Beetle: Moves one space and can climb on top of other pieces.",
# #         " -Spider: Moves exactly three spaces.",
# #         "",
# #         "~Movement Rules:",
# #         " New pieces must touch only your own pieces when placed, except for the first piece.",
# #         " You cannot move a piece that would split the hive into two separate groups.",
# #         " Once placed, a piece cannot be removed from the board.",
# #         "",
# #         "~Winning the Game:",
# #         " The game ends when one player completely surrounds the opponent's Queen Bee with their pieces."
# #     ]
# #
# #     y_offset = 50
# #     for line in rules:
# #         text_surface = rules_font.render(line, True, BLACK)
# #         screen.blit(text_surface, (50, y_offset))
# #         y_offset += 30
# #
# #     back_button = draw_button("Back", WIDTH - 350, HEIGHT - 100, False)
# #     return back_button
# 
# # def show_game_options():
# #     screen.fill(WHITE)
# #     options_font = pygame.font.Font(None, 48)
# #     options_title = options_font.render("Options", True, BLACK)
# #     screen.blit(options_title, ((WIDTH - options_title.get_width()) // 2, 50))
# #
# #     options = [
# #         "Player VS Player",
# #         "Player VS Computer",
# #         "Computer VS Computer"
# #     ]
# #
# #     y_offset = 150
# #     buttons = []
# #     for option in options:
# #         button = draw_button(option, (WIDTH - button_width) // 2, y_offset, False)
# #         buttons.append((button, option))
# #         y_offset += button_height + button_spacing
# #
# #     back_button = draw_button("Back", WIDTH - 350, HEIGHT - 100, False)
# #     return buttons, back_button
# 
# 
# 
# 
# 
# 
# 
# # Main loop
# #Main
# running = True
# show_dialog = False
# show_rules_screen = False
# show_options_screen = False
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
# 
#     # Fill screen with background color
#     screen.fill(back_color)
# 
#     # Get mouse position
#     mouse_pos = pygame.mouse.get_pos()
# 
#     if show_dialog:
#         yes_button, no_button = show_exit_dialog()
#         yes_hovered = yes_button.collidepoint(mouse_pos)
#         no_hovered = no_button.collidepoint(mouse_pos)
# 
#         yes_button = draw_button("Yes", yes_button.x, yes_button.y, yes_hovered)
#         no_button = draw_button("No", no_button.x, no_button.y, no_hovered)
# 
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button clicked
#                     if yes_button.collidepoint(event.pos):
#                         running = False
#                     elif no_button.collidepoint(event.pos):
#                         show_dialog = False
#     elif show_rules_screen:
#         back_button = show_rules()
#         back_hovered = back_button.collidepoint(mouse_pos)
#         back_button = draw_button("Back", back_button.x, back_button.y, back_hovered)
# 
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button clicked
#                     if back_button.collidepoint(event.pos):
#                         show_rules_screen = False
#     elif show_options_screen:
#         option_buttons, back_button = show_game_options()
#         back_hovered = back_button.collidepoint(mouse_pos)
#         back_button = draw_button("Back", back_button.x, back_button.y, back_hovered)
# 
#         option_hovered = [button[0].collidepoint(mouse_pos) for button in option_buttons]
#         option_buttons = [(draw_button(button[1], button[0].x, button[0].y, option_hovered[i]), button[1]) for i, button in enumerate(option_buttons)]
# 
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button clicked
#                     if back_button.collidepoint(event.pos):
#                         show_options_screen = False
#                     for i, (button_rect, option_text) in enumerate(option_buttons):
#                         if button_rect.collidepoint(event.pos):
#                             print(f"Option {i + 1} selected: {option_text}")  # Replace with actual game logic
#     else:
#         # Draw buttons and check for hover effects
#         start_button = draw_button("Start",
#                                    50, HEIGHT // 2 - button_height - button_spacing - 10,
#                                    False)   # Initially not hovered
# 
#         rules_button = draw_button("Rules",
#                                    50, HEIGHT // 2 + 10,
#                                    False)   # Initially not hovered
# 
#         exit_button = draw_button("Exit",
#                                   50, HEIGHT // 2 + button_height + button_spacing + 30,
#                                   False)   # Initially not hovered
# 
#         # Check hover states after drawing buttons
#         start_hovered = start_button.collidepoint(mouse_pos)
#         rules_hovered = rules_button.collidepoint(mouse_pos)
#         exit_hovered = exit_button.collidepoint(mouse_pos)
# 
#         # Update buttons with hover state
#         start_button = draw_button("Start",
#                                    50, HEIGHT // 2 - button_height - button_spacing - 10,
#                                    start_hovered)
# 
#         rules_button = draw_button("Rules",
#                                    50, HEIGHT // 2 + 10,
#                                    rules_hovered)
# 
#         exit_button = draw_button("Exit",
#                                   50, HEIGHT // 2 + button_height + button_spacing + 30,
#                                   exit_hovered)
# 
#         # Draw logo image on the right side of the screen
#         screen.blit(logo_image, (WIDTH - logo_image.get_width() - 20,
#                                   (HEIGHT - logo_image.get_height()) // 2))
# 
#         # Check for button clicks
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button clicked
#                     if start_button.collidepoint(event.pos):
#                         show_options_screen = True
#                     elif rules_button.collidepoint(event.pos):
#                         show_rules_screen = True
#                     elif exit_button.collidepoint(event.pos):
#                         show_dialog = True
# 
#     # Update display
#     pygame.display.flip()
# 
# # Quit Pygame
# pygame.quit()
# sys.exit()


import pygame
import sys

# Initialize Pygame
pygame.init()

# Import constants after initializing Pygame
from utils.constants import *

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

# Load logo image
logo_image = pygame.image.load("assets/logo.png")  # Update with your logo path
logo_image = pygame.transform.scale(logo_image, (450, 450))  # Scale the image if needed

# Button settings
button_font = pygame.font.Font(None, 36)

# Import utility functions
from utils.draw_button import draw_button
from utils.show_exit_dialog import show_exit_dialog
from utils.show_rules import show_rules
from utils.show_game_options import show_game_options

# Main loop
running = True
show_dialog = False
show_rules_screen = False
show_options_screen = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with background color
    screen.fill(back_color)

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    if show_dialog:
        yes_button, no_button = show_exit_dialog(screen, button_font)
        yes_hovered = yes_button.collidepoint(mouse_pos)
        no_hovered = no_button.collidepoint(mouse_pos)

        yes_button = draw_button(screen, "Yes", yes_button.x, yes_button.y, yes_hovered, button_font)
        no_button = draw_button(screen, "No", no_button.x, no_button.y, no_hovered, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if yes_button.collidepoint(event.pos):
                        running = False
                    elif no_button.collidepoint(event.pos):
                        show_dialog = False
    elif show_rules_screen:
        back_button = show_rules(screen, button_font)
        back_hovered = back_button.collidepoint(mouse_pos)
        back_button = draw_button(screen, "Back", back_button.x, back_button.y, back_hovered, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if back_button.collidepoint(event.pos):
                        show_rules_screen = False
    elif show_options_screen:
        option_buttons, back_button = show_game_options(screen, button_font)
        back_hovered = back_button.collidepoint(mouse_pos)
        back_button = draw_button(screen, "Back", back_button.x, back_button.y, back_hovered, button_font)

        option_hovered = [button[0].collidepoint(mouse_pos) for button in option_buttons]
        option_buttons = [(draw_button(screen, button[1], button[0].x, button[0].y, option_hovered[i], button_font), button[1]) for i, button in enumerate(option_buttons)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if back_button.collidepoint(event.pos):
                        show_options_screen = False
                    for i, (button_rect, option_text) in enumerate(option_buttons):
                        if button_rect.collidepoint(event.pos):
                            print(f"Option {i + 1} selected: {option_text}")  # Replace with actual game logic
    else:
        # Draw buttons and check for hover effects
        start_button = draw_button(screen, "Start",
                                   50, HEIGHT // 2 - button_height - button_spacing - 10,
                                   False, button_font)   # Initially not hovered

        rules_button = draw_button(screen, "Rules",
                                   50, HEIGHT // 2 + 10,
                                   False, button_font)   # Initially not hovered

        exit_button = draw_button(screen, "Exit",
                                  50, HEIGHT // 2 + button_height + button_spacing + 30,
                                  False, button_font)   # Initially not hovered

        # Check hover states after drawing buttons
        start_hovered = start_button.collidepoint(mouse_pos)
        rules_hovered = rules_button.collidepoint(mouse_pos)
        exit_hovered = exit_button.collidepoint(mouse_pos)

        # Update buttons with hover state
        start_button = draw_button(screen, "Start",
                                   50, HEIGHT // 2 - button_height - button_spacing - 10,
                                   start_hovered, button_font)

        rules_button = draw_button(screen, "Rules",
                                   50, HEIGHT // 2 + 10,
                                   rules_hovered, button_font)

        exit_button = draw_button(screen, "Exit",
                                  50, HEIGHT // 2 + button_height + button_spacing + 30,
                                  exit_hovered, button_font)

        # Draw logo image on the right side of the screen
        screen.blit(logo_image, (WIDTH - logo_image.get_width() - 20,
                                  (HEIGHT - logo_image.get_height()) // 2))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if start_button.collidepoint(event.pos):
                        show_options_screen = True
                    elif rules_button.collidepoint(event.pos):
                        show_rules_screen = True
                    elif exit_button.collidepoint(event.pos):
                        show_dialog = True

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()git
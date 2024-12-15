import pygame
import sys
from utils.constants import *
from utils.game_table import GameTable  # Import the GameTable class

pygame.init()

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

# Load logo image
logo_image = pygame.image.load("assets/logo.png")
logo_image = pygame.transform.scale(logo_image, (450, 450))

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
                            print(f"Option {i + 1} selected: {option_text}")  # Debug log
                            # Open the game table based on selected option
                            game_mode = option_text
                            game_table = GameTable(screen, game_mode)  # Pass the screen and game mode to GameTable
                            game_mode_result = game_table.run()  # Run the game table loop

                            # Handle returning from the game table (if needed)
                            if game_mode_result == "main_menu":
                                show_options_screen = False
    else:
        # Draw buttons and check for hover effects
        start_button = draw_button(screen, "Start", 50, HEIGHT // 2 - button_height - button_spacing - 10, False, button_font)
        rules_button = draw_button(screen, "Rules", 50, HEIGHT // 2 + 10, False, button_font)
        exit_button = draw_button(screen, "Exit", 50, HEIGHT // 2 + button_height + button_spacing + 30, False, button_font)

        # Check hover states after drawing buttons
        start_hovered = start_button.collidepoint(mouse_pos)
        rules_hovered = rules_button.collidepoint(mouse_pos)
        exit_hovered = exit_button.collidepoint(mouse_pos)

        # Update buttons with hover state
        start_button = draw_button(screen, "Start", 50, HEIGHT // 2 - button_height - button_spacing - 10, start_hovered, button_font)
        rules_button = draw_button(screen, "Rules", 50, HEIGHT // 2 + 10, rules_hovered, button_font)
        exit_button = draw_button(screen, "Exit", 50, HEIGHT // 2 + button_height + button_spacing + 30, exit_hovered, button_font)

        # Draw logo image on the right side of the screen
        screen.blit(logo_image, (WIDTH - logo_image.get_width() - 20, (HEIGHT - logo_image.get_height()) // 2))

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
sys.exit()

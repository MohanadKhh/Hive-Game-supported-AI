import pygame
import math

class GameTable:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def draw_hexagon(self, x, y, size):
        """Draw a single hexagon centered at (x, y) with the given size."""
        points = [
            (
                x + size * math.cos(math.radians(angle)),
                y + size * math.sin(math.radians(angle))
            )
            for angle in range(0, 360, 60)
        ]
        pygame.draw.polygon(self.screen, (200, 200, 200), points, 2)

    def draw_hexagonal_grid(self, start_x, start_y, rows, cols, size):
        """Draw a grid of hexagons."""
        dx = 3 / 2 * size
        dy = math.sqrt(3) * size
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * dx
                y = start_y + row * dy + (col % 2) * (dy / 2)
                self.draw_hexagon(x, y, size)

    def run(self):
        """Run the game table screen."""
        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Define the size of the hexagons
        hex_size = 40  # You can change this to adjust the hexagon size

        # Calculate the starting position for the grid to center it on the screen
        grid_width = 13 * (3 / 2 * hex_size)  # Width of the grid (13 hexagons horizontally)
        grid_height = 8 * (math.sqrt(3) * hex_size)  # Height of the grid (8 hexagons vertically)

        start_x = (screen_width - grid_width) / 2
        start_y = (screen_height - grid_height) / 2

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None  # Exit the game
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    return "main_menu"  # Return to main menu

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw hexagonal grid
            self.draw_hexagonal_grid(start_x, start_y, 8, 13, hex_size)

            # Update display
            pygame.display.flip()

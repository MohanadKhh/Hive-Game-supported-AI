import pygame
import math
from environment.hive import Hex, HexBoard, HexUtils, Piece
from pieces.QueenBee import QueenBee
from pieces.Grasshopper import Grasshopper
from pieces.Beetle import Beetle
from pieces.Spider import Spider
from pieces.Ant import Ant
from ai.AI_agent import agent_best_next_move, alpha_beta_iterative_deepening  # Import AI functions

class GameTable:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.running = True
        self.board = HexBoard()
        self.selected_piece = None
        self.selected_hex = None
        self.selected_valid_moves = []
        self.current_player = 0  # Ensure White (0) always starts
        self.game_mode = game_mode
        self.ai_depth = 3  # Set AI search depth
        self.init_pieces()
        self.white_rounds = 0
        self.black_rounds = 0
        self.white_queen_played = False
        self.black_queen_played = False
        self.show_queen_warning = False

    def init_pieces(self):
        # Initialize player decks with pieces
        self.black_pieces = [QueenBee(1), Grasshopper(1), Grasshopper(1), Grasshopper(1), Beetle(1), Beetle(1), Spider(1), Spider(1), Ant(1), Ant(1), Ant(1)]
        self.white_pieces = [QueenBee(0), Grasshopper(0), Grasshopper(0), Grasshopper(0), Beetle(0), Beetle(0), Spider(0), Spider(0), Ant(0), Ant(0), Ant(0)]

    def draw_hexagon(self, x, y, size, color):
        points = [
            (
                x + size * math.cos(math.radians(angle)),
                y + size * math.sin(math.radians(angle))
            )
            for angle in range(0, 360, 60)
        ]
        pygame.draw.polygon(self.screen, color, points, 2)

    def draw_piece(self, x, y, piece, is_selected=False):
        hex_size = 40  # Use the same size as the hexagon cells

        points = [
            (
                x + hex_size * math.cos(math.radians(angle)),
                y + hex_size * math.sin(math.radians(angle))
            )
            for angle in range(0, 360, 60)
        ]

        # Change color to red if the piece is selected
        if is_selected:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0) if piece.color == 1 else (255, 255, 255)

        pygame.draw.polygon(self.screen, color, points)

        piece_name = piece.name
        font_size = 20  # Adjust font size if needed
        text_color = (255, 255, 255) if color == (0, 0, 0) else (0, 0, 0)
        text_surface = pygame.font.Font(None, font_size).render(piece_name, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_turn_text(self):
        font = pygame.font.Font(None, 36)
        text_color = (255, 0, 0)  # Red color for the turn text
        screen_width, screen_height = self.screen.get_size()

        if self.current_player == 0:  # White's turn
            turn_text = "White turn now!"
            text_surface = font.render(turn_text, True, text_color)
            text_rect = text_surface.get_rect(center=(screen_width - 100, 450))  # Adjust position if necessary
            self.screen.blit(text_surface, text_rect)
        else:  # Black's turn
            turn_text = "Black turn now!"
            text_surface = font.render(turn_text, True, text_color)
            text_rect = text_surface.get_rect(center=(100, 450))  # Adjust position if necessary
            self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        screen_width, screen_height = self.screen.get_size()

        # Define the size of the hexagons
        hex_size = 40

        # Calculate the offset for the grid to center it on the screen
        offset_x = screen_width / 2
        offset_y = screen_height / 2

        # Draw hexagonal grid
        for q in range(-6, 7):
            for r in range(-6, 7):
                if abs(q + r) <= 6:
                    x = offset_x + hex_size * (3 / 2 * q)
                    y = offset_y + hex_size * (math.sqrt(3) * (r + q / 2))
                    self.draw_hexagon(x, y, hex_size, (200, 200, 200))

        # Draw player decks with 2 columns
        column_spacing = 60  # Adjust as needed
        row_spacing = 60  # Adjust as needed
        for i, piece in enumerate(self.black_pieces):
            x = 50 + (i % 2) * column_spacing
            y = 100 + (i // 2) * row_spacing
            self.draw_piece(x, y, piece, is_selected=(self.selected_piece == piece))

        for i, piece in enumerate(self.white_pieces):
            x = screen_width - 100 - (i % 2) * column_spacing
            y = 100 + (i // 2) * row_spacing
            self.draw_piece(x, y, piece, is_selected=(self.selected_piece == piece))

        # Draw pieces on the board
        for (q, r), piece in self.board.board.items():
            if piece:
                x = offset_x + hex_size * (3 / 2 * q)
                y = offset_y + hex_size * (math.sqrt(3) * (r + q / 2))
                self.draw_piece(x, y, piece)

        # Draw the turn text
        self.draw_turn_text()

    def handle_piece_selection(self, pos):
        screen_width = self.screen.get_width()
        for i, piece in enumerate(self.black_pieces):
            if self.current_player == 1 and math.sqrt(
                    (50 + (i % 2) * 60 - pos[0]) ** 2 + (100 + (i // 2) * 60 - pos[1]) ** 2) <= 20:
                self.selected_piece = piece
                self.selected_piece_index = i
                self.selected_piece_origin = 'black'
                self.selected_hex = None
                return
        for i, piece in enumerate(self.white_pieces):
            if self.current_player == 0 and math.sqrt(
                    (screen_width - 100 - (i % 2) * 60 - pos[0]) ** 2 + (100 + (i // 2) * 60 - pos[1]) ** 2) <= 20:
                self.selected_piece = piece
                self.selected_piece_index = i
                self.selected_piece_origin = 'white'
                self.selected_hex = None
                return

    def highlight_moves(self, moves):
        offset_x = self.screen.get_width() / 2
        offset_y = self.screen.get_height() / 2
        for move in moves:
            x = offset_x + 40 * (3 / 2 * move.q)
            y = offset_y + 40 * (math.sqrt(3) * (move.r + move.q / 2))
            self.draw_hexagon(x, y, 40, (0, 255, 0))

    def check_queen_played(self):
        if self.current_player == 0:  # White player
            if not self.white_queen_played and self.white_rounds >= 3:
                return False
        else:  # Black player
            if not self.black_queen_played and self.black_rounds >= 3:
                return False
        return True


    def show_message_box(self, message):
        dialog_width, dialog_height = 600, 150  # Increased dimensions
        dialog_rect = pygame.Rect((self.screen.get_width() - dialog_width) // 2, (self.screen.get_height() - dialog_height) // 2, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect, 2)

        font = pygame.font.Font(None, 28)  # Reduced font size
        lines = message.split('\n')
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 30 + i * 30))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

        pygame.time.wait(2000)  # Show the message for 2 seconds



    def ai_select_piece_and_place(self):
        # Select a piece from AI's deck (black pieces) if there's no piece selected
        if not self.selected_piece and self.black_pieces:
            self.selected_piece = self.black_pieces.pop(0)
            self.selected_valid_moves = self.selected_piece.get_valid_position(self.board)

        # If AI has selected a piece, make the best move
        if self.selected_piece and self.selected_valid_moves:
            best_move = self.selected_valid_moves[0]  # Select the first valid move as the best move
            self.board.place_piece(best_move, self.selected_piece)
            if isinstance(self.selected_piece, QueenBee):
                self.black_queen_played = True
            self.selected_piece = None
            self.selected_valid_moves = []
            self.current_player = 1 - self.current_player  # Switch player

    def is_piece_surrounded(self, piece):
        hex_coords = [(piece.position.q, piece.position.r)]
        for direction in HexUtils.DIRECTIONS:
            neighbor = Hex(piece.position.q + direction.q, piece.position.r + direction.r)
            hex_coords.append((neighbor.q, neighbor.r))
        for coord in hex_coords:
            if coord not in self.board.board or self.board.board[coord] is None:
                return False
        return True

    def get_queen_bee(self, color):
        for (q, r), piece in self.board.board.items():
            if isinstance(piece, QueenBee) and piece.color == color:
                return piece
        return None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    return "main_menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_hex = HexUtils.pixel_to_hex(event.pos[0] - self.screen.get_width() / 2,
                                                            event.pos[1] - self.screen.get_height() / 2, 40)
                        if self.selected_piece:
                            if clicked_hex in self.selected_valid_moves:
                                if self.selected_hex:
                                    self.board.board[(self.selected_hex.q, self.selected_hex.r)] = None
                                self.board.place_piece(clicked_hex, self.selected_piece)
                                if isinstance(self.selected_piece, QueenBee):
                                    if self.current_player == 0:
                                        self.white_queen_played = True
                                    else:
                                        self.black_queen_played = True
                                # Validate and remove the piece from the player's deck only after placing it on the board
                                if self.selected_piece_origin == 'black' and 0 <= self.selected_piece_index < len(
                                        self.black_pieces):
                                    self.black_pieces.pop(self.selected_piece_index)
                                elif self.selected_piece_origin == 'white' and 0 <= self.selected_piece_index < len(
                                        self.white_pieces):
                                    self.white_pieces.pop(self.selected_piece_index)
                                self.selected_piece = None
                                self.selected_valid_moves = []
                                if self.current_player == 0:
                                    self.white_rounds += 1
                                else:
                                    self.black_rounds += 1

                                # Check for win condition
                                white_queen = self.get_queen_bee(0)
                                black_queen = self.get_queen_bee(1)
                                if white_queen and self.is_piece_surrounded(white_queen):
                                    self.show_message_box("Black wins!")
                                    self.running = False
                                elif black_queen and self.is_piece_surrounded(black_queen):
                                    self.show_message_box("White wins!")
                                    self.running = False

                                self.current_player = 1 - self.current_player  # Switch player
                            else:
                                self.selected_piece = None
                                self.selected_valid_moves = []
                        else:
                            piece = self.board.get_piece(clicked_hex)
                            if piece and piece.color == self.current_player:
                                # Check if Queen Bee is placed before allowing to move any piece
                                if (self.current_player == 0 and not self.white_queen_played) or (
                                        self.current_player == 1 and not self.black_queen_played):
                                    if not isinstance(piece, QueenBee):
                                        self.show_message_box(
                                            "You must place the Queen Bee before moving any other piece.")
                                        continue
                                self.selected_hex = clicked_hex
                                self.selected_piece = piece
                                self.selected_valid_moves = piece.get_valid_moves(clicked_hex, self.board)
                            else:
                                self.handle_piece_selection(event.pos)
                                if self.selected_piece:
                                    if not self.check_queen_played():
                                        if self.selected_piece.name != "Queen Bee":
                                            self.show_message_box("You must play the Queen Bee by the 4th turn.")
                                            self.selected_piece = None
                                        else:
                                            self.selected_valid_moves = self.selected_piece.get_valid_position(
                                                self.board)
                                    else:
                                        self.selected_valid_moves = self.selected_piece.get_valid_position(self.board)

            if self.game_mode == "Player VS Computer" and self.current_player == 1:
                if not self.black_queen_played and self.black_rounds == 3:
                    self.selected_piece = self.black_pieces.pop(0)  # Select the queen piece
                self.ai_select_piece_and_place()

            self.screen.fill((255, 235, 215))
            self.draw_board()
            self.highlight_moves(self.selected_valid_moves)
            pygame.display.flip()






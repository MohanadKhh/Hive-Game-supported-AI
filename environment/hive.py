import math
import tkinter as tk
from tkinter import messagebox


class Hex:
    """Represents a hex coordinate in axial coordinates (q, r)."""
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    def __repr__(self):
        return f"Hex({self.q}, {self.r}, {self.s})"
    

class HexUtils:
    directions = {
        'N': (0, -1),    # North
        'NW': (-1, 0),   # North-West
        'SW': (-1, 1),    # South-West
        'S': (0, 1),     # South
        'SE': (1, 0),    # South-East
        'NE': (1, -1)    # North-East
    }
    
    @staticmethod
    def get_direction(direction):
        return HexUtils.directions[direction]

    @staticmethod
    def hex_to_pixel(hex, hex_size, offset_x, offset_y):
        x = hex_size * (3 / 2 * hex.q)
        y = hex_size * (math.sqrt(3) * (hex.r + hex.q / 2))
        return (x + offset_x, y + offset_y)

    @staticmethod
    def pixel_to_hex(x, y, hex_size):
        q = (2 / 3 * x) / hex_size
        r = (-x / 3 + math.sqrt(3) / 3 * y) / hex_size
        return Hex(round(q), round(r))



class Piece:
    """Base class for pieces on the hexagonal board."""
    def __init__(self, name,color):
        self.name = name
        self.color=color    #0 white 1 black

    def move(self, hex, direction, board):
        """Basic movement method, should be overridden by specific piece types."""
        raise NotImplementedError("This method should be implemented by specific pieces.")


class QueenBee(Piece):
    def __init__(self):
        super().__init__('Queen Bee')

    def move(self, hex, direction, board):

        d = HexUtils.get_direction(direction)
        new_hex = Hex(hex.q + d[0], hex.r + d[1])

        if new_hex in board.board and board.board[(new_hex.q, new_hex.r)] is None:
            board.board[(new_hex.q, new_hex.r)] = self
            board.board[(hex.q, hex.r)] = None
        else:
            print("Invalid move for Queen Bee.")


class Grasshopper(Piece):
    def __init__(self):
        super().__init__('Grasshopper')

    def move(self, hex, direction, board):
        d = HexUtils.get_direction(direction)
        new_hex = Hex(hex.q + d[0], hex.r + d[1])

        while board.board.get((new_hex.q, new_hex.r)) is not None:
            new_hex = Hex(new_hex.q + d[0], new_hex.r + d[1])

        if board.board.get((new_hex.q, new_hex.r)) is None:
            board.board[(new_hex.q, new_hex.r)] = self
            board.board[(hex.q, hex.r)] = None
        else:
            print("Invalid jump for Grasshopper.")


class HexBoard:
    def __init__(self, grid_size=50):
        self.grid_size = grid_size
        self.board = self.create_board()

    def create_board(self):
        board = {}
        for q in range(-self.grid_size, self.grid_size):
            for r in range(-self.grid_size, self.grid_size):
                s = -q - r
                if abs(s) < self.grid_size:
                    board[(q, r)] = None
        return board

    def place_piece(self, hex, piece):
        if (hex.q, hex.r) in self.board:
            self.board[(hex.q, hex.r)] = piece
        else:
            raise ValueError("Hex not on the board.")

    def get_piece(self, hex):
        return self.board.get((hex.q, hex.r))

    def move(self, hex, direction, piece):
        # Ensure that piece is in the current hex
        current_piece = self.get_piece(hex)
        if current_piece != piece:
            raise ValueError("No matching piece at this location.")
        
        piece.move(hex, direction, self)


class HexagonalBoardGUI(tk.Tk):
    """The GUI for visualizing the hexagonal board."""
    def __init__(self, board, hex_size=40, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.hex_size = hex_size
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()

        self.center_x = 400
        self.center_y = 300
        self.offset_x = self.center_x
        self.offset_y = self.center_y
        self.selected_hex = None

        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        for (q, r), piece in self.board.board.items():
            if abs(q) < self.board.grid_size and abs(r) < self.board.grid_size:
                center_x, center_y = HexUtils.hex_to_pixel(Hex(q, r), self.hex_size, self.offset_x, self.offset_y)
                if piece:
                    if isinstance(piece, QueenBee):
                        self.draw_hex(center_x, center_y, 'yellow')
                    elif isinstance(piece, Grasshopper):
                        self.draw_hex(center_x, center_y, 'green')
                    else:
                        self.draw_hex(center_x, center_y, 'lightblue')
                    self.draw_piece(center_x, center_y, piece.name)
                else:
                    self.draw_hex(center_x, center_y)

    def draw_hex(self, x, y, color='lightgray'):
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = x + self.hex_size * math.cos(angle)
            py = y + self.hex_size * math.sin(angle)
            points.append((px, py))
            self.canvas.create_polygon(points, outline="black", fill=color, width=2)

    def draw_piece(self, x, y, piece):
        self.canvas.create_text(x, y, text=piece, font=("Arial", 8, "bold"))

    def on_click(self, event):
        clicked_hex = HexUtils.pixel_to_hex(event.x - self.offset_x, event.y - self.offset_y, self.hex_size)
        messagebox.showinfo("Clicked Hex", f"Hex: ({clicked_hex.q}, {clicked_hex.r}).")


if __name__ == "__main__":
    board = HexBoard(grid_size=25)

    center_hex = Hex(0, 0)
    bee = QueenBee()
    grasshopper = Grasshopper()

    # just example 
    board.place_piece(center_hex, bee)
    board.place_piece(Hex(-2, 0), grasshopper)
    board.place_piece(Hex(0,-1), Piece("any"))
    board.place_piece(Hex(0,-2), Piece("any"))
    board.place_piece(Hex(-1,-2), Piece("any"))
    board.place_piece(Hex(-2,-1), Piece("any"))
    board.place_piece(Hex(-2,1), Piece("any"))
    board.place_piece(Hex(-1,0), Piece("any"))
    board.place_piece(Hex(2,-1), Piece("any"))
    board.place_piece(Hex(2,0), Piece("any"))
    board.place_piece(Hex(1,1), Piece('any'))
    board.place_piece(Hex(1,-1), Piece("any"))

    # remove comment and run again to see the move
    # board.move(Hex(-2, 0), 'N' ,grasshopper)
    

    app = HexagonalBoardGUI(board)
    app.mainloop()

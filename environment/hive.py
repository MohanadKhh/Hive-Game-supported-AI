#Hive file
import math

class Hex:
    """Represents a hex coordinate in axial coordinates (q, r)."""
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r)

    def __hash__(self):
        return hash((self.q, self.r))

    def __repr__(self):
        return f"Hex({self.q}, {self.r}, {self.s})"

    def __eq__(self, other):
        if isinstance(other, Hex):
            return self.q == other.q and self.r == other.r and self.s == other.s
        return False
    
class HexUtils:
    DIRECTIONS = [
        Hex(1, 0), Hex(1, -1), Hex(0, -1),
        Hex(-1, 0), Hex(-1, 1), Hex(0, 1)
    ]

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

    @staticmethod
    def hex_neighbors(hex):
        neighbors = []
        for direction in HexUtils.directions.values():
            neighbor = Hex(hex.q + direction[0], hex.r + direction[1])
            neighbors.append(neighbor)
        return neighbors
    
    @staticmethod
    def is_hive_connected(board):
        """Checks if all pieces on the board are part of one connected hive."""
        visited = set()
        pieces = [(q, r) for (q, r), piece in board.board.items() if piece is not None]

        if not pieces:
            return True

        # Start flood-fill from the first piece
        def flood_fill(hex):
            if hex in visited or (board.board[hex] is None):
                return
            visited.add(hex)
            for direction in HexUtils.directions.values():
                neighbor = (hex[0] + direction[0], hex[1] + direction[1])
                if neighbor in board.board and board.board[neighbor] is not None:
                    flood_fill(neighbor)

        # Start from the first piece
        flood_fill(pieces[0])

        # If all pieces were visited, the hive is connected
        return len(visited) == len(pieces)
    
    @staticmethod
    def is_valid_after_move(from_hex, board):
        piece = board.get_piece(from_hex)

        if not piece:
            return False

        board.board[(from_hex.q,from_hex.r)] = None
        connected = HexUtils.is_hive_connected(board)
        board.board[(from_hex.q,from_hex.r)] = piece

        return connected
    
class Piece:
    """Base class for pieces on the hexagonal board."""
    def __init__(self, name,color,value=5):
        self.name = name
        self.color=color #0 for white 1 for black
        self.value = value
    
    def get_valid_moves(self, hex, board):
        raise NotImplementedError("")
    directions = [
        Hex (0, -1),    # North
        Hex (-1, 0),   # North-West
        Hex (-1, 1),    # South-West
        Hex (0, 1),     # South
        Hex (1, 0),    # South-East
        Hex(1, -1)    # North-East
    ]
    def get_valid_position(self, board):
        numberOfPieces = sum(1 for piece in board.board.values() if piece is not None)
        valid_position=[]
        if numberOfPieces == 0:
            valid_position =[Hex(0,0)]
        elif numberOfPieces ==1 :
            valid_position = [Hex (0, -1),Hex (-1, 0),Hex (-1, 1),Hex (0, 1),Hex (1, 0),Hex(1, -1)]
        else:
            for (q,r) ,piece in board.board.items():
                if piece is not None:
                    if piece.color == 0 and self.color ==0: #white
                        neighbors = [
                        (q, r - 1),
                        (q - 1, r),
                        (q - 1, r + 1),
                        (q, r + 1),
                        (q + 1, r),
                        (q + 1, r - 1)
                        ]
                        for neighbor in neighbors:
                            empty_place = board.get_piece(Hex(neighbor[0],neighbor[1])) 
                            if empty_place is None:
                                black_neighbors = [
                                    (neighbor[0], neighbor[1] - 1),
                                    (neighbor[0] - 1, neighbor[1]),
                                    (neighbor[0] - 1, neighbor[1] + 1),
                                    (neighbor[0], neighbor[1] + 1),
                                    (neighbor[0] + 1, neighbor[1]),
                                    (neighbor[0] + 1, neighbor[1] - 1)
                                    ]
                                flag=True
                                for black_place in black_neighbors:
                                    
                                    if board.get_piece(Hex(black_place[0],black_place[1])) is not None and board.get_piece(Hex(black_place[0],black_place[1])).color == 1:
                                        flag=False
                                        break
                                if flag:
                                    valid_position.append(Hex(neighbor[0],neighbor[1])) 
                    elif piece.color == 1 and self.color ==1: #black
                        neighbors = [
                        (q, r - 1),
                        (q - 1, r),
                        (q - 1, r + 1),
                        (q, r + 1),
                        (q + 1, r),
                        (q + 1, r - 1)
                        ]
                        for neighbor in neighbors:
                            empty_place = board.get_piece(Hex(neighbor[0],neighbor[1])) 
                            if empty_place is None:
                                white_neighbors = [
                                    (neighbor[0], neighbor[1] - 1),
                                    (neighbor[0] - 1, neighbor[1]),
                                    (neighbor[0] - 1, neighbor[1] + 1),
                                    (neighbor[0], neighbor[1] + 1),
                                    (neighbor[0] + 1, neighbor[1]),
                                    (neighbor[0] + 1, neighbor[1] - 1)
                                    ]
                                flag=True
                                for white_place in white_neighbors:
                                    if board.get_piece(Hex(white_place[0],white_place[1])) is not None and board.get_piece(Hex(white_place[0],white_place[1])).color == 0:
                                        flag=False
                                        break
                                if flag:
                                    valid_position.append(Hex(neighbor[0],neighbor[1]))
        return valid_position

                            


               
    
    def move(self, hex, direction, board):
        """Basic movement method, should be overridden by specific piece types."""
        raise NotImplementedError("This method should be implemented by specific pieces.")

class HexBoard:
    def __init__(self, grid_size=50):
        self.grid_size = grid_size
        self.board = self.create_board()
        # print("DEBUG: HexBoard initialized with board:", self.board)

    # def validate_board(self):
    #     if self.board is None:
    #         raise ValueError("board.board is None! Something went wrong.")

    def display(self):
        """
        Display the board in a readable hexagonal format.
        Empty hexes are represented by ".", and filled hexes display the piece's representation.
        """
        min_q = min(q for q, r in self.board)
        max_q = max(q for q, r in self.board)
        min_r = min(r for q, r in self.board)
        max_r = max(r for q, r in self.board)

        for r in range(min_r, max_r + 1):
            row = " " * (r - min_r)  # Indentation for hexagonal format
            for q in range(min_q, max_q + 1):
                s = -q - r
                if (q, r) in self.board and abs(s) < self.grid_size:
                    piece = self.board[(q, r)]
                    row += (str(piece) if piece else ".") + " "
                else:
                    row += "  "  # Empty spaces for alignment

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
            piece.set_position(hex.q, hex.r)  # Set the position of the piece
            return self
        else:
            raise ValueError("Hex not on the board.")

    def get_piece(self, hex):
        return self.board.get((hex.q, hex.r))

    def move(self, hex, new_hex,board,valid_moves):
        piece = self.get_piece(hex)
        piece.move(hex, new_hex, self,valid_moves)
        return self

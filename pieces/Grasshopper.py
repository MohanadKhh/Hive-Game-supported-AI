#Pieces_Grasshopper File
from environment.hive import Piece, HexUtils, Hex
class Grasshopper(Piece):
    def __init__(self,color):
        super().__init__('Grasshopper',color)
        self.position = None  # Add position attribute
    def set_position(self, q, r):
        self.position = Hex(q, r)
    def get_valid_moves(self, hex, board):
        valid_moves=[]
        if HexUtils.is_valid_after_move(hex, board):
            for d in HexUtils.directions.values():
                new_hex = Hex(hex.q + d[0], hex.r + d[1])
                if board.board[(new_hex.q,new_hex.r)] is None:
                    continue

                while board.board.get((new_hex.q, new_hex.r)) is not None:
                    new_hex = Hex(new_hex.q + d[0], new_hex.r + d[1])

                valid_moves.append(new_hex)

        return valid_moves


    def move(self, hex, new_hex, board,valid_moves):
        if new_hex in valid_moves:
            board.board[(new_hex.q, new_hex.r)] = self
            board.board[(hex.q, hex.r)] = None

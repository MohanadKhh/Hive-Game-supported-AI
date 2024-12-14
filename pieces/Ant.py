from environment.hive import Piece, HexUtils, Hex

class Ant(Piece):
    def __init__(self, color):
        super().__init__('Ant' ,color)

    def get_valid_moves(self, current_position, board):
        if not HexUtils.is_valid_after_move(current_position, board):
            return []

        def is_valid_move(start, end, visited):
            if (end.q, end.r) not in board.board:
                return False
            if board.board[(end.q, end.r)] is not None:
                return False
            if not self.is_connected(end, board.board, start, current_position):
                return False
            if (end.q, end.r) in visited:
                return False
            return True

        def freedom_move(piece_position, direction, board):
            directions = HexUtils.directions

            def is_occupied(hex):
                if (hex.q, hex.r) == (current_position.q, current_position.r):
                    return False
                return board.board.get((hex.q, hex.r)) is not None

            def both_adjacent_occupied(hex, adj_directions):
                return all(is_occupied(Hex(hex.q + dq, hex.r + dr)) for (dq, dr) in adj_directions)

            if direction == 'N':
                return not both_adjacent_occupied(piece_position, [directions['NW'], directions['NE']])
            elif direction == 'NW':
                return not both_adjacent_occupied(piece_position, [directions['N'], directions['SW']])
            elif direction == 'SW':
                return not both_adjacent_occupied(piece_position, [directions['NW'], directions['S']])
            elif direction == 'S':
                return not both_adjacent_occupied(piece_position, [directions['SW'], directions['SE']])
            elif direction == 'SE':
                return not both_adjacent_occupied(piece_position, [directions['NE'], directions['S']])
            elif direction == 'NE':
                return not both_adjacent_occupied(piece_position, [directions['N'], directions['SE']])
            else:
                return False

        def get_valid_positions(start, visited):
            if start in visited:
                return []
            valid_positions = []
            for direction, (q, r) in HexUtils.directions.items():
                if freedom_move(start, direction, board):
                    next_pos = Hex(start.q + q, start.r + r)
                    if is_valid_move(start, next_pos, visited):
                        new_visited = visited.copy()
                        new_visited.add((next_pos.q, next_pos.r))
                        valid_positions.append(next_pos)
                        valid_positions.extend(get_valid_positions(next_pos, new_visited))
            return valid_positions

        visited = {(current_position.q, current_position.r)}
        return get_valid_positions(current_position, visited)

    @staticmethod
    def is_connected(position, board_dict, previous_position, current_position):
        # Check if the position is connected to any other piece except the previous position
        for neighbor in HexUtils.hex_neighbors(position):
            if (neighbor.q, neighbor.r) in board_dict and board_dict[(neighbor.q, neighbor.r)] is not None and (
                    neighbor.q, neighbor.r) != (current_position.q, current_position.r):
                # Check if there is an intersection between the neighbor and the previous position
                for prev_neighbor in HexUtils.hex_neighbors(previous_position):
                    if (prev_neighbor.q, prev_neighbor.r) == (neighbor.q, neighbor.r):
                        return True
        return False

    def move(self, current_position, new_position, board, valid_move):
        if new_position in valid_move:
            board.board[(new_position.q, new_position.r)] = self
            board.board[(current_position.q, current_position.r)] = None




#
# if __name__ == "__main__":
#     board = HexBoard(grid_size=25)
#
#     center_hex = Hex(0, 0)
#     bee = QueenBee(0)
#     grasshopper = Grasshopper(0)
#     ant = Ant(1)
#
#     # just example
#     board.place_piece(center_hex, bee)
#     board.place_piece(Hex(-2, 0), grasshopper)
#     board.place_piece(Hex(0,-1), Piece("any" , 0))
#     board.place_piece(Hex(0,-2), Piece("any" , 0))
#     board.place_piece(Hex(-1,-2), Piece("any" , 0))
#     board.place_piece(Hex(-2,-1), Piece("any",0))
#     board.place_piece(Hex(-2,1), Piece("any",0))
#     board.place_piece(Hex(-1,0), Piece("any",0))
#     board.place_piece(Hex(2,-1), Piece("any",0))
#     board.place_piece(Hex(2,0), Piece("any",0))
#     board.place_piece(Hex(1,1), ant)
#     board.place_piece(Hex(1,-1), Piece("any",0))
#     # remove comment and run again to see the move
#     # board.move(Hex(-2, 0), 'N' ,grasshopper)
#     ant.get_valid_moves(Hex(1, 1), board)
#
#     app = HexagonalBoardGUI(board)
#     app.mainloop()

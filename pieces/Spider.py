from os.path import curdir

from hive import Piece, HexUtils, Hex


class Spider(Piece):
    def __init__(self):
        super().__init__("Spider")

    def valid_moves(self, current_position, board):
        if (not HexUtils.is_valid_after_move(current_position, board)):
            return []
        def is_valid_move(start, end, visited):
            if (end.q, end.r) not in board.board:
                print("not on board")
                return False
            if board.board[(end.q, end.r)] is not None:
                print("occupied")
                return False
            if not self.is_connected(end, board.board, start, current_position):
                print("not connected")
                return False
            if (end.q, end.r) in visited:
                print("already visited")
                return False
            return True

        def get_valid_positions(start, steps, visited):
            if steps == 0:
                return [start]
            valid_positions = []
            for direction in HexUtils.directions.values():
                next_pos = Hex(start.q + direction[0], start.r + direction[1])
                if is_valid_move(start, next_pos, visited):
                    new_visited = visited.copy()
                    new_visited.add((next_pos.q, next_pos.r))
                    valid_positions.extend(get_valid_positions(next_pos, steps - 1, new_visited))
            return valid_positions

        visited = {(current_position.q, current_position.r)}
        return get_valid_positions(current_position, 3, visited)

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

    def move(self, current_position, new_position, board):
        if new_position in self.valid_moves(current_position, board) and self.can_move(current_position, board):
            board.board[(new_position.q, new_position.r)] = self
            board.board[(current_position.q, current_position.r)] = None
            return True
        else:
            print("Invalid move")
            return False

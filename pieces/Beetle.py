from hive import Piece , HexUtils , Hex 


class Beetle(Piece) :
    frozenPiece = None
    def __init__(self,color):
        super().__init__('Beetle',color)

    def get_valid_moves(self, hex, board):
        valid_moves = []

        for direction in HexUtils.directions.values():
            new_hex = Hex(hex.q + direction[0], hex.r + direction[1])

            # Check if the new_hex is within the board and unoccupied
            if (new_hex.q, new_hex.r) in board.board :
                
                # Create a copy of the board
                board_copy = board.board.copy()

                # Temporarily move the Queen Bee to the new position
                board_copy[(hex.q, hex.r)] = None
                board_copy[(new_hex.q, new_hex.r)] = self

                # Check if any of the neighboring hexes around the new position are occupied
                neighbors = [
                    (new_hex.q, new_hex.r - 1),
                    (new_hex.q - 1, new_hex.r),
                    (new_hex.q - 1, new_hex.r + 1),
                    (new_hex.q, new_hex.r + 1),
                    (new_hex.q + 1, new_hex.r),
                    (new_hex.q + 1, new_hex.r - 1)
                ]
                if self.frozenPiece is None:
                    # Ensure new position is connected to at least one neighbor
                    if any(board_copy.get(neighbor) is not None for neighbor in neighbors) and self.frozenPiece is None :
                        # Perform a hive connectivity check
                        visited = set()
                        start_hex = next(
                            (pos for pos, piece in board_copy.items() if piece is not None), None
                        )

                        # BFS to check connectivity
                        queue = [start_hex]
                        while queue:
                            current = queue.pop()
                            if current not in visited:
                                visited.add(current)
                                for direction in HexUtils.directions.values():
                                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                                    if neighbor in board_copy and board_copy[neighbor] is not None and neighbor not in visited:
                                        queue.append(neighbor)
                        # Check if all pieces in the hive are connected
                        total_pieces = sum(1 for piece in board_copy.values() if piece is not None)
                        if len(visited) == total_pieces and self.frozenPiece is None:
                            valid_moves.append(new_hex)
                else:
                    valid_moves.append(new_hex)
                # Restore the original board state
                board_copy[(new_hex.q, new_hex.r)] = None
                board_copy[(hex.q, hex.r)] = self

        return valid_moves

    
    
    def move(self, hex, new_hex, board,valid_moves):
        if new_hex in valid_moves:
            # board.board[(new_hex.q, new_hex.r)] = self
            # board.board[(hex.q, hex.r)] = None
            self.move2(hex, new_hex, board,valid_moves)

    # def move(self, current_hex, direction, board):
    #     dir_offset = HexUtils.get_direction(direction)
    #     target_hex = Hex(current_hex.q + dir_offset[0], current_hex.r + dir_offset[1])

    #     for hex in self.get_valid_moves(current_hex, board):
    #         if hex.r==target_hex.r and hex.q==target_hex.q :
    #             if board.board[(target_hex.q, target_hex.r)] == None:
    #                 board.board[(target_hex.q, target_hex.r)] = self
    #                 if self.frozenPiece == None:
    #                     board.board[(current_hex.q, current_hex.r)] = None
    #                 else : 
    #                     board.board[(current_hex.q, current_hex.r)] = self.frozenPiece 
    #                     self.frozenPiece = None

    #             else :
    #                 if self.frozenPiece == None:
    #                     board.board[(current_hex.q, current_hex.r)] = None
    #                 else : 
    #                     board.board[(current_hex.q, current_hex.r)] = self.frozenPiece 
    #                     self.frozenPiece = None
    #                 self.frozenPiece = board.board[(target_hex.q, target_hex.r)]
    #                 board.board[(target_hex.q, target_hex.r)] = self
                    
    #             break
    #         else:
    #             continue


    def move2(self, current_hex, target_hex, board,valid_move):
            # dir_offset = HexUtils.get_direction(direction)
            # target_hex = Hex(current_hex.q + dir_offset[0], current_hex.r + dir_offset[1])

            for hex in valid_move:
                if hex.r==target_hex.r and hex.q==target_hex.q :
                    if board.board[(target_hex.q, target_hex.r)] == None:
                        board.board[(target_hex.q, target_hex.r)] = self
                        if self.frozenPiece == None:
                            board.board[(current_hex.q, current_hex.r)] = None
                        else : 
                            board.board[(current_hex.q, current_hex.r)] = self.frozenPiece 
                            self.frozenPiece = None

                    else :
                        if self.frozenPiece == None:
                            board.board[(current_hex.q, current_hex.r)] = None
                        else : 
                            board.board[(current_hex.q, current_hex.r)] = self.frozenPiece 
                            self.frozenPiece = None
                        self.frozenPiece = board.board[(target_hex.q, target_hex.r)]
                        board.board[(target_hex.q, target_hex.r)] = self
                        
                    break
                else:
                    continue










#Pieces_Queen File
from environment.hive import Piece, HexUtils, Hex
class QueenBee(Piece):
    def __init__(self,color):
        super().__init__('Queen Bee',color)
        #.......
        self.position = None  # Add position attribute

    def set_position(self, q, r):
        self.position = Hex(q, r)


    def get_valid_moves(self, hex, board):
    
        valid_moves = []

        # Check if the Queen Bee is surrounded by five neighbors
        neighbors = [
            (hex.q, hex.r - 1),
            (hex.q - 1, hex.r),
            (hex.q - 1, hex.r + 1),
            (hex.q, hex.r + 1),
            (hex.q + 1, hex.r),
            (hex.q + 1, hex.r - 1)
        ]

        occupied_neighbors = sum(1 for neighbor in neighbors if board.board.get(neighbor) is not None)
        unoccupied_neighbors = [neighbor for neighbor in neighbors if board.board.get(neighbor) is None]

        if occupied_neighbors >= 5:
            return valid_moves  # If surrounded by five neighbors, the Queen Bee cannot move
        
        if len(unoccupied_neighbors) == 2 and occupied_neighbors == 4:
            n1, n2 = unoccupied_neighbors
            n1_neighbors = [
                (n1[0], n1[1] - 1),
                (n1[0] - 1, n1[1]),
                (n1[0] - 1, n1[1] + 1),
                (n1[0], n1[1] + 1),
                (n1[0] + 1, n1[1]),
                (n1[0] + 1, n1[1] - 1)
            ]
            # If the two unoccupied neighbors are neighbors to each other, the Queen Bee cannot move
            if n2 not in n1_neighbors:
                return valid_moves

        for direction in HexUtils.directions.values():
            new_hex = Hex(hex.q + direction[0], hex.r + direction[1])

            # Check if the new_hex is within the board and unoccupied
            if (new_hex.q, new_hex.r) in board.board and board.board[(new_hex.q, new_hex.r)] is None:
                
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

                new_neighbors = [
                (new_hex.q, new_hex.r - 1),
                (new_hex.q - 1, new_hex.r),
                (new_hex.q - 1, new_hex.r + 1),
                (new_hex.q, new_hex.r + 1),
                (new_hex.q + 1, new_hex.r),
                (new_hex.q + 1, new_hex.r - 1)
            ]
                

                new_occupied_neighbors = sum(1 for neighbor in new_neighbors if board_copy.get(neighbor) is not None)
                new_unoccupied_neighbors = [neighbor for neighbor in new_neighbors if board_copy.get(neighbor) is None]



                # Exclude the move if it results in five neighbors
                if new_occupied_neighbors >= 5:
                    return valid_moves

                if len(new_unoccupied_neighbors)==2 and new_occupied_neighbors ==4 :
                    n1_new, n2_new = new_unoccupied_neighbors
                    n1_new_neighbors = [
                    (n1_new[0], n1_new[1] - 1),
                    (n1_new[0] - 1, n1_new[1]),
                    (n1_new[0] - 1, n1_new[1] + 1),
                    (n1_new[0], n1_new[1] + 1),
                    (n1_new[0] + 1, n1_new[1]),
                    (n1_new[0] + 1, n1_new[1] - 1)
                    ]
            # If the two unoccupied neighbors are neighbors to each other, the Queen Bee cannot move
                    if n2_new not in n1_new_neighbors:
                        return valid_moves
                    
                if len(new_unoccupied_neighbors)==3 and new_occupied_neighbors ==3 :
                    n_new1,n_new2,n_new3 = new_unoccupied_neighbors
                    n_new1_neighbors = [
                    (n_new1[0], n_new1[1] - 1),
                    (n_new1[0] - 1, n_new1[1]),
                    (n_new1[0] - 1, n_new1[1] + 1),
                    (n_new1[0], n_new1[1] + 1),
                    (n_new1[0] + 1, n_new1[1]),
                    (n_new1[0] + 1, n_new1[1] - 1)
                    ]
                    n_new2_neighbors = [
                    (n_new2[0], n_new2[1] - 1),
                    (n_new2[0] - 1, n_new2[1]),
                    (n_new2[0] - 1, n_new2[1] + 1),
                    (n_new2[0], n_new2[1] + 1),
                    (n_new2[0] + 1, n_new2[1]),
                    (n_new2[0] + 1, n_new2[1] - 1)
                    ]
                    n_new3_neighbors = [
                    (n_new3[0], n_new3[1] - 1),
                    (n_new3[0] - 1, n_new3[1]),
                    (n_new3[0] - 1, n_new3[1] + 1),
                    (n_new3[0], n_new3[1] + 1),
                    (n_new3[0] + 1, n_new3[1]),
                    (n_new3[0] + 1, n_new3[1] - 1)
                    ]
                    if n_new2 not in n_new1_neighbors and n_new3 not in n_new1_neighbors  :
                        if Hex(n_new1[0],n_new1[1]) == hex:
                            return valid_moves
                    elif n_new1 not in n_new2_neighbors and n_new3 not in n_new2_neighbors:
                        if Hex(n_new2[0],n_new2[1]) == hex:
                            return valid_moves
                    elif n_new1 not in n_new3_neighbors and n_new2 not in n_new3_neighbors:
                        if Hex(n_new3[0],n_new3[1]) == hex:
                            return valid_moves
                    
                if len(new_unoccupied_neighbors)==4 and new_occupied_neighbors ==2 :
                    n_new11,n_new22,n_new33,n_new44 = new_unoccupied_neighbors
                    n_new11_neighbors = [
                    (n_new11[0], n_new11[1] - 1),
                    (n_new11[0] - 1, n_new11[1]),
                    (n_new11[0] - 1, n_new11[1] + 1),
                    (n_new11[0], n_new11[1] + 1),
                    (n_new11[0] + 1, n_new11[1]),
                    (n_new11[0] + 1, n_new11[1] - 1)
                    ]
                    n_new22_neighbors = [
                    (n_new22[0], n_new22[1] - 1),
                    (n_new22[0] - 1, n_new22[1]),
                    (n_new22[0] - 1, n_new22[1] + 1),
                    (n_new22[0], n_new22[1] + 1),
                    (n_new22[0] + 1, n_new22[1]),
                    (n_new22[0] + 1, n_new22[1] - 1)
                    ]
                    n_new33_neighbors = [
                    (n_new33[0], n_new33[1] - 1),
                    (n_new33[0] - 1, n_new33[1]),
                    (n_new33[0] - 1, n_new33[1] + 1),
                    (n_new33[0], n_new33[1] + 1),
                    (n_new33[0] + 1, n_new33[1]),
                    (n_new33[0] + 1, n_new33[1] - 1)
                    ]
                    n_new44_neighbors = [
                    (n_new44[0], n_new44[1] - 1),
                    (n_new44[0] - 1, n_new44[1]),
                    (n_new44[0] - 1, n_new44[1] + 1),
                    (n_new44[0], n_new44[1] + 1),
                    (n_new44[0] + 1, n_new44[1]),
                    (n_new44[0] + 1, n_new44[1] - 1)
                    ]
                    if n_new22 not in n_new11_neighbors and n_new33 not in n_new11_neighbors and n_new44 not in n_new11_neighbors  :
                        if Hex(n_new11[0],n_new11[1]) == hex:
                            return valid_moves
                    elif n_new11 not in n_new22_neighbors and n_new33 not in n_new22_neighbors and n_new44 not in n_new22_neighbors :
                        if Hex(n_new22[0],n_new22[1]) == hex:
                            return valid_moves
                    elif n_new11 not in n_new33_neighbors and n_new22 not in n_new33_neighbors and n_new44 not in n_new33_neighbors :
                        if Hex(n_new33[0],n_new33[1]) == hex:
                            return valid_moves
                    elif n_new11 not in n_new44_neighbors and n_new22 not in n_new44_neighbors and n_new33 not in n_new44_neighbors :
                        if Hex(n_new44[0],n_new44[1]) == hex:
                            return valid_moves


                # Ensure new position is connected to at least one neighbor
                if any(board_copy.get(neighbor) is not None for neighbor in neighbors):
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
                    if len(visited) == total_pieces:
                        valid_moves.append(new_hex)

                # Restore the original board state
                board_copy[(new_hex.q, new_hex.r)] = None
                board_copy[(hex.q, hex.r)] = self

        return valid_moves



    def move(self, hex, new_hex, board,valid_moves):
        if new_hex in valid_moves:
            board.board[(new_hex.q, new_hex.r)] = self
            board.board[(hex.q, hex.r)] = None
    
    

#AI_agent(part 1)
import copy
from environment.hive import Piece, HexBoard, Hex, HexUtils
from pieces import Ant
from pieces import Beetle
from pieces import QueenBee
from pieces import Grasshopper
from pieces import Spider


def evaluate_board(board, player):
    #   if player is -1 then its black turn,1 is white turn
    from math import sqrt

    def count_valid_moves(piece, position):
        """Count valid moves for the specified piece."""
        return len(piece.get_valid_moves(position, board)) if piece else 0

    def calculate_distance(pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    black_queen_pos = None
    white_queen_pos = None

    if board and board.board:  # Ensure board is not None and has a 'board' attribute
        for (q, r), piece in board.board.items():
            if piece and piece == "Queen Bee":
                if piece.color == 1:  # Black Queen
                    black_queen_pos = Hex(q, r)
                elif piece.color == 0:  # White Queen
                    white_queen_pos = Hex(q, r)
    else:
        raise ValueError("The board is not properly initialized.")

    # Get the queen pieces
    black_queen = board.get_piece(black_queen_pos) if black_queen_pos else None
    white_queen = board.get_piece(white_queen_pos) if white_queen_pos else None

    # Calculate mobility scores
    if player == -1:  # black
        opponent_queen_mobility = count_valid_moves(white_queen,white_queen_pos) if white_queen else 0
        own_queen_mobility = count_valid_moves(black_queen,black_queen_pos ) if black_queen else 0

        # Calculate proximity of player pieces to opponent player queen
        proximity_score = 0
        if white_queen:
            for (q, r), piece in board.board.items():
                if piece and piece.color == 1:  # Black's pieces
                    distance = calculate_distance((q, r), (white_queen_pos.q,white_queen_pos.r) )
                    proximity_score += max(0, (10 - distance))  # Reward closer pieces
    else:  # white
        opponent_queen_mobility = count_valid_moves(black_queen,black_queen_pos)if black_queen else 0
        own_queen_mobility = count_valid_moves(white_queen, white_queen_pos) if white_queen else 0

        proximity_score = 0
        if black_queen:
            for (q, r), piece in board.board.items():
                if piece and piece.color == 0:  # White's pieces
                    distance = calculate_distance((q, r), (black_queen_pos.q,black_queen_pos.r))
                    proximity_score += max(0, 10 - distance)  # Reward closer pieces

    # use piece values if queens are not yet used
    piece_value_score = sum(piece.value for (q, r), piece in board.board.items() if piece is not None)

    # Calculate the final score
    score = 0
    if white_queen or black_queen:
        # Use mobility and proximity if queens are present
        score -= opponent_queen_mobility * 10  #heuristic to Penalize opponent queen mobility
        score += own_queen_mobility * 5  #heuristic to Reward AI queen mobility
        score += proximity_score  # Add proximity score
    else:
        #piece value-based scoring
        score += piece_value_score

    return score


def get_all_possible_moves(board, player):
    """
    Get all possible moves for a given player.
    Args:
    - board (Board): The game board object containing all pieces and their positions.
    - player: (1 for white, -1 for black).

    Returns:
    - list of lists: List[List[CurrentHex, TargetHex, Piece]]
    """
    all_moves = []

    for (q, r), piece in board.board.items():
        if piece is None:  # Skip this iteration if the piece is None
            continue
        if piece and ((player == -1 and piece.color == 1) or (player == 1 and piece.color == 0)):
            current_hex = Hex(q, r)
            valid_moves = piece.get_valid_moves(current_hex, board)
            for target_hex in valid_moves:
                all_moves.append([current_hex, target_hex,piece])

    if not all_moves:
        print("No valid moves for pieces.")
    return all_moves


def game_over(board):
    """
       Check if the game is over by determining if either queen is surrounded.

       Args:
           board (HexBoard): The current board state.

       Returns:
           int: 0 if the game is ongoing, 1 if Black queen is surrounded,
                2 if White queen is surrounded, 3 if both queens are surrounded.
    """

    def is_surrounded(hex):
        neighbors = HexUtils.hex_neighbors(hex)
        return all(board.get_piece(neighbor) is not None for neighbor in neighbors)

    black_queen = None
    white_queen = None

    if board and board.board:  # Ensure board is not None and has a 'board' attribute
        for (q, r), piece in board.board.items():
            if piece is None:
                continue
            if piece and piece.name == "Queen Bee":
                if piece.color == 1:  # Black Queen
                    black_queen = Hex(q, r)
                elif piece.color == 0:  # White Queen
                    white_queen = Hex(q, r)
    else:
        raise ValueError("The board is not properly initialized.")

    black_surrounded = black_queen and is_surrounded(black_queen)
    white_surrounded = white_queen and is_surrounded(white_queen)

    if black_surrounded and white_surrounded:
        return 3
    elif black_surrounded:
        return 1
    elif white_surrounded:
        return 2
    else:
        return False


def minmax(board,player, depth, is_maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board,player)

    if is_maximizing_player:  # AI's turn (Black)
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, player):  # -1 is Black
            new_board = copy.deepcopy(board)
            start_pos,end_pos,piece = move
            new_board = new_board.move(start_pos,end_pos,board,piece.get_valid_moves(start_pos,board))
            eval = minmax(new_board,(-1*player), depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:  # Opponent's turn (White)
        min_eval = float('inf')
        for move in get_all_possible_moves(board, player):  # 1 is White
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            eval = minmax(new_board,(-1*player), depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def alpha_beta(board, player, depth, alpha, beta, is_maximizing_player):
    """
    Minmax function with alpha-beta pruning.
    """
    if depth == 0 or game_over(board):
        return evaluate_board(board, player)

    if is_maximizing_player:  # AI's turn (Black)
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, player):  # -1 is Black
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            eval = alpha_beta(new_board, (-1 * player), depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Prune
                break
        return max_eval
    else:  # Opponent's turn (White)
        min_eval = float('inf')
        for move in get_all_possible_moves(board, player):  # 1 is White
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            eval = alpha_beta(new_board, (-1 * player), depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Prune
                break
        return min_eval


#AI_agent(part 2)

def alpha_beta_iterative_deepening(board, player, max_depth, time_limit=5):
    import time
    """
    Args:
        board: The game board state.
        player: The player (-1 for AI, 1 for opponent).
        max_depth: The maximum depth to search.
        time_limit: Time limit in seconds for the iterative deepening.

    Returns:
        A tuple containing the best move and its value.
    """
    alpha = float('-inf')
    beta = float('inf')
    best_move = None
    best_value = float('-inf')
    start_time = time.time()

    for depth in range(1, max_depth + 1):
        print(f"Searching at depth {depth}...")
        current_best_move = None
        current_best_value = float('-inf')

        for move in get_all_possible_moves(board, player):
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            move_value = alpha_beta(new_board, (-1*player), depth - 1, alpha, beta, False)

            if move_value > current_best_value:
                current_best_value = move_value
                current_best_move = move

            alpha = max(alpha, current_best_value) if player == -1 else alpha

            # Time check
            if time_limit and time.time() - start_time > time_limit:
                print("Time limit reached during depth", depth)
                return best_move

        # Update best result
        if current_best_move is not None:
            best_move = current_best_move
            best_value = current_best_value

        # Exit if no time left
        if time_limit and time.time() - start_time > time_limit:
            print("Time limit reached.")
            break

    return best_move, best_value


def agent_best_next_move(board, depth, player, algorithm="alpha_beta_iterative"):
    """
    find the best move using one of three algorithms:
    - Minmax
    - Minmax with Alpha-Beta Pruning
    - Alpha-Beta Pruning with Iterative Deepening

    Args:
        board: The game board state.
        depth: The maximum search depth.
        player: The player (-1 for AI(black), 1 for opponent).
        algorithm: The algorithm to use ("minmax", "alpha_beta", "alpha_beta_iterative").

    Returns:
        The best move.
    """
    if algorithm == "minmax":
        best_move = None
        best_value = float('-inf')
        for move in get_all_possible_moves(board, player):
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            move_value = minmax(new_board,(-1*player), depth - 1, False)

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    elif algorithm == "alpha_beta":
        best_move = None
        best_value = float('-inf') if player == -1 else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in get_all_possible_moves(board, player):
            new_board = copy.deepcopy(board)
            start_pos, end_pos, piece = move
            new_board = new_board.move(start_pos, end_pos, board, piece.get_valid_moves(start_pos, board))
            move_value = alpha_beta(new_board,(-1*player) ,depth - 1, alpha, beta, False)

            if move_value > best_value:
                best_value = move_value
                best_move = move

            alpha = max(alpha, best_value) if player == -1 else alpha


        return best_move

    elif algorithm == "alpha_beta_iterative":
        best_move, _ = alpha_beta_iterative_deepening(board, player, max_depth=depth)
        return best_move

    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
"""
Manual testing 
"""
# def main():
#     print("hello")
#     # Create a HexBoard instance
#     board = HexBoard(5)
#
#     # Initialize pieces with name and color (0 for white, 1 for black)
#     black_queen = QueenBee(1)  # Black Queen
#     white_queen = QueenBee(0)  # White Queen
#     white_beetle = Beetle(0)
#     black_beetle = Beetle(1)  # Black Beetle
#     white_hopper = Grasshopper(0)  # White Hopper
#     white_spider = Spider(0)
#     black_hopper = Grasshopper(1)
#     black_hopper1 = Grasshopper(1)
#     black_spider = Spider(1)
#     black_ant = Ant(1)
#     a = Hex(0,0)
#     b = Hex(0,1)
#     c = Hex(0, -1)
#     d = Hex(-1,1)
#     e = Hex(0, -2)
#     f = Hex(0, -3)
#     # Place pieces on the board
#     board.place_piece(a, white_spider)
#     board.place_piece(c, black_beetle)
#     board.place_piece(d, white_queen)
#     board.place_piece(e, black_queen)
#     # board.place_piece( b, white_hopper)
#     board.place_piece(f, black_ant)
#
#     print(black_ant.get_valid_moves(f,board))
#
#     # Display the initial board state
#     print("\nInitial Board State:")
#     board.display()
#
#     # Set parameters for the agent's algorithm
#     max_depth = 2  # Depth limit for search
#     current_player = -1  # Black's turn
#     algorithm = "alpha_beta"  # Algorithm choice
#
#     # Find the best move
#     best_move = agent_best_next_move(board, max_depth, current_player, algorithm)
#
#     # Apply the best move if one is found
#     if best_move:
#         print("\nBest Move Found:", best_move)
#         board.make_move(best_move)
#         print("\nBoard After Move:")
#         board.display()
#     else:
#         print("\nNo valid moves found. Game over.")
#
# if __name__ == "__main__":
#     main()

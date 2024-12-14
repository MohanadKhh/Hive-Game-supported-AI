def minmax(board, depth, is_maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if is_maximizing_player:  # AI's turn (Black)
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, -1):  # -1 is Black
            new_board = copy.deepcopy(board)
            new_board = new_board.move_piece(move)
            eval = minmax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:  # Opponent's turn (White)
        min_eval = float('inf')
        for move in get_all_possible_moves(board, 1):  # 1 is White
            new_board = copy.deepcopy(board);
            new_board = new_board.move_piece(move)
            eval = minmax(new_board, depth - 1, True)
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
            new_board = new_board.move_piece(move)
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
            new_board = new_board.move_piece(move)
            eval = alpha_beta(new_board, (-1 * player), depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Prune
                break
        return min_eval


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
    best_value = float('-inf') if player == -1 else float('inf')
    start_time = time.time()

    for depth in range(1, max_depth + 1):
        print(f"Searching at depth {depth}...")
        current_best_move = None
        current_best_value = float('-inf') if player == -1 else float('inf')

        for move in get_all_possible_moves(board, player):
            new_board = copy.deepcopy(board)
            new_board = new_board.make_move(move)
            move_value = alpha_beta(new_board, -player, depth - 1, alpha, beta, player != -1)

            if (player == -1 and move_value > current_best_value) or (player == 1 and move_value < current_best_value):
                current_best_value = move_value
                current_best_move = move

            alpha = max(alpha, current_best_value) if player == -1 else alpha
            beta = min(beta, current_best_value) if player == 1 else beta

            # Time check
            if time.time() - start_time > time_limit:
                print("Time limit reached.")
                return best_move, best_value

        # Update best result
        if current_best_move:
            best_move = current_best_move
            best_value = current_best_value

        # Exit if no time left
        if time.time() - start_time > time_limit:
            print("Time limit exceeded during depth search.")
            break

    return best_move, best_value
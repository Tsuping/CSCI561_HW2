def Minmax(curr_board, prev_board, depth, alpha, beta, next_player):
    if depth == 0:
        return 
    suggest_moves = []
    highest_score = 0
    current_board_copy = copy.deepcopy(curr_board)
    for moves in find_valid_move(curr_board, prev_board, next_player):
        next_state_board = next_state_movement(curr_board, moves, next_player)
        dfs_search_min = -1 * min_part(next_state_board, current_board_copy, depth-1, alpha, beta, find_opponent(next_player))
        if dfs_search_min > highest_score or not suggest_moves:
            highest_score = dfs_search_min
            alpha = highest_score
            suggest_moves = [moves]
        elif dfs_search_min == highest_score:
            suggest_moves.append(moves)

    return suggest_moves
    


def min_part(curr_board, prev_board, depth, alpha, beta, next_player):
    heuristic_value = find_rewards(curr_board, next_player)
    if depth == 0:
        return heuristic_value
    curr_board_copy = copy.deepcopy(curr_board)
    for moves in find_valid_move(curr_board, prev_board, next_player):
        next_state_board = next_state_movement(curr_board, moves, next_player)
        current_value = max_part(next_state_board, curr_board_copy, depth - 1, alpha, beta, next_player)
        values = -1 * current_value
        if values > heuristic_value:
            heuristic_value = values
        players_turn = -1 * heuristic_value

        if players_turn < alpha:
            return heuristic_value
        if heuristic_value > beta:
            beta = heuristic_value
        

    return heuristic_value

def max_part(curr_board, prev_board, depth, alpha, beta, next_player):
    heuristic_value = find_rewards(curr_board, next_player)
    if depth == 0:
        return heuristic_value
    curr_board_copy = copy.deepcopy(curr_board)
    for moves in find_valid_move(curr_board, prev_board, next_player):
        next_state_board = next_state_movement(curr_board, moves, next_player)
        current_value = min_part(next_state_board, curr_board_copy, depth - 1, alpha, beta, next_player)
        values = -1 * current_value
        if values > heuristic_value:
            heuristic_value = values
        opponent = -1 * heuristic_value
        if opponent < beta:
            return heuristic_value
        if heuristic_value > alpha:
            alpha = heuristic_value

    return heuristic_value


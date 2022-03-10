import copy
import os
import time
import random
input = "input.txt"


def find_opponent(val):
    return 3 - val

def read_input(file):
    Board_size = 5
    info = []
    with open(file) as F:
        for lines in F.readlines():
            info.append(lines.strip())
    player = int(info[0])
    prev_board = []
    current_board = []
    for i in range(1, Board_size + 1):
        prev_board.append([int(value) for value in info[i]])
    for i in range(Board_size + 1, len(info)):
        current_board.append([int(value) for value in info[i]])
    return player, prev_board, current_board



def write_output(output_file, move):
    with open(output_file, 'w') as F:
        for item in move:
            F.write(item + " ")

def delete_tile(board, dead_piece_list):
    for piece in dead_piece_list:
        board[piece[0]][piece[1]] = 0
    return board


def ko_rule(current_board, prev_board):
    for i in range(5):
        for j in range(5):
            if current_board[i][j] != prev_board[i][j]:
                return False

    return True

def find_liberty(board, row, col):
    count = 0
    for point in find_ally_cluster(board, row, col):
        neighboring = find_neighbor(board, point[0], point[1])
        for check in neighboring:
            if board[check[0]][check[1]] == 0:
                count += 1
    return count

def find_dead_tile(board, player):
    dead_tile = list()
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                if not find_liberty(board, i, j) and (i,j) not in dead_tile:
                    dead_tile.append((i,j))
    return dead_tile



def find_neighbor(board, i, j):
    neighbor = []
    board = delete_dead_tiles(board, (i, j))
    if i > 0:
        neighbor.append((i-1,j))
    if i < 4:
        neighbor.append((i+1,j))
    if j > 0:
        neighbor.append((i, j-1))
    if j < 4:
        neighbor.append((i, j+1))
    return neighbor


def find_neighbor_ally(board, i, j):
    allies = []
    for stones in find_neighbor(board, i, j):
        if board[i][j] == board[stones[0]][stones[1]]:
            allies.append(stones)
    return allies


def find_ally_cluster(board, i, j):
    ally_cluster = list()
    queue = []
    queue.append((i, j))
    while queue:
        node = queue.pop()
        ally_cluster.append((node[0], node[1]))
        for neighbor in find_neighbor_ally(board, node[0], node[1]):
            if neighbor not in queue and neighbor not in ally_cluster:
                queue.append(neighbor)
    return ally_cluster

def delete_dead_tiles(board, player):
    check = find_dead_tile(board, player)
    if len(check) == 0:
        return board
    new_board = delete_tile(board, check)
    return new_board


def find_all_move(curr_board): 
    list = []
    for i in range(5):
        for j in range(5):
            if curr_board[i][j] == 0:
                list.append((i, j))
    return list

def find_valid_move(curr_board, prev_board, player):
    moves_list = find_all_move(curr_board)

    legal_move = []
    for move in moves_list:
        row = move[0]
        col = move[1]
        current_board_copy = copy.deepcopy(curr_board)
        current_board_copy[row][col] = player
        next_board_copy = copy.deepcopy(current_board_copy)
        liberties_check = find_liberty(current_board_copy, row, col)
        if liberties_check == 0:
            dead_tile = find_dead_tile(current_board_copy, find_opponent(player))
            if dead_tile:
                current_board_copy = delete_dead_tiles(current_board_copy, find_opponent(player))
            liberties_check = find_liberty(current_board_copy, row, col)
        if liberties_check >= 1:
            dead_tile = find_dead_tile(next_board_copy, find_opponent(player))
            if  dead_tile:
                next_board_copy = delete_dead_tiles(next_board_copy, find_opponent(player))
            if dead_tile != None and ko_rule(next_board_copy, prev_board) == True:
                print("KO violation")
            else:
                legal_move.append(move)
    return legal_move 



def next_state_movement(board, position, player):
    new_board = copy.deepcopy(board)
    new_board[position[0]][position[1]] = player
    new_board = delete_dead_tiles(new_board, find_opponent(player))
    return new_board

def find_rewards(board, player_type):
    col = 0
    board_size = len(board[col])
    komi = board_size/2
    our_agent = 0
    opponent_agent = 0
    seen_player = []
    seen_opponent = []
    our_agent_potential_reward = 0
    opponent_agent_potnetial_reward = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                our_agent += 1
                seen_player.append([i, j])

            elif board[i][j] == find_opponent(player):
                opponent_agent += 1
                seen_opponent.append([i, j])
    for piece in seen_player:
        ally_cluster = find_ally_cluster(board, piece[0], piece[1])
        liberty_count = find_liberty(board, piece[0], piece[1])
        our_agent_potential_reward += (our_agent + liberty_count)
        for word in ally_cluster:
            if word in seen_player:
                seen_player.pop(word)

    for piece_op in seen_opponent:
        ally_cluster = find_ally_cluster(board, piece_op[0], piece_op[1])
        liberty_count = find_liberty(board, piece_op[0], piece_op[1])
        opponent_agent_potnetial_reward += (opponent_agent + liberty_count)
        for word in ally_cluster:
            if word in seen_opponent:
                seen_opponent.pop(word)

    value = our_agent_potential_reward - opponent_agent_potnetial_reward
    if player == 1:
        value -= komi
    if player_type == player:
        return value
    else:
        return -1 * value

def minmax(curr_board, prev_board, depth, alpha, beta, player, isMax):
    if depth == 0:
        return find_rewards(curr_board, player), None
    
    valid_move = find_valid_move(curr_board, prev_board, player)
    random.shuffle(valid_move)

    if valid_move == None:
        current_move = ["PASS"]
        return 0, current_move
    
    current_move = None

    if isMax == True:
        v = -1000
        for move in valid_move:
            
            current_board_copy = copy.deepcopy(curr_board)
            next_state_board = next_state_movement(current_board_copy, move,player)
            score = minmax(next_state_board, curr_board, depth - 1, alpha, beta, find_opponent(player), False)
            if v < score[0]:
                v = score[0]
                alpha = max(v, alpha)
                current_move = [move]
            if alpha >= beta:
                break
        if current_move == None:
            return v, None
        return v, current_move

    else:
        v = 1000
        for move in valid_move:
            current_board_copy = copy.deepcopy(curr_board)
            next_state_board = next_state_movement(current_board_copy, move, player)
            score = minmax(next_state_board, curr_board, depth - 1, alpha, beta, find_opponent(player), True)
            if v > score[0]:
                v = score[0]
                beta = min(v, beta)
                current_move = [move]
            if alpha >= beta:
                break
        if current_move == None:
            return v, None
        return v, current_move


player, prev_board, current_board = read_input(input)

f2 = open("output.txt", "w+")
count = 0
for i in range(5):
    for j in range(5):
        if current_board[i][j] != 0:
            count += 1
if count == 0 and player == 1:
    moves = [(2,2)]

    
move = minmax(current_board, prev_board, 2, -1000, 1000, player, True)
moves = move[1]
            
if moves == None:

    f2.write("PASS")
else:
    rand_best = random.choice(moves)
    f2.write("%d%s%d" % (rand_best[0], ",", rand_best[1]))
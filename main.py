import copy
import os



input = "input.txt"

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

player, prev_board, current_board = read_input(input)

def write_output(output_file, move):
    with open(output_file, 'w') as F:
        F.write(move)

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

def good_move(curr_board, prev_board, player, i, j):
    if curr_board[i][j] != 0:
        return False
    copy_board = copy.deepcopy(curr_board)
    copy_board[i][j] = player
    dead_anemy_tile = find_dead_tile(copy_board, 3 - player)
    copy_board = delete_dead_tiles(copy_board, 3 - player)
    if find_liberty(copy_board, i, j) >= 1 and not (dead_anemy_tile and ko_rule(copy_board, prev_board)):
        return True


def find_valid_move(curr_board, prev_board, player):
    moves = []
    for i in range(5):
        for j in range(5):
            if good_move(curr_board, prev_board, player, i, j):
                moves.append((i, j))
    return moves












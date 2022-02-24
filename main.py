import os


input = "input.txt"

def read_input(file):
    Board_size = 5
    info = []
    with open(file) as F:
        for lines in F.readlines():
            info.append(lines.strip())
    player = info[0]
    prev_board = []
    current_board = []
    for i in range(1, Board_size + 1):
        prev_board.append([int(value) for value in info[i]])
    for i in range(Board_size + 1, len(info)):
        current_board.append([int(value) for value in info[i]])
    return player, prev_board, current_board

player, prev_board, current_board = read_input(input)
print(player)

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

def find_dead_tile(board, player):
    dead_tile = list()
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                if find_liberty(board, i, j) == 0 and (i,j) not in dead_tile:
                    dead_tile.append((i,j))
    return dead_tile

def find_neighbor(board, i, j):
    neighbor = []
    if i > 0:
        neighbor.append((i-1,j))
    if i < 5:
        neighbor.append((i + 1,j))
    if j > 0:
        neighbor.append((i, j - 1))
    if j < 5:
        neighbor.append((i, j + 1))
    return neighbor


def find_neighbor_ally(board, i, j):
    allies = []
    for stones in find_neighbor(board, i, j):
        print(stones)
        if board[i][j] == board[stones[0]][stones[1]]:
            allies.append(stones)
    return allies



def find_liberty(board, row, col):
    count = 0
    #Need one more loop(function) to check the adjacent ally tile and everything below this will be include in this loop
    neighboring = find_neighbor(board, row, col)
    for check in neighboring:
        if board[check[0]][check[1]] == 0:
            count += 1
    return count

print(find_neighbor_ally(current_board, 0, 2))



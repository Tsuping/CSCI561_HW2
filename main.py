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
        for value in info[i]:
            prev_board.append(int(value))
    for i in range(Board_size + 1, len(info)):
        for value in info[i]:
            current_board.append(int(value))
    return player, prev_board, current_board

player, prev_board, current_board = read_input(input)

def write_output(output_file, move):
    with open(output_file, 'w') as F:
        F.write(move)



import copy

def get_data():
    with open("data.txt", "r") as f:
        data = f.read()
    return data

patterns = [
    [[0, 0, 1, 1, 1, 1, 0]],
    
    [[0, 0, 0, 1, 0, 0, 0],
     [0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 1, 0, 0, 0]],

    [[0, 0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 1, 0, 0],
     [0, 0, 1, 1, 1, 0, 0]],

    [[0, 0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0]],

    [[0, 0, 1, 1, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 0]]
]


empty_space = [[0 for _ in range(7)] for __ in range(3)]


def print_board(board):
    for line in board:
            for block in line:
                print("#" if block == 2 else "@" if block == 1 else ".", end = "")
            print("")


def move_right(board):
    old_board = [list(i) for i in board] # If the pieces can't move, just return the old board
    for line_num, line in enumerate(board[:100]):
        for rock_num in range(len(line) - 1, -1, -1):
            if line[rock_num] == 1:
                check_line = line + [0] # Avoid index errors
                if rock_num == len(line) - 1 or check_line[rock_num + 1] == 2:
                    #print("No move")
                    return old_board
                line[rock_num + 1] = 1
                line[rock_num] = 0
        board[line_num] = line
    return board


def move_left(board):
    old_board = [list(i) for i in board] # If the pieces can't move, just return the old board
    for line_num, line in enumerate(board[:100]):
        for rock_num in range(len(line)):
            if line[rock_num] == 1:
                if rock_num == 0 or line[rock_num - 1] == 2:
                    return old_board
                line[rock_num - 1] = 1
                line[rock_num] = 0
        board[line_num] = line
    return board


def convert(num): # Convert rocks on board to be solid
    if num == 1:
        return 2
    return num


def board_moving(board):
    for line in board[:100]:
        for rock in line:
            if rock == 1:
                return True
    return False

def move_down(board):
    old_board = [list(i) for i in board] # To be returned if no movement - change all 1s to 2s though!!
    for line_num in range(len(board) - 1, -1, -1):
        for rock_pos, rock in enumerate(board[line_num]):
            if board[line_num][rock_pos] == 1:
                if board[line_num + 1][rock_pos] == 2:
                    for old_line_num in range(len(old_board)):
                        old_board[old_line_num] = [convert(i) for i in old_board[old_line_num]]
                    return old_board
                board[line_num+1][rock_pos] = 1
                board[line_num][rock_pos] = 0
    return board


def strip_board(board):
    for line in board:
        if not all([i == 0 for i in line]):
            return board
        board = board[1:]


def shorten_board(board):
    #blocked = [False for _ in range(7)]
    for line_num, line in enumerate(board):
        #for position in range(len(line)):
            #if line[position] == 2:
                #blocked[position] = True
        #if all(blocked):
        if all([i == 2 for i in line]):
            return board[:line_num + 1], len(board) - (line_num + 1) # New board, rows lost
    return board, 0


def main():
    total = 0
    jets = get_data()
    board = [[2, 2, 2, 2, 2, 2, 2]] # 0 = empty, 1 = moving, 2 = solid
    #print(data)
    jet_index = 0
    #for pattern in patterns:
        #for line in pattern:
            #for block in line:
                #print("#" if block else ".", end = "")
            #print("")
        #print("\n")
    block_num = 0
    while block_num < 2023:
        if not board_moving(board):
            #if block_num % 100 == 0:
                #print(block_num)
            if block_num == 2022:
                break
            board = strip_board(board)
            board = [list(i) for i in patterns[block_num % len(patterns)]] + [list(i) for i in empty_space] + board
            block_num += 1
            #print_board(board)
            #input("Added pattern\n")
        if jets[jet_index] == "<":
            board = move_left(board)
        elif jets[jet_index] == ">":
            board = move_right(board)
        jet_index += 1
        jet_index %= len(jets)
        #print_board(board)
        #input("Moved left/right\n")
        board = move_down(board)
        board, extra_rows = shorten_board(board)
        #print_board(board)
        total += extra_rows
        #print_board(board)
        #input("Moved down\n")

    print(f"Part 1: {len(strip_board(board)) + total - 1}")

    cache = [] # Cache format = {[first 30 rows, block_num, jet index] : current_total}
    totals = []
    total = 0
    jets = get_data()
    board = [[2, 2, 2, 2, 2, 2, 2]] # 0 = empty, 1 = moving, 2 = solid
    #print(data)
    jet_index = 0
    #for pattern in patterns:
        #for line in pattern:
            #for block in line:
                #print("#" if block else ".", end = "")
            #print("")
        #print("\n")
    block_num = 0
    extra_blocks = 0
    extra_blocks_done = 0
    while True:
        if not board_moving(board):
            #if block_num % 100 == 0:
                #print(block_num)
            if extra_blocks:
                extra_blocks_done += 1
                if extra_blocks_done >= extra_blocks:
                    #print(temp_totals2, len(strip_board(board)) + total - 1)
                    extra_length = (len(strip_board(board)) + total - 1) - temp_totals2
                    final_final_total = extra_length + initial_final_total
                    #print(final_final_total)
                    break
            else:
                if [board[:30], block_num % len(patterns), jet_index] in cache:
                    #print("2nd Block num:", block_num, "2nd total:", len(strip_board(board)) + total - 1, "1st Block num, 1st total:", totals[cache.index([board[:30], block_num % len(patterns), jet_index])], cache.index([board[:30], block_num % len(patterns), jet_index]))
                    temp_totals = totals[cache.index([board[:30], block_num % len(patterns), jet_index])]
                    temp_totals2 = len(strip_board(board)) + total - 1
                    initial_final_total = temp_totals[1] + (temp_totals2 - temp_totals[1])*((1000000000000 - temp_totals[0])//(block_num - temp_totals[0]))
                    extra_blocks = (1000000000000 - temp_totals[0])%(block_num - temp_totals[0])
                    #print(initial_final_total, extra_blocks)
                else:
                    cache.append([board[:30], block_num % len(patterns), jet_index])
                    totals.append([block_num, len(strip_board(board)) + total - 1])
            board = strip_board(board)
            board = [list(i) for i in patterns[block_num % len(patterns)]] + [list(i) for i in empty_space] + board
            block_num += 1
            #print_board(board)
            #input("Added pattern\n")
        if jets[jet_index] == "<":
            board = move_left(board)
        elif jets[jet_index] == ">":
            board = move_right(board)
        jet_index += 1
        jet_index %= len(jets)
        #print_board(board)
        #input("Moved left/right\n")
        board = move_down(board)
        board, extra_rows = shorten_board(board)
        #print_board(board)
        total += extra_rows
        #print_board(board)
        #input("Moved down\n")
    print(f"Part 2: {final_final_total}")
        


if __name__ == "__main__":
    main()

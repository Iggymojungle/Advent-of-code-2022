from time import perf_counter
def get_data():
    with open("data.txt", "r") as f:
        data = [list(i) for i in f.read().split("\n")]
    return data


move_directions = {
    (-1, 0) : "^", 
    (1, 0) : "v", 
    (0, -1) : "<", 
    (0, 1) : ">"
}

check_directions = {
    (-1, 0) : [[-1, 0], [-1, -1], [-1, 1]],
    (1, 0) : [[1, 0], [1, -1], [1, 1]],
    (0, -1) : [[0, -1], [-1, -1], [1, -1]],
    (0, 1) : [[0, 1], [-1, 1], [1, 1]]
}

around_space = {
    (-1, 0) : "v",
    (1, 0) : "^",
    (0, -1) : ">",
    (0, 1) : "<"
}


def print_grid(grid):
    for line in grid:
        print("".join(line))
    print("\n")


def extend_grid(grid):
    for line in range(len(grid)):
        grid[line] = ["."] + grid[line] + ["."]
    grid = [["." for _ in range(len(grid[0]))]] + grid + [["." for _ in range(len(grid[0]))]]
    return grid


def collapse_grid(grid):
    for _ in range(2):
        while all([i == "." for i in grid[0]]):
            grid = grid[1:]
        while all([i == "." for i in grid[-1]]):
            grid = grid[:-1]
        grid = [list(i) for i in list(zip(*grid))]
    return grid


def turn(grid, start_index):
    grid = extend_grid(grid)
    moving = False
    move_order = list(move_directions.keys())
    for _ in range(start_index):
        move_order.append(move_order.pop(0))
    
    for line_num, line in enumerate(grid):
        for space_num, space in enumerate(line):
            if space == "#":
                neighbors = False
                for line_change in (-1, 0, 1):
                    for space_change in (-1, 0, 1):
                        if grid[line_num + line_change][space_num + space_change] in ["#", "v", "<", ">", "^"] and [line_change, space_change] != [0, 0]:
                            neighbors = True
                if not neighbors:
                    continue
                for direction in move_order:
                    moveable = True
                    for check in check_directions[direction]:
                        if grid[line_num + check[0]][space_num + check[1]] != ".":
                            moveable = False
                    if moveable:
                        grid[line_num][space_num] = move_directions[direction]
                        break
    
    for line_num, line in enumerate(grid):
        for space_num, space in enumerate(line):
            around_count = 0
            to_move = None
            for check_space in around_space:
                if 0 <= line_num + check_space[0] < len(grid) and 0 <= space_num + check_space[1] < len(grid[0]):
                    if grid[line_num + check_space[0]][space_num + check_space[1]] == around_space[check_space]:
                        around_count += 1
                        to_move = [line_num + check_space[0], space_num + check_space[1]]
            if around_count == 1:
                grid[line_num][space_num] = "#"
                grid[to_move[0]][to_move[1]] = "."
                moving = True

    for line_num, line in enumerate(grid):
            for space_num, space in enumerate(line):
                if space in move_directions.values():
                    grid[line_num][space_num] = "#"
                    
    start_index += 1
    start_index %= 4
    return grid, start_index, moving
                

def main():
    grid = get_data()
    #print_grid(grid)
    start_index = 0
    elf_count = 0
    for line in grid:
        for space in line:
            if space == "#":
                elf_count += 1
    for _ in range(10):
        grid, start_index, moving = turn(grid, start_index)
        grid = collapse_grid(grid)
    print(f"Part 1: {len(grid) * len(grid[0]) - elf_count}")
    print("Part 2 takes about 45 seconds to run")
    start = perf_counter()
    rounds = 0
    moving = True
    grid = get_data()
    start_index = 0
    while moving:
        rounds += 1
        grid, start_index, moving = turn(grid, start_index)
        grid = collapse_grid(grid)
        #if rounds % 10 == 0:
            #print(rounds)
        #print_grid(grid)
    end = perf_counter()
    print(f"Part 2: {rounds}")
    print(f"Part 2 time: {round(end - start)} seconds")


if __name__ == "__main__":
    main()

import pygrille
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
    #for line in grid:
        #print(line)
    #print("\n")
    move_order = list(move_directions.keys())
    for _ in range(start_index):
        move_order.append(move_order.pop(0))
    #print(move_order)
    
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
    #print_grid(grid)
    #for direction_index in range(4):
        #actual_direction = list(move_directions.keys())[(direction_index + start_index) % 4]
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
                #if space == move_directions[actual_direction]:
                    #if grid[line_num + actual_direction[0]][space_num + actual_direction[1]] == ".":
                        #grid[line_num + actual_direction[0]][space_num + actual_direction[1]] = "#"
                        #grid[line_num][space_num] = "."
    for line_num, line in enumerate(grid):
            for space_num, space in enumerate(line):
                if space in move_directions.values():
                    grid[line_num][space_num] = "#"
    start_index += 1
    start_index %= 4
    return grid, start_index, moving
                
PIXEL_SIZE = 6
GRID_DIMENSIONS = (150, 150)


def draw_grid(grid, pg_grid):
    for line_num, line in enumerate(grid):
        for cell_num, cell in enumerate(line):
            if cell == "#":
                pg_grid[cell_num][line_num].colour = (55, 184, 240)
            elif cell == ".":
                pg_grid[cell_num][line_num].colour = (0, 0, 0)
    pg_grid.draw()


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

    pg_grid = pygrille.Grid(PIXEL_SIZE, GRID_DIMENSIONS, framerate = 180)
    rounds = 0
    moving = True
    grid = get_data()
    running = True
    start_index = 0
    while moving:
        if not pg_grid.check_open():
            running = False
            break
        pg_grid.tick()
        draw_grid(grid, pg_grid)
        rounds += 1
        grid, start_index, moving = turn(grid, start_index)
        grid = collapse_grid(grid)
        #if rounds % 10 == 0:
            #print(rounds)
        #print_grid(grid)
    print(f"Part 2: {rounds}")
    while running:
        running = pg_grid.check_open()
        pg_grid.tick()
    pg_grid.quit()
    #print(len(grid), len(grid[0]))
    
        
    


if __name__ == "__main__":
    main()

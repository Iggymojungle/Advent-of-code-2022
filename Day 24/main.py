from time import perf_counter

def get_data():
    with open("data.txt", "r") as f:
        grid = [list(i) for i in f.read().split("\n")]
    return grid


directions = {
    "^" : (-1, 0),
    "v" : (1, 0),
    ">" : (0, 1),
    "<" : (0, -1)
}


moveable = [
    [0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]
]


def print_grid(grid):
    for line in grid:
        print("".join([i if len(i) == 1 else str(len(i)) for i in line]))
    print("\n")


def move_blizzards(grid):
    new_grid = [["." if cell != "#" else "#" for cell in line] for line in grid]
    for line_num, line in enumerate(grid):
        for cell_num, cell in enumerate(line):
            for character in cell:
                if character in directions:
                    new_coords = [line_num + directions[character][0], cell_num + directions[character][1]]
                    if new_grid[new_coords[0]][new_coords[1]] == "#":
                        for _ in range(2): # Move twice more to go over the hashes
                            new_coords = [new_coords[0] + directions[character][0], new_coords[1] + directions[character][1]]
                        new_coords = [new_coords[0] % len(grid), new_coords[1] % len(grid[0])]
                    if new_grid[new_coords[0]][new_coords[1]] == ".": # allow multiple in one spot
                        new_grid[new_coords[0]][new_coords[1]] = character
                    else:
                        new_grid[new_coords[0]][new_coords[1]] += character
    return new_grid


def get_options(coords, grid):
    options = []
    for direction in moveable:
        new_pos = [coords[i] + direction[i] for i in range(len(coords))]
        if 0 <= new_pos[0] < len(grid) and  0 <= new_pos[1] < len(grid[0]):
            if grid[new_pos[0]][new_pos[1]] == ".":
                options.append(new_pos)
    return options
        

def bfs(grid, coords, end):
    last_print = 0
    steps = 0
    queue = [coords]
    grid_cache = [grid]
    for _ in range(1000): # Arbitrary number - better way would be to work out LCM of width and height and mod step number by this and only cache up to this value. This way works though for the solution and I can't be bothered to change it.
        grid_cache.append(move_blizzards(grid_cache[-1]))
    
    while len(queue) > 0:
        next_queue = []
        grid = grid_cache[steps + 1]
        for _ in range(len(queue)): # Do bfs for each thing in the queue, then change the grid and step number
            current = queue.pop(0)
        
            if current == end:
                return current, steps, grid_cache[steps]
            
            for option in get_options(current, grid):
                if option not in next_queue:
                    next_queue.append(option)
        steps += 1
        queue = next_queue


def main():
    start = perf_counter()
    grid = get_data()
    coords = [0, 1]
    coords, steps0, grid = bfs(grid, coords, [len(grid) - 1, len(grid[0]) - 2])
    print(f"Part 1: {steps0}")
    coords, steps1, grid = bfs(grid, coords, [0, 1])
    coords, steps2, grid = bfs(grid, coords, [len(grid) - 1, len(grid[0]) - 2])
    print(f"Part 2: {steps0 + steps1 + steps2}")
    end = perf_counter()
    print(f"Time for both parts: {round(end - start)} seconds")


if __name__ == "__main__":
    main()

def get_data():
    with open("data.txt", "r") as f:
        data = [[list(map(int, m)) for m in [i.split(",") for i in j]] for j in [k.split(" -> ") for k in f.read().split("\n")]]
    return data


SCALE_ENCODING = 300
FLOOR = 175 # Y coord of floor
GRID_DIMENSIONS = (400, 200)


def save_grid(grid):
    with open("test_output.csv", "w") as f:
        for line in grid:
            for cell in line:
                if cell is None:
                    f.write(",")
                elif cell:
                    f.write(f"{cell},")
            f.write("\n")


def make_grid():
    data = get_data()
    grid = [[None for _ in range(GRID_DIMENSIONS[0])] for __ in range(GRID_DIMENSIONS[1])] # None = empty, True = rock or sand
    for line in data:
        for coord_num, coord in enumerate(line[:-1]):
            next_coord = line[coord_num + 1]
            if coord[0] == next_coord[0]:
                for y_coord in range(coord[1], next_coord[1] + int(1 if int(next_coord[1] - coord[1]) > 0 else -1), 1 if int(next_coord[1] - coord[1]) > 0 else -1):
                    grid[y_coord][coord[0]-SCALE_ENCODING] = True
            elif coord[1] == next_coord[1]:
                for x_coord in range(coord[0], next_coord[0] + int(1 if int(next_coord[0] - coord[0]) > 0 else -1), 1 if int(next_coord[0] - coord[0]) > 0 else -1):
                    grid[coord[1]][x_coord-SCALE_ENCODING] = True
    return grid


def main():
    grid = make_grid()
    fallen = False
    sand_count = 0
    grid = [list(i) for i in list(zip(*grid))]
    while not fallen:
        sand = [500 - SCALE_ENCODING, 0]
        sand_count += 1
        settled = False
        while not settled:
            if sand[1] + 1 >= len(grid[0]):
                fallen = True
                settled = True
            elif not grid[sand[0]][sand[1] + 1]:
                sand = [sand[0], sand[1] + 1]
            elif not grid[sand[0] - 1][sand[1] + 1]:
                sand = [sand[0] - 1, sand[1] + 1]
            elif not grid[sand[0] + 1][sand[1] + 1]:
                sand = [sand[0] + 1, sand[1] + 1]
            else:
                grid[sand[0]][sand[1]] = "s"
                settled = True
    print(f"Part 1: {sand_count - 1}")

    grid = make_grid()
    for i in range(len(grid[0])): # Fill in floor
        grid[FLOOR][i] = True
    blocked = False
    sand_count = 0
    grid = [list(i) for i in list(zip(*grid))]
    while not blocked:
        sand = [500 - SCALE_ENCODING, 0]
        sand_count += 1
        settled = False
        while not settled:
            if not grid[sand[0]][sand[1] + 1]:
                sand = [sand[0], sand[1] + 1]
            elif not grid[sand[0] - 1][sand[1] + 1]:
                sand = [sand[0] - 1, sand[1] + 1]
            elif not grid[sand[0] + 1][sand[1] + 1]:
                sand = [sand[0] + 1, sand[1] + 1]
            else:
                grid[sand[0]][sand[1]] = "s"
                settled = True
                if sand == [500-SCALE_ENCODING, 0]:
                    blocked = True
    print(f"Part 2: {sand_count}")
    save_grid(list(zip(*grid)))


if __name__ == "__main__":
    main()

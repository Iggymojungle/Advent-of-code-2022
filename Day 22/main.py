def grid_convert(grid): # This only works for my particular grid - will not work for other shapes
    count = -1
    for cell in range(len(grid[0])):
        if grid[0][cell] == "X":
            if count < 50:
                grid[0][cell] = "A" + str(count)
            else:
                grid[0][cell] = "B" + str(count - 50)
            count += 1
    
    column = grid[1].index("X")
    count = 99
    for row in range(len(grid)):
        if grid[row][column] == "X":
            if count >= 50:
                grid[row][column] = "D" + str(count - 50)
            elif count >= 0:
                grid[row][column] = "F" + str(count)
            count -= 1
    
    count = 49
    column = grid[1].index("X")
    for row in range(len(grid)):
        if grid[row][column] == "X":
            grid[row][column] = "G" + str(count)
            count -= 1

    count = 0
    for cell in range(len(grid[51])):
        if grid[51][cell] == "X":
            grid[51][cell] = "E" + str(count)
            count += 1
    
    column = grid[51].index("E0")
    count = 1
    for row in range(len(grid)):
        if grid[row][column] == "X":
            if count < 50:
                grid[row][column] = "E" + str(count)
            else:
                grid[row][column] = "G" + str(count - 50)
            count += 1

    count = 50
    for cell in range(len(grid[100])):
        if grid[100][cell] == "X":
            grid[100][cell] = "F" + str(count)
            count -= 1
    
    column = 0
    count = 0
    for row in range(len(grid)):
        if grid[row][column] == "X":
            if count < 50:
                grid[row][column] = "D" + str(count)
            else:
                grid[row][column] = "A" + str(count - 50)
            count += 1

    count = 0
    for cell in range(len(grid[-1])):
        if grid[-1][cell] == "X":
            grid[-1][cell] = "B" + str(count)
            count += 1
    
    column = 51
    count = 0
    for row in range(len(grid)):
        if grid[row][column] == "X":
            grid[row][column] = "C" + str(count)
            count += 1
    
    count = 1
    for cell in range(len(grid[-51])):
        if grid[-51][cell] == "X":
            grid[-51][cell] = "C" + str(count)
            count += 1
    return grid


def outline(grid):
    letter = "X" # Teleport from X to Y or vice versa
    for _ in range(2):
        for line_num, line in enumerate(grid):
            if line[0] == " ":
                for space in range(len(line)):
                    if line[space] != " ":
                        grid[line_num].insert(0, " ")
                        grid[line_num][space] = letter
                        break
            else:
                grid[line_num] = [letter] + line
        grid = [list(reversed(line)) for line in grid]
        #letter = "Y"
    return grid


def transpose(grid):
    return [list(i) for i in list(zip(*grid))]


def get_data():
    with open("grid.txt", "r") as f:
        grid = [list(i) for i in f.read().split("\n")]
        for line_num, line in enumerate(grid):
            widest = max([len(i) for i in grid])
            grid[line_num] += [" " for i in range(widest - len(line))]
        grid = outline(grid)
        grid = transpose(grid)
        grid = outline(grid)
        grid = transpose(grid)
        #print_grid(grid)
    
    with open("movements.txt", "r") as f:
        movements_temp = f.read()
        movements = []
        while len(movements_temp) > 2:
            index = 0
            while movements_temp[index].isnumeric():
                index += 1
            movements.append(movements_temp[:index])
            movements.append(movements_temp[index:index + 1])
            movements_temp = movements_temp[index+1:]
        movements.append(movements_temp)
        for i in range(len(movements)):
            if movements[i].isnumeric():
                movements[i] = int(movements[i])
    return grid, movements


def print_grid(grid, coords = None):
    grid = [list(i) for i in grid] # Ensure grid is copied in memory properly
    if coords:
        grid[coords[0]][coords[1]] = "O"
    for line in grid:
        print("".join([i if len(i) == 1 else i[1] for i in line]))


facing = { # Numbers to add to coords when moving in a particular direction
    0 : [0, 1], # 0 = Right
    1 : [1, 0], # 1 = Down
    2 : [0, -1], # 2 = Left
    3 : [-1, 0] # 3 = Up
}


def move_p1(coords, current_facing, grid, to_move):
    for _ in range(to_move):
        #print(_, grid[coords[0]][coords[1]])
        if grid[coords[0]][coords[1]] == " ":
            print_grid(grid, coords)
            print_grid(grid, pos_before)
            print(current_facing)
            raise Exception("Went off grid")
        pos_before = list(coords)
        coords = [coords[i] + facing[current_facing][i] for i in range(len(coords))]
        
        if grid[coords[0]][coords[1]] == "X":
            if current_facing == 2:
                coords[1] = "".join(grid[coords[0]]).rindex("X")
                while grid[coords[0]][coords[1]] == "X":
                    coords[1] -= 1
                    
            elif current_facing == 3:
                column = [line[coords[1]] for line in grid]
                coords[0] = "".join(column).rindex("X")
                while grid[coords[0]][coords[1]] == "X":
                    coords[0] -= 1

            if current_facing == 0:
                coords[1] = grid[coords[0]].index("X")
                while grid[coords[0]][coords[1]] == "X":
                    coords[1] += 1
                    
            elif current_facing == 1:
                column = [line[coords[1]] for line in grid]
                coords[0] = column.index("X")
                while grid[coords[0]][coords[1]] == "X":
                    coords[0] += 1
        
        if grid[coords[0]][coords[1]] == "#":
            #print("Finished early")
            coords = pos_before
            return coords
    return coords


def move_p2(coords, current_facing, grid, to_move):
    for _ in range(to_move):
        pos_before = list(coords)
        facing_before = int(current_facing)
        coords = [coords[i] + facing[current_facing][i] for i in range(len(coords))]
        if len(grid[coords[0]][coords[1]]) > 1: # If on a warp space
            # Special cases (corners)
            if grid[coords[0]][coords[1]] in ["C0", "F0", "E0"]:
                if grid[coords[0]][coords[1]] in ["C0", "E0"]:
                    if current_facing == 1: # Going down
                        current_facing = 2
                    elif current_facing == 0: # Going right
                        current_facing = 3
                elif grid[coords[0]][coords[1]] == "F0":
                    if current_facing == 3: # Going up
                        current_facing = 0
                    elif current_facing == 2: # Going left
                        current_facing = 1
                coords = [coords[i] + facing[current_facing][i] for i in range(len(coords))]
            else:
                # Find corresponding warp space
                #print(coords, grid[coords[0]][coords[1]])
                for line_num, line in enumerate(grid):
                    if grid[coords[0]][coords[1]] in line and line_num != coords[0]:
                        coords = [line_num, line.index(grid[coords[0]][coords[1]])]
                        #print(coords, grid[coords[0]][coords[1]])
                        break
                # Work out new facing direction by brute force
                for direction in facing:
                    #print(facing[direction])
                    #print(coords)
                    temp_coords = [coords[i] + facing[direction][i] for i in range(len(coords))]
                    if 0 < temp_coords[0] < len(grid) and 0 < temp_coords[1] < len(grid[0]):
                        if grid[temp_coords[0]][temp_coords[1]] in [".", "#"]:
                            coords = temp_coords
                            current_facing = direction
                            break
                else:
                    raise Exception("No valid place found to move to")

        if grid[coords[0]][coords[1]] == "#":
            coords = pos_before
            current_facing = facing_before
            return coords, current_facing
    return coords, current_facing


def main():
    grid, movements = get_data()
    coords = [1, grid[1].index("X") + 1] # Get starting position
    current_facing = 0 # Start off facing right
    #print(grid[coords[0]][coords[1]])
    #print(coords)
    #print(movements)
    for instruction in movements:
        if isinstance(instruction, int):
            coords = move_p1(coords, current_facing, grid, instruction)
            #print_grid(grid, coords)
            #print("\n")
        else:
            if instruction == "L":
                current_facing -= 1
            if instruction == "R":
                current_facing += 1
            current_facing %= 4
    #print(coords, current_facing)
    password = 1000 * coords[0] + 4 * coords[1] + current_facing
    print(f"Part 1: {password}")
    
    grid_dimensions = [len(grid[0]), len(grid)]
    
    grid = grid_convert(grid)
    #print_grid(grid)
    coords = [1, grid[1].index("D49") + 1]
    current_facing = 0
    for instruction in movements:
        if isinstance(instruction, int):
            coords, current_facing = move_p2(coords, current_facing, grid, instruction)
            #print_grid(grid, coords)
            #print("\n")
            #input()
        else:
            if instruction == "L":
                current_facing -= 1
            if instruction == "R":
                current_facing += 1
            current_facing %= 4
    password = 1000 * coords[0] + 4 * coords[1] + current_facing
    print(f"Part 2: {password}")

if __name__ == "__main__":
    main()
        
move_dict = {
    "U" : [0, 1],
    "L" : [-1, 0],
    "R" : [1, 0],
    "D" : [0, -1]
}

possible_tail_moves = [
    [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], 
    [1, 1], [-1, -1], [-1, 1], [1, -1]
]

next_to = [
    [0, 0], [0, 1], [1, 0], [-1, 0], [0, -1]
]


def check_next_to(head_pos, tail_pos):
    for move in possible_tail_moves:
        if [tail_pos[i] + move[i] for i in (0, 1)] == head_pos:
            return True
    return False


def check_adjacent(head_pos, tail_pos):
    for move in next_to:
        if [tail_pos[i] + move[i] for i in (0, 1)] == head_pos:
            return True
    return False   

    
def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(" ") for i in f.read().split("\n")]
    return data


def print_grid(tail_seen_pos, Tpos, Hpos, knots):
    grid = [["." for _ in range(20)] for __ in range(20)]
    for pos in tail_seen_pos:
        grid[pos[1]][pos[0]] = "#"
    grid[Tpos[1]][Tpos[0]] = "T"
    grid[Hpos[1]][Hpos[0]] = "H"
    for num in range(len(knots)-1, -1, -1):
        grid[knots[num][1]][knots[num][0]] = str(len(knots)-num)
    for z in grid:
        print(z)


def main():
    data = get_data()
    head_pos = [0, 0]
    tail_pos = [0, 0]
    positions = [[0, 0]]
    for i in data:
        for times in range(int(i[1])):
            head_pos = [head_pos[j] + move_dict[i[0]][j] for j in (0, 1)]
            if not check_next_to(head_pos, tail_pos):
                for move in possible_tail_moves:
                    if check_adjacent(head_pos, [tail_pos[j] + move[j] for j in (0, 1)]):
                        tail_pos =  [tail_pos[j] + move[j] for j in (0, 1)]
                        positions.append(tail_pos)
                        break
    unique_positions = []
    for i in positions:
        if i not in unique_positions:
            unique_positions.append(i)
    print(f"Part 1: {len(unique_positions)}")

    knots = [[0, 0] for _ in range(10)]
    positions = [[0, 0]]
    for i in data:
        for times in range(int(i[1])):
            knots[0] = [knots[0][j] + move_dict[i[0]][j] for j in (0, 1)]
            for index, tail_pos in enumerate(knots[1:]):
                head_pos = knots[index]
                if not check_next_to(head_pos, tail_pos):
                    for move in possible_tail_moves:
                        if check_adjacent(head_pos, [tail_pos[j] + move[j] for j in (0, 1)]):
                            knots[index+1] =  [tail_pos[j] + move[j] for j in (0, 1)]
                            if index == len(knots) - 2:
                                positions.append(tail_pos)
                            break
                    else:
                        for move in possible_tail_moves:
                            if check_next_to(head_pos, [tail_pos[j] + move[j] for j in (0, 1)]):
                                knots[index+1] =  [tail_pos[j] + move[j] for j in (0, 1)]
                                if index == len(knots) - 2:
                                    positions.append(tail_pos)
    unique_positions = []
    for i in positions:
        if i not in unique_positions:
            unique_positions.append(i)
    print(f"Part 2: {len(unique_positions)+1}")

    


if __name__ == "__main__":
    main()
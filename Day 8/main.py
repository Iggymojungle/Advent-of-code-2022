def get_data():
    with open("data.txt","r") as f:
        data = [list(map(int, i)) for i in f.read().split("\n")]
    return data


def transpose(old_list):
    new_list = list(zip(*old_list))
    new_list = [list(i) for i in new_list]
    return new_list


def get_left_right(data):
    total = 0
    trees = []
    for line_num, line in enumerate(data):
        for pos, tree in enumerate(line):
            if all([tree > line[pos+i] for i in range(1, len(line)-pos)]) or all([tree > line[i] for i in range(pos-1, -1, -1)]):
                total += 1
                trees.append([line_num, pos])
    return total, trees


def seeable(line, pos, tree):
    line_total = 1
    if pos == len(line) - 1:
        return 0
    while line[pos + line_total] < tree:
        if line_total + pos + 1 < len(line):
            line_total += 1
        else:
            return line_total
    return line_total


def update_part_2(data, total_grid):
    for line_num, line in enumerate(data):
        for pos, tree in enumerate(line):
            line_total = seeable(line, pos, tree)
            total_grid[line_num][pos] *= line_total
            line_total = seeable(list(reversed(line)), len(line) - 1 - pos, tree)
            total_grid[line_num][pos] *= line_total
    return total_grid  


def main():
    data = get_data()
    total, trees = get_left_right(data)
    data = transpose(data)
    total2, trees2 = get_left_right(data)
    for coord in trees2:
        trees.append([coord[1], coord[0]])
    unique_trees = []
    for tree in trees:
        if tree not in unique_trees:
            unique_trees.append(tree)
    print(f"Part 1: {len(unique_trees)}")
    
    data = get_data()
    best = 0
    total_grid = [[1 for j in range(len(data[i]))] for i in range(len(data))]
    total_grid = update_part_2(data, total_grid)
    data = transpose(data)
    total_grid = transpose(total_grid)
    total_grid = update_part_2(data, total_grid)
    final_max = [max(i) for i in total_grid]
    final_max = max(final_max)
    print(f"Part 2: {final_max}")


if __name__ == "__main__":
    main()

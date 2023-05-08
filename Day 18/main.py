def get_data():
    with open("data.txt", "r") as f:
        data = [list(map(int, i.split(","))) for i in f.read().split("\n")]
    return data


to_check = [
    [-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]
]


def check_inside(data, current_coord, visited = None, depth = None, inside = None): # NOT WORKING!!!!!!!!
    if inside is None:
        inside = True
    if visited is None:
        visited = [current_coord]
    else:
        visited.append(current_coord)
    if depth is None:
        depth = 0
    else:
        if depth > 500:
            return visited, False
    for check in to_check:
        if [current_coord[i] + check[i] for i in range(3)] not in data:
            visited, inside = check_inside(data, [current_coord[i] + check[i] for i in range(3)], visited, depth + 1, inside)
            if not inside:
                return visited, inside
    return visited, inside


def bfs_inside(data, current_coord): # FIX THIS (Maybe, or fix something else i guess)
    queue = ["temp"]
    visited = [current_coord]
    while len(queue) > 0:
        if "temp" in queue:
            queue = []
        else:
            current_coord = queue.pop(0)
            visited.append(current_coord)
        for check in to_check:
            if [current_coord[i] + check[i] for i in range(3)] not in data and [current_coord[i] + check[i] for i in range(3)] not in visited and [current_coord[i] + check[i] for i in range(3)] not in queue: 
                queue.append([current_coord[i] + check[i] for i in range(3)])

        if len(queue) > 100:
            return visited, False
    return visited, True


def main():
    data = get_data()
    total = 0
    for cube in data:
        total += 6
        for check in to_check:
            if [cube[i] + check[i] for i in range(3)] in data:
                total -= 1
    print(f"Part 1: {total}")
    known_inside = []
    known_outside = []
    total = 0
    for cube in data:
        total += 6
        for check in to_check:
            if [cube[i] + check[i] for i in range(3)] in data:
                total -= 1
            elif [cube[i] + check[i] for i in range(3)] in known_inside:
                total -= 1
            elif [cube[i] + check[i] for i in range(3)] not in known_outside:
                temp_visited, inside = bfs_inside(data, [cube[i] + check[i] for i in range(3)])
                if inside:
                    total -= 1
                    for coord in temp_visited:
                        known_inside.append(coord)
                else:
                    for coord in temp_visited:
                        known_outside.append(coord)
    print(f"Part 2: {total}")
                


if __name__ == "__main__":
    main()

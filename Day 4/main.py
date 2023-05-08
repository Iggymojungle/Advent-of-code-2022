def get_data():
    with open("data.txt", "r") as f:
        data = [[k.split("-") for k in j] for j in [i.split(",") for i in f.read().split("\n")]]
    return data


def convert_range(start, end):
    return range(int(start), int(end) + 1)


def check_inside(line):
    range1 = convert_range(line[0][0], line[0][1])
    range2 = convert_range(line[1][0], line[1][1])
    if range1.start in range2 and range1[-1] in range2: 
        return True
    return False


def check_overlap(line):
    range1 = convert_range(line[0][0], line[0][1])
    range2 = convert_range(line[1][0], line[1][1])
    for i in range1:
        if i in range2:
            return True
    return False


def main():
    data = get_data()
    total = 0
    for line in data:
        if check_inside(line) or check_inside([line[1], line[0]]):
            total += 1
    print(f"Part 1: {total}")
    total = 0
    for line in data:
        if check_overlap(line) or check_overlap([line[1], line[0]]):
            total += 1
    print(f"Part 2: {total}")
            


if __name__ == "__main__":
    main()
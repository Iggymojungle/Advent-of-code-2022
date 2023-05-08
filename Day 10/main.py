def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(" ") for i in f.read().split("\n")]
    return data


def main():
    data = get_data()
    cycles = 0
    x = 1
    total = 0
    just_read = False
    for instruction in data:
        if just_read:
            just_read = False
        elif cycles % 40 == 20:
            total += cycles * x

        if instruction[0] == "noop":
            cycles += 1
        elif instruction[0] == "addx":
            if cycles % 40 in [18, 19]:
                total += (cycles + (20-(cycles % 40))) * x
                just_read = True
            cycles += 2
            x += int(instruction[1])
    print(f"Part 1: {total}")

    
    line = 0
    adding = False
    cycles = 0
    x = 1
    print("Part 2:")
    while line < len(data):
        if cycles == 40:
            print("")
            cycles = 0

        if cycles in [x-1, x, x+1]:
            print("██", end = "")
        else:
            print("  ", end = "")

        if adding:
            x += int(data[line][1])
            line += 1
            adding = False
        elif data[line][0] == "addx":
            adding = True
        elif data[line][0] == "noop":
            line += 1
        cycles += 1
        

if __name__ == "__main__":
    main()
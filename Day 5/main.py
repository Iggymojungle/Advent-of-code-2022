def get_data():
    with open("starting_order.txt", "r") as f:
        stacks = [i.replace("] [", ".").replace("[", "").replace("]", "").split(".") for i in f.read().split("\n")]
        stacks = list(zip(*stacks))
        stacks = [[j for j in i if j != " "] for i in stacks]

    with open("data.txt", "r") as f:
        order = [[int(k) for k in j] for j in [i.replace("move ", "").replace("from ", "").replace("to ", "").split(" ") for i in f.read().split("\n")]]
    
    return stacks, order


def main():
    stacks, order = get_data()
    for instruction in order:
        for _ in range(instruction[0]):
            stacks[instruction[2]-1].insert(0, stacks[instruction[1]-1].pop(0))
    print(f'Part 1: {"".join([i[0] for i in stacks])}')

    stacks, order = get_data()
    for instruction in order:
        for times in range(instruction[0], 0, -1):
            stacks[instruction[2]-1].insert(0, stacks[instruction[1]-1].pop(times-1))
    print(f'Part 2: {"".join([i[0] for i in stacks])}')


if __name__ == "__main__":
    main()
        
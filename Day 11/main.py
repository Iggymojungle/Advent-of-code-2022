def get_data(): # Lines put in form [list of items, operation, test, monkey if true, monkey if false]
    with open("data.txt", "r") as f:
        data = [i.split("\n") for i in f.read().split("\n\n")]
        data = [[i.strip() for i in j] for j in data]
        data = [i[1:] for i in data]
        for i in range(len(data)):
            data[i][0] = list(map(int, data[i][0].replace(",", "").split(" ")[2:]))
            data[i][1] = data[i][1].split(" ")[3:]
            data[i][2] = int(data[i][2].split(" ")[-1])
            data[i][3] = int(data[i][3].split(" ")[-1])
            data[i][4] = int(data[i][4].split(" ")[-1])
    return data


def main():
    data = get_data()
    totals = [0 for _ in range(len(data))]
    for rounds in range(20):
        for monkey_num, monkey in enumerate(data):
            for old in monkey[0]:
                totals[monkey_num] += 1
                worry_level = eval(f"{monkey[1][0]}{monkey[1][1]}{monkey[1][2]}")
                worry_level //= 3
                if worry_level % monkey[2] == 0:
                    data[monkey[3]][0].append(worry_level)
                else:
                    data[monkey[4]][0].append(worry_level)
                data[monkey_num][0] = []
    print(f"Part 1: {sorted(totals)[-1] * sorted(totals)[-2]}")
    
    data = get_data()
    divisor = 1
    for monkey in data: # Get divisor to use for mods
        divisor *= monkey[2]
    totals = [0 for _ in range(len(data))]
    for rounds in range(10000):
        # print(rounds)
        for monkey_num, monkey in enumerate(data):
            for old in monkey[0]:
                totals[monkey_num] += 1
                worry_level = eval(f"{monkey[1][0]}{monkey[1][1]}{monkey[1][2]}")
                worry_level %= divisor
                if worry_level % monkey[2] == 0:
                    data[monkey[3]][0].append(worry_level)
                else:
                    data[monkey[4]][0].append(worry_level)
                data[monkey_num][0] = []       
    print(f"Part 2: {sorted(totals)[-1] * sorted(totals)[-2]}")


if __name__ == "__main__":
    main()
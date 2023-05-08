def get_data():
    with open("data.txt", "r") as f:
        data = f.read().split("\n")
        return data


def decode(letter):
    letter = ord(letter)
    if letter < 97:
        return letter - 38
    return letter - 96


def main():
    data = get_data()
    data = [[i[:len(i)//2],i[len(i)//2:]] for i in data]
    for position, rucksack in enumerate(data):
        for letter in rucksack[0]:
            if letter in rucksack[1]:
                data[position] = decode(letter)
                break
    print(f"Part 1: {sum(data)}")

    data = get_data()
    total = 0
    for position, rucksack in enumerate(data):
        if position % 3 == 0:
            rucksacks = [data[position + 1], data[position + 2]]
            for letter in rucksack:
                if letter in rucksacks[0] and letter in rucksacks[1]:
                    total += decode(letter)
                    break
    print(f"Part 2: {total}")


if __name__ == "__main__":
    main()
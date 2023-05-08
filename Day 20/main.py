import copy


def get_data():
    with open("data.txt", "r") as f:
        data = copy.deepcopy(list(map(data_number, f.read().split("\n"))))
    return data


class data_number(int):
    uid = 0


def move(data, move_number):
    moving_index = [i.uid for i in data].index(move_number)
    number = data.pop(moving_index)
    new_index = (moving_index + number)
    new_index %= len(data)
    if new_index == 0:
        new_index = len(data)
    data.insert(new_index, number)
    move_number += 1
    return data, move_number


KEY = 811589153


def get_total(data):
    total = 0
    zero_index = data.index(0)
    for number in [1000, 2000, 3000]:
        total += data[(zero_index + number) % len(data)]
    return total


def main():
    data = get_data()
    for i in range(len(data)):
        data[i].uid = i
    move_number = 0
    for _ in range(len(data)):
        data, move_number = move(data, move_number)
    total = get_total(data)
    print(f"Part 1: {total}")
    print("Part 2 takes a minute or so to run")
    
    data = get_data()
    for i in range(len(data)):
        data[i] = data_number(KEY * data[i])
        data[i].uid = i
    for _ in range(10):
        move_number = 0
        print(_)
        for __ in range(len(data)):
            data, move_number = move(data, move_number)
    total = get_total(data)
    print(f"Part 2: {total}")


if __name__ == "__main__":
    main()

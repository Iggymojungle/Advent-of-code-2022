def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(": ") for i in f.read().split("\n")]
        data = {i[0] : i[1].split(" ") for i in data}
    return data


def get_monkey_yell_p1(data, monkey):
    if len(data[monkey]) == 1:
        return complex(data[monkey][0])
    return eval(f"{get_monkey_yell_p1(data, data[monkey][0])}{data[monkey][1]}{get_monkey_yell_p1(data, data[monkey][2])}")


def get_monkey_yell_p2(data):
    monkey = "root"
    return get_monkey_yell_p1(data, data[monkey][0]) == get_monkey_yell_p1(data, data[monkey][2])


def main():
    data = get_data()
    #for line in data:
        #print(line, data[line])
    print(f"Part 1: {int(get_monkey_yell_p1(data, 'root').real)}")
    #data["humn"] = [0]
    #while not get_monkey_yell_p2(data):
        #print(data["humn"][0])
        #data["humn"][0] += 1
    #print(data["humn"])
    data["humn"] = [1j]
    side1 = get_monkey_yell_p1(data, data["root"][0])
    side2 = get_monkey_yell_p1(data, data["root"][2])
    if side1.imag:
        left = side1
        right = side2
    else:
        left = side2
        right = side1
    answer = (left.real - right.real)/(left.imag*-1)
    print(f"Part 2: {round(answer)}")
    
        


if __name__ == "__main__":
    main()

outcomes = {
    "A" : {"X" : 3, "Y" : 6, "Z" : 0},
    "B" : {"X" : 0, "Y" : 3, "Z" : 6},
    "C" : {"X" : 6, "Y" : 0, "Z" : 3}
}


outcomes_convert = {
    "A" : {"X" : "Z", "Y" : "X", "Z" : "Y"},
    "B" : {"X" : "X", "Y" : "Y", "Z" : "Z"},
    "C" : {"X" : "Y", "Y" : "Z", "Z" : "X"}
}


shapes = {
    "X" : 1,
    "Y" : 2,
    "Z" : 3
}


def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(" ") for i in f.read().split("\n")]
    return data


def main():
    data = get_data()
    score = 0
    for round in data:
        score += outcomes[round[0]][round[1]] + shapes[round[1]]
    print(f"Part 1: {score}")
    
    score = 0
    for round in data:
        round[1] = outcomes_convert[round[0]][round[1]]
        score += outcomes[round[0]][round[1]] + shapes[round[1]]
    print(f"Part 2 {score}")
    


if __name__ == "__main__":
    main()
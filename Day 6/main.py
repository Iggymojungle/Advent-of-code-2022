def get_data():
    with open("data.txt", "r") as f:
        data = f.read()
    return data


def main():
    data = get_data()
    i = 0
    while len(set([data[i],data[i+1],data[i+2],data[i+3]])) != 4:
        i += 1
    print(f"Part 1: {i+4}")
    while len(set([data[i+j] for j in range(0,14)])) != 14:
        i += 1  
    print(f"Part 2: {i+14}")


if __name__ == "__main__":
    main()
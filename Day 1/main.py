def get_data():
    with open("data.txt", "r") as f:
        data = f.read()
        data = [i.split("\n") for i in data.split("\n\n")]
        data = [[int(i) for i in j] for j in data]
        return data


def main():
    data = get_data()
    data = [sum(i) for i in data]
    print(f"Part 1: {max(data)}")
    data = sorted(data)
    print(f"Part 2: {sum(data[-3:])}")


if __name__ == "__main__":
    main()

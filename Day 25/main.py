def get_data():
    with open("data.txt", "r") as f:
        data = f.read().split("\n")
    return data


decode_numbers = {
    "2" : 2,
    "1" : 1,
    "0" : 0,
    "-" : -1,
    "=" : -2
}


encode_numbers = {v : k for k, v in decode_numbers.items()}


def decode(snafu_number):
    place_value = 1
    total = 0
    for digit in reversed(snafu_number):
        total += decode_numbers[digit] * place_value
        place_value *= 5
    return total


def get_lower_pv_list(place_value):
    lower_pv_list = []
    temp_pv = place_value / 5
    while temp_pv >= 1:
        lower_pv_list.append(temp_pv)
        temp_pv /= 5
    return lower_pv_list


def to_base_5(normal_number):
    base_5_number = ""
    while normal_number:
        base_5_number = str(normal_number % 5) + base_5_number
        normal_number //= 5
    return base_5_number


def encode_from_b5(base_5_number):
    base_5_number = reversed(base_5_number)
    final_number = ""
    carry = 0
    for digit in base_5_number:
        digit = int(digit)
        if digit + carry > 2:
            digit = (digit + carry) - 5
            carry = 1
        else:
            digit = digit + carry
            carry = 0
        final_number += str(encode_numbers[digit])
    final_number += str(encode_numbers[carry])
    final_number = "".join(list(reversed(final_number)))
    while final_number[0] == "0":
        final_number = final_number[1:]
    return final_number




def main():
    data = get_data()
    total = 0
    for snafu_number in data:
        total += decode(snafu_number)
    #print(encode_from_b5(to_base_5(4890)))
    #print(total)
    #print(encode(353))
    print(f"Part 1: {encode_from_b5(to_base_5(total))}")
    print("Part 2: AoC complete!!!!!")


if __name__ == "__main__":
    main()

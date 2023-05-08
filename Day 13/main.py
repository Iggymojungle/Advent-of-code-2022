import ast
def get_data():
    with open("data.txt","r") as f:
        data = f.read().replace("\n\n","\n").split("\n")
        data = [ast.literal_eval(i) for i in data]
    return data


def recursive_check(list1, list2):
    #print(list1,"|",list2)
    if isinstance(list1, int) and isinstance(list2, int):
        if list1 != list2:
            return list1 < list2
        return None

    elif isinstance(list1, int) or isinstance(list2, int):
        if isinstance(list1, int):
            return recursive_check([list1], list2)
        if isinstance(list2, int):
            return recursive_check(list1, [list2])

    else:
        if len(list1) == 0 and len(list2) == 0:
            return None
        if len(list1) == 0:
            return True
        if len(list2) == 0:
            return False
        index = 0
        check = recursive_check(list1[index], list2[index])
        while check is None:
            index += 1
            if len(list1) > index and len(list2) > index:
                check = recursive_check(list1[index:], list2[index:])
            else:
                if len(list1) == len(list2):
                    return None
                if len(list1) <= index:
                    return True
                if len(list2) <= index:
                    return False
        return check            


def bubble_sort(data):
    changed = True
    while changed:
        changed = False
        for packet_num in range(len(data)-1):
            list1 = data[packet_num]
            list2 = data[packet_num + 1]
            if not recursive_check(list1, list2):
                data[packet_num] = list2
                data[packet_num + 1] = list1
                changed = True
    return data



def main():
    data = get_data()
    total = 0
    for i in range(0, len(data), 2):
        ordered = recursive_check(data[i], data[i+1])
        #print(ordered)
        if ordered:
            total += int((i+2)/2)
    print(f"Part 1: {total}")
    data.append([[2]])
    data.append([[6]])
    sorted_data = bubble_sort(data)
    #for i in sorted_data:
        #print(i)
    print(f"Part 2: {(sorted_data.index([[2]]) + 1) * (sorted_data.index([[6]]) + 1)}")
    
        


if __name__ == "__main__":
    main()
        
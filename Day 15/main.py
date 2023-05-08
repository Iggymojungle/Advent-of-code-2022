import time

def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(": ") for i in f.read().replace("Sensor at ", "").replace("closest beacon is at ", "").replace("x=", "").replace("y=", "").split("\n")]
        data = [[list(map(int, j.split(", "))) for j in i] for i in data]
    return data


def mhdist(coords1, coords2):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])


def can_combine(range1, range2):
    return range1.start <= range2.stop and range2.start <= range1.stop



def combine_ranges(range1, range2):
    if range1.start <= range2.start:
        if range1.stop <= range2.stop:
            return range(range1.start, range2.stop)
        return range1
    if range2.stop <= range1.stop:
        return range(range2.start, range1.stop)
    return range2


ROW_TO_CHECK = 2000000
MAX_PART_2 = 4000000


def get_beaconless(distances, row_num):
    ranges = []
    for sensor in distances:
        to_row = abs(sensor["sensor"][1] - row_num)
        extra_range = sensor["distance"] - to_row
        if extra_range >= 0:
            ranges.append(range(sensor["sensor"][0] - extra_range, sensor["sensor"][0] + extra_range + 1))
    #print(ranges)
    combining = True
    while combining:
        combining = False
        to_break = False
        for item in ranges:
            for item2 in [i for i in ranges if i != item]:
                if can_combine(item, item2):
                    ranges = [i for i in ranges if i not in [item, item2]] + [combine_ranges(item, item2)]
                    combining = True
                    to_break = True
                    break
            if to_break:
                break
    return ranges
    


def main():
    data = get_data()
    #print(data)
    distances = [{"sensor" : i[0], "distance" : mhdist(i[0], i[1])} for i in data]
    beacons_not_unique = [i[1] for i in data]
    beacons = []
    for beacon in beacons_not_unique:
        if beacon not in beacons:
            beacons.append(beacon)
    ranges = get_beaconless(distances, ROW_TO_CHECK)
    total = sum([len(r) for r in ranges])
    #print(total)
    for beacon in beacons:
        if beacon[1] == ROW_TO_CHECK and any([beacon[0] in i for i in ranges]):
            total -= 1
    print(f"Part 1: {total}")
    print("Part 2 takes up to 6 minutes to complete on replit or up to 3 minutes running locally...")
    start_time = time.perf_counter()
    for row in range(0, MAX_PART_2 + 1):
        no_beacon = get_beaconless(distances, row)
        no_beacon = [i for i in no_beacon if 0 in i or MAX_PART_2 in i]
        #print(no_beacon)
        if len(no_beacon) > 1:
            #print(no_beacon, row)
            final_row = row
            final_ranges = no_beacon
            break
    for column in range(0, MAX_PART_2 + 1):
        if column not in final_ranges[0] and column not in final_ranges[1]:
            final_column = column
    #print(final_row, final_column)
    final_answer = final_column * 4000000 + final_row
    print(f"Part 2: {final_answer}")
    end_time = time.perf_counter()
    print(f"Part 2 time to complete: {(end_time - start_time)//1} seconds")

        


if __name__ == "__main__":
    main()

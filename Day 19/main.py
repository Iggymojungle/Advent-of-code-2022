import copy
# Data inital format [ore for ore robot, ore for clay robot, ore for obsidian robot, clay for obsidian robot, ore for geode robot, obsidian for geode robot]
# Data after full format {robot product:{required products to make:number of required product needed}}

def get_data():
    with open("data.txt","r") as f:
        data = [list(map(int, i.strip().split(" ")[1:])) for i in f.read().replace("Blueprint ", "").replace(". ", "").replace(".", "").replace(":", "").replace("Each ", "").replace(" robot costs ", "").replace("ore"," ").replace("  and ", " ").replace(" clay", "").replace("obsidian", "").replace("geode"," ").replace("  "," ").split("\n")]
        data = [{"ore" : {"ore":line[0]}, 
                 "clay" : {"ore":line[1]},
                 "obsidian" : {"ore":line[2],"clay":line[3]},
                 "geode" : {"ore":line[4],"obsidian":line[5]}
                } for line in data]
    return data


def get_options(resources, blueprint, robots):
    options = {
        "ore" : False,
        "clay" : False,
        "obsidian" : False,
        "geode" : False
    }
    for robot in blueprint:
        #print(robot)
        if all([blueprint[robot][resource] <= resources[resource] for resource in blueprint[robot]]):
            options[robot] = True
    return [i for i in options if options[i]]


def get_resources(resources, robots):
    for resource in resources:
        #print(resource, resources[resource], robots[resource])
        resources[resource] += robots[resource]
    #print(resources)
    return resources


def build_robot(type, robots, resources, blueprint):
    robots[type] += 1
    for resource_type in blueprint[type]:
        resources[resource_type] -= blueprint[type][resource_type]
    #print(f"{robots=}, {resources=}")
    return resources, robots


def maximise_geodes(blueprint, robots = None, resources = None, minute = None, max_geodes = None, max_needed = None):
    #input(str(minute)+str(resources)+str(robots))
    if robots is None:
        robots = {
            "ore" : 1,
            "clay" : 0,
            "obsidian" : 0,
            "geode" : 0
        }
    if resources is None:
        resources = {
            "ore" : 0,
            "clay" : 0,
            "obsidian" : 0,
            "geode" : 0
        }
    if max_needed is None:
        max_needed = {
            "ore" : 0,
            "clay" : 0,
            "obsidian" : 0,
            "geode" : 0
        }
        for robot in blueprint:
            for resource in blueprint[robot]:
                if blueprint[robot][resource] > max_needed[resource]:
                    max_needed[resource] = blueprint[robot][resource]
    if max_geodes is None:
        max_geodes = 0
    if minute is None:
        minute = 24
    if minute <= 0:
        #print(max_geodes)
        return max_geodes
    # Get possible robot types to build
    options = get_options(resources, blueprint, robots)
    # Increment resources
    resources = get_resources(resources, robots)
    # Update max_geodes if applicable
    if resources["geode"] > max_geodes:
        max_geodes = resources["geode"]
        print(max_geodes)
    if "geode" in options:
        resources, robots = build_robot("geode", robots, resources, blueprint)
        max_geodes = maximise_geodes(blueprint, robots, resources, minute - 1, max_geodes, max_needed)
    elif "obsidian" in options:
        max_geodes = maximise_geodes(blueprint, copy.deepcopy(robots), copy.deepcopy(resources), minute - 1, max_geodes, max_needed)
        resources, robots = build_robot("obsidian", robots, resources, blueprint)
        max_geodes = maximise_geodes(blueprint, robots, resources, minute - 1, max_geodes, max_needed)
    else:
        old_resources = copy.copy(resources)
        old_robots = copy.copy(robots)
        for option in options:
            resources, robots = build_robot(option, copy.copy(old_robots), copy.copy(old_resources), blueprint)
            if robots[option] <= max_needed[option]:
                max_geodes = maximise_geodes(blueprint, robots, resources, minute - 1, max_geodes, max_needed)
        max_geodes = maximise_geodes(blueprint, copy.copy(old_robots), copy.copy(old_resources), minute - 1, max_geodes, max_needed)
    return max_geodes
            


def main():
    print("Warning: Very very slow.")
    data = get_data()
    total = 0
    for id, line in enumerate(data):
        print(line)
        max_geodes = maximise_geodes(line)
        print(max_geodes)
        total += (id + 1) * max_geodes
    print(f"Part 1: {total}")
    total = 1
    print("For part 2 (for me): first = 35, second = 72, third = 11. Takes ages to actually run to completion though!")
    for line in data[0:3]:
        max_geodes = maximise_geodes(line, minute = 32)
        print(max_geodes)
        total *= max_geodes
    print(f"Part 2: {total}")
    input()


if __name__ == "__main__":
    main()

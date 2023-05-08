def get_data():
    with open("data.txt", "r") as f:
        data = [line.split(" ") for line in f.read().split("\n")]
    return data


class Node:
    def __init__(self, name, size = None):
        self.name = name
        self.links = {}
        self.size = size

    def __repr__(self):
        return self.name

    def set_links(self, name, size = None):
        self.links.update({name:Node(name, size)})

    def print_tree(self):
        print(self.name)
        for i in self.links:
            self.links[i].print_tree()

    def get_tree(self, directories = []):
        if not self.size:
            directories.append(self)
        for i in self.links:
            directories = self.links[i].get_tree()
        return directories

    def get_size(self):
        if self.size:
            return self.size
        return sum([i.get_size() for i in self.links.values()])   


def main():
    TOTAL_DISK_SPACE = 70000000
    SPACE_NEEDED = 30000000
    total = 0
    data = get_data()
    tree_start = Node("/")
    current_node = tree_start
    current_path = [tree_start]
    for line in data:
        if line[0] == "$":
            if line[1] == "cd":
                if line[2] == "..":
                    current_path = current_path[:-1]
                    current_node = current_path[-1]
                else:
                    if line[1] not in current_node.links:
                        current_node.set_links(line[2])
                    current_path.append(current_node.links[line[2]])
                    current_node = current_node.links[line[2]]
        elif line[0] == "dir":
            if line[1] not in current_node.links:
                current_node.set_links(line[1])
        else:
            current_node.set_links(line[1],int(line[0]))
    directories = tree_start.get_tree()
    for i in directories:
        temp = i.get_size()
        if temp <= 100000:
            total += temp
    print(f"Part 1: {total}")
    extra_space_needed = SPACE_NEEDED - (TOTAL_DISK_SPACE - tree_start.get_size())
    dir_sizes = [i.get_size() for i in directories if i.get_size() > extra_space_needed]
    print(f"Part 2: {min(dir_sizes)}")


if __name__ == "__main__":
    main()

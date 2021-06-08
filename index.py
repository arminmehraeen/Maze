import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def returnPath(node, maze):
    p = []
    r, c = np.shape(maze)
    result = [[-1 for i in range(c)] for j in range(r)]
    current = node
    while current is not None:
        p.append(current.position)
        current = current.parent
    p = p[::-1]
    v = 0
    for i in range(len(p)):
        result[p[i][0]][p[i][1]] = v
        v += 1
    return result


def search(maze, cost, start, end, move):
    sNode = Node(None, tuple(start))
    sNode.g = sNode.h = sNode.f = 0
    eNode = Node(None, tuple(end))
    eNode.g = eNode.h = eNode.f = 0

    list1 = []
    list2 = []
    list1.append(sNode)

    t = 0
    max = (len(maze) // 2) ** 10

    r, c = np.shape(maze)

    while len(list1) > 0:
        t += 1

        current_node = list1[0]
        current_index = 0
        for index, item in enumerate(list1):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if t > max:
            return returnPath(current_node, maze)

        list1.pop(current_index)
        list2.append(current_node)

        if current_node == eNode:
            return returnPath(current_node, maze)

        children = []
        for new_position in move:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (r - 1) or node_position[0] < 0
                    or node_position[1] > (c - 1) or node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in list2 if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - eNode.position[0]) ** 2) +
                       ((child.position[1] - eNode.position[1]) ** 2))
            child.f = child.g + child.h

            if len([i for i in list1 if child == i and child.g > i.g]) > 0:
                continue

            list1.append(child)


def readFile():
    f = open("C:/Users/Mehraeen/Desktop/Maze/input.txt", "r")
    array = f.readlines()
    size1 = len(array) - 1
    main = []
    for i in range(0, size1):
        temp = array[i].replace("\n", "")
        p = []
        for j in range(0, len(temp)):
            if temp[j] == "0":
                p.append(1)
            elif temp[j] == "1":
                p.append(0)
        main.append(p)
    print("READ FILE SUCCESSFULLY.\n")
    return main


def writeFile(data):
    outFile = open("C:/Users/Mehraeen/Desktop/Maze/output.txt", "w+")
    outFile.write(data)
    outFile.close()
    print("WRITE FILE SUCCESSFULLY.\n")


def findMax(array):
    min = 0
    for k in array:
        for p in k:
            if p > min:
                min = p
    return min


if __name__ == '__main__':
    main = readFile()

    start = [0, 0]
    end = [3, 4]
    cost = 1

    move = [[1, 0], [0, 1]]
    path = search(main, cost, start, end, move)
    out1 = findMax(path) + 1
    print(out1)

    move = [[1, 0], [1, 1], [0, 1]]
    path = search(main, cost, start, end, move)
    out2 = findMax(path) + 1
    print(out2)

    data = "% s" % out1 + "\n" + "% s" % out2
    writeFile(data)

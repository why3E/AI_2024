import math

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = self.h = self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def heuristic(node, goal):
    dx, dy = abs(node.position[0] - goal.position[0]), abs(node.position[1] - goal.position[1])
    return math.sqrt(dx**2 + dy**2) * 10


def aStar(maze, start, end):
    startNode, endNode = Node(None, start), Node(None, end)
    openList, closedSet = [startNode], set()
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while openList:
        currentNode = min(openList, key=lambda o: o.f)
        openList.remove(currentNode)
        closedSet.add(currentNode.position)

        if currentNode == endNode:
            path = []
            while currentNode:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1]

        for dx, dy in directions:
            pos = (currentNode.position[0] + dx, currentNode.position[1] + dy)
            if pos in closedSet or not (0 <= pos[0] < len(maze) and 0 <= pos[1] < len(maze[0])) or maze[pos[0]][pos[1]]:
                continue

            g_cost = currentNode.g + (14 if dx != 0 and dy != 0 else 10)
            neighbor = Node(currentNode, pos)
            if any(openNode for openNode in openList if neighbor == openNode and g_cost >= openNode.g):
                continue

            neighbor.g, neighbor.h = g_cost, heuristic(neighbor, endNode)
            neighbor.f = neighbor.g + neighbor.h
            openList.append(neighbor)
    return None


def display_maze(maze, path):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) in path:
                print("S" if (i, j) == path[0] else "G" if (i, j) == path[-1] else ".", end=" ")
            else:
                print("█" if cell == 1 else "□", end=" ")
        print()


def main():
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    start, end = (6, 0), (4, 6)
    path = aStar(maze, start, end)
    if path:
        print("Path:", path)
        display_maze(maze, path)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
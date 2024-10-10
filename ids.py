import time
import math
import psutil
import os
from collections import deque


class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))
        self.tiles = tiles

    def execute_action(self, action):
        new_tiles = self.tiles[:]
        zero_index = new_tiles.index('0')

        if action == 'L':
            if zero_index % self.size > 0:
                new_tiles[zero_index - 1], new_tiles[zero_index] = new_tiles[zero_index], new_tiles[zero_index - 1]
        if action == 'R':
            if zero_index % self.size < (self.size - 1):
                new_tiles[zero_index + 1], new_tiles[zero_index] = new_tiles[zero_index], new_tiles[zero_index + 1]
        if action == 'U':
            if zero_index - self.size >= 0:
                new_tiles[zero_index - self.size], new_tiles[zero_index] = new_tiles[zero_index], new_tiles[
                    zero_index - self.size]
        if action == 'D':
            if zero_index + self.size < self.size * self.size:
                new_tiles[zero_index + self.size], new_tiles[zero_index] = new_tiles[zero_index], new_tiles[
                    zero_index + self.size]
        return Board(new_tiles)


class Node:
    def __init__(self, state, parent, action):
        # characteristics associated with a node
        self.state = state
        self.parent = parent
        self.action = action


def goal_state(curr_tiles):
    # to check if we have reached our goal state
    return curr_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']


def find_path_to_parent(node):
    # finding the path back to root node - ( gives final action string)
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path = path[::-1]
    return path


def depth(node):
    # returns the depth of the tree (l that we have explored so far)
    depth = 0
    while node.parent is not None:
        node = node.parent
        depth += 1
    return depth


def is_cycle(node):
    # kind of reached set, we check if give node has been expanded before or not
    # if expanded we return a False meaning node's child will not be added to frontier
    ancestor = node.parent
    while ancestor is not None:
        if node.state.tiles == ancestor.state.tiles:
            return True
        ancestor = ancestor.parent
    return False


def expand(node):
    # we will expand the current node into four possible direction and add then to the graph
    child = []
    action = ['L', 'R', 'U', 'D']
    for i in action:
        child_state = node.state.execute_action(i)
        new_node = Node(child_state, node, i)
        child.append(new_node)
    return child


def depth_limited_search(problem, limit):
    # it will search for our goal state till limit depth otherwise return failure
    # initialize frontier with root node
    frontier = [problem]
    result = "failure"
    count = 0
    while frontier:
        # implementing LIFO
        node = frontier.pop()
        count += 1
        # check for goal state for current node
        if goal_state(node.state.tiles):
            path = find_path_to_parent(node)
            return path, count
        # if we have exceeded the limit we will return cutoff
        if depth(node) > limit:
            result = "cutoff"
        # if still l depth is not reached we expand to child of current node
        # but before expanding we check if current node is expanded or not with is_cycle
        elif not is_cycle(node):
            for child in expand(node):
                frontier.append(child)
    return result


def iterative_deepening_search(root_node):
    # the main implementation where we start with depth = 0 and go till infinity
    # the while loop will work till we find a solution or the memory runs out
    depth = 0
    while True:
        result = depth_limited_search(root_node, depth)
        if result != "cutoff":
            return result
        depth += 1


def main():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024.0
    initial = str(input("initial configuration: "))
    initial_list = initial.split(" ")
    root = Node(Board(initial_list), None, None)
    # formatting the result to a dictionary
    start_time = time.time()
    result = iterative_deepening_search(root)
    end_time = time.time()
    print(result)
    final_memory = process.memory_info().rss / 1024.0
    params = ["Moves", "Number of Nodes expanded", "Memory Used"]
    formatted_result = {}
    formatted_result["Time Taken"] = end_time - start_time
    for param, value in zip(params, result):
        formatted_result[param] = value
    formatted_result[params[-1]] = str(final_memory - initial_memory) + " KB"
    print(formatted_result)


if __name__ == "__main__":
    main()



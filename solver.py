import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys

if __name__ = "__main__":
    main()

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    numOfStudents = len(G)
    bestGroupSoFar = None

    edges = G.edges(data=True)
    sortedEdges = sorted(edges, key = lambda tuple: tuple[2].get['happiness'], reverse = True)
    
    ''' Yaksh's Pseudo Code '''
    # keep track of groups -> currentGroups = [Group Object1, Group Object2]
    # GroupObject will be a class with attributes -> set of members, happiness, stress 
    # GroupObject will have methods to calculate happiness, group stress if potential pair wants to be added

    for i in range(1, len(maxHappinessPerK)):
        # i is our current k value
        C = G.copy()
        C.clear
        currentHappiness = 0
        maxGroupStress = s / i

        while numOfGroups <= i:
            mostHappyPair = sortedEdges[0]

            # determine whether to add mostHappyPair here
            newHappinessAmount = getHappinessAmount()
            groupStressWithPair = getGroupStress()

            if groupStressWithPair <= maxGroupStress:
                C.addEdge(mostHappyPair)
                currentHappiness += newHappinessAmount
            else:
                # To Do: create new group with that added edge 
                numOfGroups += 1

        maxHappinessPerK[i] = currentHappiness

    # BIG To Do: Also need to somehow keep track group current assignments per k, so we can return that 
    return max(maxHappinessPerK)
                

                
            
    
def getHappinessAmount():



def dp_hauffman_solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    # TODO: your code here!
    #for e in G.edges:
    pass

def main():
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
    # path = sys.argv[1]
    # G, s = read_input_file(path)
    # D, k = solve(G, s)
    # assert is_valid_solution(D, G, s, k)
    # print("Total Happiness: {}".format(calculate_happiness(D, G)))
    # write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
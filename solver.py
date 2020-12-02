import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys

if __name__ = "__main__":
    main()

def convertPairGroupToMap(groupAssignments):
    result = {}
    for i in range(len(groupAssignments)):
        result[i] = groupAssignments[i]
    groupAssignments = convert_dictionary(result)
    return groupAssignments

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
    bestAssignment = None
    bestHappiness = 0
    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness'], reverse = True)

    for i in range(1, numOfStudents+1):
        # i is our current k value
        groupAssignments = []

        C = G.copy()
        C.clear()
        currentKHappiness = 0
        maxGroupStress = s / i

        while len(groupAssignments) <= i:
            mostHappyPair = sortedEdges.pop(0) # (u,v,{happiness: 3, stress: 3})
            
            student1 = mostHappyPair[0]
            student2 = mostHappyPair[1]

            mostHappyPairGroup = None # this will be a set of students
            isStudent1Assigned = False
            isStudent2Assigned = False

            for i in range(len(groupAssignments)):
                if student1 in groupAssignments[i]:
                    isStudent1Assigned = True
                    if mostHappyPairGroup == None:
                        mostHappyPairGroup = groupAssignments[i]
                elif student2 in groupAssignments[i]:
                    isStudent2Assigned = True
                    if mostHappyPairGroup == None:
                        mostHappyPairGroup = groupAssignments[i]
                
            
            if isStudent1Assigned and isStudent2Assigned:
                continue
            
            if mostHappyPairGroup == None or len(mostHappyPairGroup) == 0:
                groupAssignments.append(set(student1, student2))
                mostHappyPairGroup = set(student1, student2)
            
            # only adding the edge before stress check so that we can use provided util methods. we will remove if exceeds stress. 
            for vertex in mostHappyPairGroup:
                C.add_edge(student1, vertex)
                C.add_edge(student2, vertex)
            
            roomStress = calculate_stress_for_room(mostHappyPairGroup, C)

            #calculate happiness
            if roomStress <= maxGroupStress:
                roomHappiness = calculate_happiness_for_room(mostHappyPairGroup, C)

            else:
                # To Do: create new group with that added edge 
                for vertex in mostHappyPairGroup:
                    C.remove_edge(student1, vertex)
                    C.remove_edge(student2, vertex)

        if currentKHappiness > bestHappiness:
            bestAssignment = groupAssignments
            bestHappiness = currentKHappiness

    # format they want it in 
    return convertPairGroupToMap()



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
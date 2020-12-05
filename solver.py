import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys

def convertListIntoMap(groupAssignments):
    pairMap = {}
    numOfGroups = 0
    for i in range(len(groupAssignments)):
        for student in groupAssignments[i]:
            pairMap[student] = i
        numOfGroups += 1
    return pairMap, numOfGroups

def passesStressCheck1(G, maxGroupStress, groupAssignments, studentGroup, nonPairedStudent):
    groupIndex = studentGroup[0]
    groupAssignments[groupIndex].add(nonPairedStudent)
    roomStress = calculate_stress_for_room(list(groupAssignments[groupIndex]), G)
    if roomStress <= maxGroupStress:
        return True
    else:
        groupAssignments[groupIndex].remove(nonPairedStudent)
        return False
        
def passesStressCheck2(G, maxGroupStress, student1, student2):
    roomStress = calculate_stress_for_room([student1, student2], G)
    return roomStress <= maxGroupStress

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness'], reverse = True)
    sortedEdgesCopy = sortedEdges.copy()

    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0

    for i in range(1, len(G) + 1):
        groupAssignments = [] # list of student sets
        createdGroups = 0
        maxGroupStress = s / i

        print("Max Group Stress is: " + str(maxGroupStress))

        while createdGroups <= i:
            print("Current K: " + str(i))
            mostHappyPair = sortedEdgesCopy.pop(0) # format: (u, v, {happiness: 3, stress: 3})

            print("Most Happy Pair is: " + str(mostHappyPair))
            print("Length of copy array: " + str(len(sortedEdgesCopy)))
            student1 = mostHappyPair[0]
            student2 = mostHappyPair[1]

            student1Group = (None, None) # (groupAssignmentIndex, set of students in group)
            student2Group = (None, None)

            for i in range(len(groupAssignments)):
                if student1 in groupAssignments[i]:
                    student1Group = (i, groupAssignments[i])
                if student2 in groupAssignments[i]:
                    student2Group = (i, groupAssignments[i])

            print("Student 1 Group is: " + str(student1Group) + " and Student 2 Group is " + str(student2Group))

            if student1Group == (None, None) and student2Group == (None, None):
                if passesStressCheck2(G, maxGroupStress, student1, student2):
                    groupAssignments.append({student1, student2}) # make new group with student 1 and 2
                    createdGroups += 1

            elif student1Group == (None, None) and student2Group != (None, None): 
                if passesStressCheck1(G, maxGroupStress, groupAssignments, student2Group, student1): # adds student 1 to student 2 group to check stress
                    pass

            elif student1Group != (None, None) and student2Group == (None, None): 
                if passesStressCheck1(G, maxGroupStress, groupAssignments, student1Group, student2): # adds student 2 to student 1 group to check stress
                    pass

            elif student1Group != (None, None) and student2Group != (None, None):
                pass # student1 and student2 have already been assigned -> don't add suboptimal pairing
            
            print("Number of created groups: " + str(createdGroups))
            print("Sorted Edges Copy next element is " + str(sortedEdgesCopy[0]))
        
        createdGroups = 0 
        sortedEdgesCopy = sortedEdges.copy() # reset sorted list for next iteration of k

        groupMap, numOfGroups = convertListIntoMap(groupAssignments)
        currentAssignmentHappiness = calculate_happiness(groupMap, G)
        if currentAssignmentHappiness > bestAssignmentHappiness:
            bestAssignment = groupMap
            bestAssignmentHappiness = currentAssignmentHappiness
            optimalK = numOfGroups
        
        print("Group Assignments: " + str(groupAssignments))

    return bestAssignment, optimalK

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'outputs/10.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)
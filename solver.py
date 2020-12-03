import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys

if __name__ = "__main__":
    main()

def convertListIntoMap(groupAssignments):
    pairMap = {}
    numOfGroups = 0
    for i in range(len(groupAssignments)):
    	for student in groupAssignments[i]:
    		pairMap[student] = i
    	numOfGroups += 1
    return pairMap, numOfGroups

def passesStressCheck(G, maxGroupStress, studentGroup, nonPairedStudent):
	studentGroupCopy = studentGroup
	roomStress = calculate_stress_for_room(list(studentGroupCopy.add(nonPairedStudent)), G)
	return roomStress <= maxGroupStress

def passesStressCheck(G, maxGroupStress, student1, student2):
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
    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0

    for i in range(1, len(G) + 1):
        groupAssignments = [] # list of student sets
        createdGroups = 0
        maxGroupStress = s / i

        while createdGroups <= i:
            mostHappyPair = sortedEdges.pop(0) # format: (u, v, {happiness: 3, stress: 3})
            
            student1 = mostHappyPair[0]
            student2 = mostHappyPair[1]

            mostHappyPairGroup = None # set of students

            student1Group = (None, None) # (groupAssignmentIndex, set of students in group)
            student2Group = (None, None)

            for i in range(len(groupAssignments)):
                if student1 in groupAssignments[i]:
                    student1Group = (i, groupAssignments[i])
                if student2 in groupAssignments[i]:
                    student2Group = (i, groupAssignments[i])

            if student1Group == (None, None) and student2Group == (None, None):
            	if passesStressCheck(G, maxGroupStress, student1, student2):
            		groupAssignments.append({student1, student2}) # make new group with student 1 and 2
            		createdGroups += 1

            elif student1Group == (None, None) and student2Group != (None, None): 
            	if passesStressCheck(G, maxGroupStress, student2Group[i], student1):
            		groupIndex = student2Group[0]
            		groupAssignments[groupIndex].append(student1) # add student1 to student2's group
            		createdGroups += 1

            elif student1Group != (None, None) and student2Group == (None, None): 
            	if passesStressCheck(G, maxGroupStress, student1Group[i], student2):
            		groupIndex = student1Group[0]
            		groupAssignments[groupIndex].append(student2) # add student2 to student1's group
            		createdGroups += 1

            elif student1Group != (None, None) and student2Group != (None, None):
            	continue # student1 and student2 have already been assigned -> don't add suboptimal pairing

        groupMap, numOfGroups = convertListIntoMap(groupAssignments)
        currentAssignmentHappiness = calculate_happiness(groupMap, G)
        if currentAssignmentHappiness > bestAssignmentHappiness:
        	bestAssignment = groupMap
        	bestAssignmentHappiness = currentAssignmentHappiness
        	optimalK = numOfGroups

    return bestAssignment, optimalK


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
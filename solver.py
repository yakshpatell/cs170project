import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys
import glob
import os

def convertListIntoMap(groupAssignments):
    pairMap = {}
    numOfGroups = 0
    for i in range(len(groupAssignments)):
        for student in groupAssignments[i]:
            pairMap[student] = i
        numOfGroups += 1
    return pairMap, numOfGroups

def addStudentToGroup(G, maxGroupStress, groupAssignments, studentGroup, nonPairedStudent):
    groupIndex = studentGroup[0]
    groupAssignments[groupIndex].add(nonPairedStudent)
    roomStress = calculate_stress_for_room(list(groupAssignments[groupIndex]), G)
    if roomStress > maxGroupStress:
        groupAssignments[groupIndex].remove(nonPairedStudent)

def addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
    happiestGroup = (None, 0) # (index in groupAssignment, happiness level with both students)
    for i in range(len(groupAssignments)):
        groupAssignments[i].add(student1)
        groupAssignments[i].add(student2)
        roomStress = calculate_stress_for_room(groupAssignments[i], G)
        if roomStress <= maxGroupStress:
            groupHappiness = calculate_happiness_for_room(groupAssignments[i], G)
            happiestGroupHappiness = happiestGroup[1]
            if groupHappiness > happiestGroupHappiness:
                happiestGroup = (i, groupHappiness)
        groupAssignments[i].remove(student1)
        groupAssignments[i].remove(student2)
    if happiestGroup[0] == None:
        roomStress = calculate_stress_for_room([student1, student2], G)
        if roomStress <= maxGroupStress:
            groupAssignments.append({student1, student2})
            return True
    else:
        happiestGroupIndex = happiestGroup[0]
        groupAssignments[happiestGroupIndex].add(student1)
        groupAssignments[happiestGroupIndex].add(student2)	
    return False

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness']/tuple[2]['stress'] if tuple[2]['stress'] > 0 else tuple[2]['happiness'], reverse = True)
    sortedEdgesCopy = sortedEdges.copy()

    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0

    for i in range(1, len(G) + 1):

        groupAssignments = [] # list of student sets

        #print("K: " + str(i))

        createdGroups = 0
        maxGroupStress = s / i

        #print("Max Group Stress: " + str(maxGroupStress))

        while createdGroups <= i and len(sortedEdgesCopy) > 0:
        
            #print("Group Assignments: " + str(groupAssignments))
            #print("length of sortedEdges " + str(len(sortedEdgesCopy)))
            mostHappyPair = sortedEdgesCopy.pop(0) #format: (u, v, {happiness: 3, stress: 3})

            #print("Most Happy Pair is: " + str(mostHappyPair))
            
            #print("Number of created groups: " + str(createdGroups))

            student1 = mostHappyPair[0]
            student2 = mostHappyPair[1]

            student1Group = (None, None) # (groupAssignmentIndex, set of students in group)
            student2Group = (None, None)

            for a in range(len(groupAssignments)):
                if student1 in groupAssignments[a]:
                    student1Group = (a, groupAssignments[a])
                if student2 in groupAssignments[a]:
                    student2Group = (a, groupAssignments[a])

            if student1Group == (None, None) and student2Group == (None, None):
                if createdGroups < i and addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
                    createdGroups += 1

            elif student1Group == (None, None) and student2Group != (None, None): 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student2Group, student1) # adds student 1 to student 2 group to check stress

            elif student1Group != (None, None) and student2Group == (None, None): 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student1Group, student2) # adds student 2 to student 1 group to check stress
           
        createdGroups = 0 
        sortedEdgesCopy = sortedEdges.copy() # reset sorted list for next iteration of k

        groupMap, numOfGroups = convertListIntoMap(groupAssignments)
        currentAssignmentHappiness = calculate_happiness(groupMap, G)
        if currentAssignmentHappiness > bestAssignmentHappiness and len(groupMap) == len(G):
            bestAssignment = groupMap
            bestAssignmentHappiness = currentAssignmentHappiness
            optimalK = numOfGroups
    print(bestAssignment)
    print(optimalK)
    return bestAssignment, optimalK


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     #assert len(sys.argv) == 2
#     #path = sys.argv[1]
#     path = "inputs/small-234.in"
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'small-234.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        print(input_path)
        output_path = 'class_outputs/' + os.path.basename(input_path)[:-3] + '.out'
        G, s = read_input_file(input_path)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        write_output_file(D, output_path)
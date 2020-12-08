import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys
import glob
import os
import statistics

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
    bestGroup = (None, 0) # (index in groupAssignment, happiness level with both students)
    for i in range(len(groupAssignments)):
        groupAssignments[i].add(student1)
        groupAssignments[i].add(student2)
        roomStress = calculate_stress_for_room(groupAssignments[i], G)
        if roomStress <= maxGroupStress:
            groupHappiness = calculate_happiness_for_room(groupAssignments[i], G)
            groupScore = groupHappiness/roomStress
            bestGroupScore = bestGroup[1]
            if groupScore > bestGroupScore:
                bestGroup = (i, groupScore)
        groupAssignments[i].remove(student1)
        groupAssignments[i].remove(student2)
    if bestGroup[0] == None:
        return True
    else:
        bestGroupIndex = bestGroup[0]
        groupAssignments[bestGroupIndex].add(student1)
        groupAssignments[bestGroupIndex].add(student2)	
    return False

def sorthelper(tuple, assignedStudents, hStdDev):
    if tuple[0] not in assignedStudents and tuple[1] not in assignedStudents:
        return (tuple[2]['happiness'] + (2*hStdDev))
    elif tuple[0] not in assignedStudents or (tuple[1] not in assignedStudents):
        return (tuple[2]['happiness'] + (hStdDev))
    elif tuple[0] in assignedStudents and tuple[1] in assignedStudents:
        return tuple[2]['happiness']


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    happinessValues = [tuple[2]['happiness'] for tuple in G.edges(data = True)]
    happinessStdev = statistics.stdev(happinessValues)


    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness'], reverse = True)
    #sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness']/tuple[2]['stress'] if tuple[2]['stress'] > 0 else tuple[2]['happiness'], reverse = True)
    sortedEdgesCopy = sortedEdges.copy()

    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0

    for i in range(1, len(G) + 1):

        groupAssignments = [] # list of student sets
        assigned = 0
        #print("K: " + str(i))

        createdGroups = 0
        maxGroupStress = s / i

        #print("Max Group Stress: " + str(maxGroupStress))
        assignedStudents = set()


        flag = False
        rosettaEdges = sortedEdgesCopy.copy()
        while createdGroups < i and len(sortedEdgesCopy) > 0:
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
                roomStress = calculate_stress_for_room([student1, student2], G)
                if roomStress <= maxGroupStress:
                    groupAssignments.append({student1, student2})
                    createdGroups += 1
                    assigned += 2
                    rosettaEdges.pop(0)
                    assignedStudents.add(student1)
                    assignedStudents.add(student2)


        shiftedEdges = sorted(rosettaEdges,key = lambda tuple: sorthelper(tuple,assignedStudents,happinessStdev))
        shiftedEdgesCopy = (shiftedEdges.copy())*3
        while assigned < len(G) and len(shiftedEdgesCopy) > 0:
            #print("Group Assignments: " + str(groupAssignments))
            #print(i)
            #print(createdGroups)
            #print(assigned)
            #print("length of sortedEdges " + str(len(sortedEdgesCopy)))
            mostHappyPair = shiftedEdgesCopy.pop(0) #format: (u, v, {happiness: 3, stress: 3})
    
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

            if student1Group == (None, None) and student2Group == (None, None) and flag == True:
                if not addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
                    assigned += 2


            elif student1Group == (None, None) and student2Group != (None, None) and flag == True: 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student2Group, student1) # adds student 1 to student 2 group to check stress
                assigned += 1

            elif student1Group != (None, None) and student2Group == (None, None) and flag == True: 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student1Group, student2) # adds student 2 to student 1 group to check stress
                assigned += 1

        print("groups: " + str(createdGroups) + " K: " + str(i))      
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

if __name__ == '__main__':
    #assert len(sys.argv) == 2
    #path = sys.argv[1]
    path = "inputs/medium-125.in"
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'medium-125.out')


#For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         print(input_path)
#         output_path = 'class_outputs/' + os.path.basename(input_path)[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)
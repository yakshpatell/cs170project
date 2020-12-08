import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary, calculate_stress_for_room, calculate_happiness_for_room
import sys
import glob
import os
import heapq 

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

# def addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
#     leastStressedGroup = (None, 0) # (index in groupAssignment, ratio score of h/s)
#     for i in range(len(groupAssignments)):
#         groupAssignments[i].add(student1)
#         groupAssignments[i].add(student2)
#         currentRoomStress = calculate_stress_for_room(groupAssignments[i], G)
#         if roomStress <= maxGroupStress:
#             leastStress = leastStressedGroup[1]
#             if currentRoomStress < leastStress:
#                 leastStressedGroup = (i, currentRoomStress)
#         groupAssignments[i].remove(student1)
#         groupAssignments[i].remove(student2)
#     if happiestGroup[0] == None:
#         roomStress = calculate_stress_for_room([student1, student2], G)
#         if roomStress <= maxGroupStress:
#             groupAssignments.append({student1, student2})
#             return True
#     else:
#         leastStressGroupIndex = leastStressedGroup[0]
#         groupAssignments[leastStressGroupIndex].add(student1)
#         groupAssignments[leastStressGroupIndex].add(student2)	
#     return False

def addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
    roomStress = calculate_stress_for_room([student1, student2], G)
    if roomStress <= maxGroupStress:
        groupAssignments.append({student1, student2})
        return True
    return False

# def packRestOfStudents(G, groupAssignments, numberOfStudents, numOfCreatedGroups, maxGroupStress, sortedEdges):

# 	sortedByIncreasingStress = sorted(sortedEdges, key = lambda tuple: tuple[2]['stress'])

# 	# add new code logic here !!!
# 	# smallestStressPair = pop(0)
# 	# track whether we see either one
# 	# until all students have been assigned
# 	## if one is assigned, and other isn't, add to group
# 	## if both are assigned, pass to next iteration 
# 	## if none are assigned, pass to next iteration

#     studentsInGroups = set()
#     numberOfAssignedStudents = 0
# 	for i in range(len(groupAssignments)):
# 		for student in groupAssignments[i]:
# 			studentsInGroups.add(student)
#             numberOfAssignedStudents += 1

#     while numberOfAssignedStudents < numberOfStudents:
#         if len(sortedByIncreasingStress) == 0:
#             return False
#         smallestStressPair = sortedByIncreasingStress.pop(0)

#         student1 = smallestStressPair[0]
#         student2 = smallestStressPair[1]

#         student1Group = (None, {}) # (groupAssignmentIndex, set of students in group)
#         student2Group = (None, {})

#         for a in range(len(groupAssignments)):
#             if student1 in groupAssignments[a]:
#                 student1Group = (a, groupAssignments[a])
#             if student2 in groupAssignments[a]:
#                 student2Group = (a, groupAssignments[a])

#         if student1Group != (None, {}) and student2Group != (None, {}):
            







# 	stressMappings = {}
# 	roomStressList = []
# 	for i in range(len(groupAssignments)):
# 		roomStress = calculate_stress_for_room(list(groupAssignments[i]), G)
# 		stressMappings[roomStress] = i
# 		roomStressList.append(roomStress)

# 	heapq.heapify(roomStressList)

# 	studentsInGroups = set()
# 	for i in range(len(groupAssignments)):
# 		for student in groupAssignments[i]:
# 			studentsInGroups.add(student)

# 	for student in range(numberOfStudents):
# 		if student in studentsInGroups:
# 			continue
# 		else:
# 			isStudentAssigned = False
# 			while not isStudentAssigned:
# 				if len(roomStressList) == 0:
# 					return None

# 				leastStressValue = heapq.heappop(roomStressList)
# 				roomToFillIndex = stressMappings[leastStressValue]
# 				groupAssignments[roomToFillIndex].add(student)
# 				roomStressWithStudent = calculate_stress_for_room(list(groupAssignments[roomToFillIndex]), G)

# 				if roomStressWithStudent > maxGroupStress:
# 					groupAssignments[roomToFillIndex].remove(student)
# 				else:
# 					isStudentAssigned = True
# 					stressMappings[roomStressWithStudent] = i
# 					heapq.heappush(roomStressList, roomStressWithStudent)
# 					print("SAVED STUDENT FROM NO GROUP!")
# 	return groupAssignments

def getDefaultAssignment(numOfStudents):
	getDefaultAssignment = {}
	for i in range(numOfStudents):
		getDefaultAssignment[i] = i
	return getDefaultAssignment
	

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    # sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness']/tuple[2]['stress'] if tuple[2]['stress'] > 0 else tuple[2]['happiness'], reverse = True)
    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness'], reverse = True)

    sortedEdgesCopy = sortedEdges.copy()

    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0
    numberOfStudents = len(G)

    for i in range(1, numberOfStudents + 1):

        groupAssignments = [] # list of student sets
        numberOfAssignedStudents = 0

        numOfCreatedGroups = 0
        maxGroupStress = s / i

        while numOfCreatedGroups <= i and len(sortedEdgesCopy) > 0:

            mostHappyPair = sortedEdgesCopy.pop(0) # format: (u, v, {happiness: 3, stress: 3})

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
                if numOfCreatedGroups < i and addedNewGroup(student1, student2, G, groupAssignments, maxGroupStress):
                    numOfCreatedGroups += 1

            elif student1Group == (None, None) and student2Group != (None, None): 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student2Group, student1) # adds student 1 to student 2 group to check stress

            elif student1Group != (None, None) and student2Group == (None, None): 
                addStudentToGroup(G, maxGroupStress, groupAssignments, student1Group, student2) # adds student 2 to student 1 group to check stress
        
        sortedEdgesCopy = sortedEdges.copy()

        # groupAssignments = packRestOfStudents(G, groupAssignments, numberOfStudents, numOfCreatedGroups, maxGroupStress, sortedEdges)
        if groupAssignments == None:
        	continue

        groupMap, numOfGroups = convertListIntoMap(groupAssignments)
        currentAssignmentHappiness = calculate_happiness(groupMap, G)
        if currentAssignmentHappiness > bestAssignmentHappiness:
            bestAssignment = groupMap
            bestAssignmentHappiness = currentAssignmentHappiness
            optimalK = numOfGroups

    if bestAssignment == None:
        defaultAssignment = getDefaultAssignment(numberOfStudents)
        print("Best Assignment: " + str(defaultAssignment))
        print("Optimal K: " + str(numberOfStudents))
        return defaultAssignment, numberOfStudents
        
    print("Best Assignment: " + str(bestAssignment))
    print("Optimal K: " + str(optimalK))
    return bestAssignment, optimalK


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    #assert len(sys.argv) == 2
    #path = sys.argv[1]
    path = "inputs/small-203.in"
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'small-203.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         print(input_path)
#         output_path = 'class_outputs/' + os.path.basename(input_path)[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         print("Total Happiness: {}".format(calculate_happiness(D, G)))
#         write_output_file(D, output_path)
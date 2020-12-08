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
        return True
    return False

def getDefaultAssignment(numOfStudents):
	getDefaultAssignment = {}
	for i in range(numOfStudents):
		getDefaultAssignment[i] = i
	return getDefaultAssignment

def createPairGroups(G, sortedEdges, stressThreshold):
    numOfGroupsToCreate = len(G)//2
    maxGroupStress = stressThreshold  / (1.2 * numOfGroupsToCreate)
    groupAssignments = []
    numOfGroups = 0
    assignedStudents = []
    while len(sortedEdges) > 0 and numOfGroups < numOfGroupsToCreate:
        mostHappyPair = sortedEdges.pop(0)
        currentGroup = {mostHappyPair[0], mostHappyPair[1]}
        roomStress = calculate_stress_for_room(currentGroup, G)
        if roomStress <= maxGroupStress:
            groupAssignments.append(currentGroup)
            assignedStudents.append(mostHappyPair[0])
            assignedStudents.append(mostHappyPair[1])
            sortedEdges = list(filter(lambda x: x[0] not in currentGroup and x[1] not in currentGroup, sortedEdges))
            numOfGroups += 1
    if numOfGroups == numOfGroupsToCreate:
        return convertListIntoMap(groupAssignments)
    notassigned = [i for i in range(len(G)) if i not in assignedStudents]
    for s in notassigned:
        groupAssignments.append({s})
    D,numK = convertListIntoMap(groupAssignments)
    if is_valid_solution(D,G,stressThreshold,numK):
        return D,numK
    return None, len(G) # return defaultAssignment instead
        
def addStudentsToExisitingGroups(student1, student2, G, groupAssignments, maxGroupStress):
    leastStressedGroup = (None, 0) # (index in groupAssignment, least stress)
    for i in range(len(groupAssignments)):
        groupAssignments[i].add(student1)
        groupAssignments[i].add(student2)
        roomStress = calculate_stress_for_room(groupAssignments[i], G)
        if roomStress <= maxGroupStress and roomStress < leastStressedGroup[1]:
            leastStressedGroup = (i, roomStress)
        groupAssignments[i].remove(student1)
        groupAssignments[i].remove(student2)
    if leastStressedGroup[0] == None:
        return False
    groupAssignments[leastStressedGroup[0]].add(student1)
    groupAssignments[leastStressedGroup[0]].add(student2)	
    return True

def solve(G, s):
    sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['happiness'], reverse = True)
    # sortedEdges = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['stress'], reverse = True)
    sortedEdgesCopy = sortedEdges.copy()
    sortedEdgesCopy = sortedEdgesCopy*3
    bestAssignment = None
    bestAssignmentHappiness = 0
    optimalK = 0
    numberOfStudents = len(G)
    for i in range(1, numberOfStudents + 1):
        groupAssignments = []
        assigned = 0
        createdGroups = 0
        maxGroupStress = s / i
        areGroupsMaxed = False
        while assigned < len(G) and len(sortedEdgesCopy) > 0:
            mostHappyPair = sortedEdgesCopy.pop(0) # format: (u, v, {happiness: 3, stress: 3})
            if createdGroups == i:
                areGroupsMaxed = True
            student1 = mostHappyPair[0]
            student2 = mostHappyPair[1]
            student1Group = (None, None) # (groupAssignmentIndex, set of students in group)
            student2Group = (None, None)
            for a in range(len(groupAssignments)):
                if student1 in groupAssignments[a]:
                    student1Group = (a, groupAssignments[a])
                if student2 in groupAssignments[a]:
                    student2Group = (a, groupAssignments[a])
            if student1Group == (None, None) and student2Group == (None, None) and areGroupsMaxed == False:
                roomStress = calculate_stress_for_room([student1, student2], G)
                if roomStress <= maxGroupStress:
                    groupAssignments.append({student1, student2})
                    createdGroups += 1
                    assigned += 2
            elif student1Group == (None, None) and student2Group == (None, None) and areGroupsMaxed == True:
                if addStudentsToExisitingGroups(student1, student2, G, groupAssignments, maxGroupStress):
                    assigned += 2
            elif student1Group == (None, None) and student2Group != (None, None) and areGroupsMaxed == True: 
                if addStudentToGroup(G, maxGroupStress, groupAssignments, student2Group, student1): # adds student 1 to student 2 group to check stress
                    assigned += 1
            elif student1Group != (None, None) and student2Group == (None, None) and areGroupsMaxed == True: 
                if addStudentToGroup(G, maxGroupStress, groupAssignments, student1Group, student2): # adds student 2 to student 1 group to check stress
                    assigned += 1
        createdGroups = 0 
        sortedEdgesCopy = sortedEdges.copy() # reset sorted list for next iteration of k
        sortedEdgesCopy = sortedEdgesCopy*3
        groupAssignments = packRestOfStudents(G, groupAssignments, numberOfStudents, createdGroups, maxGroupStress, sortedEdges)
        if groupAssignments == None:
        	continue
        groupMap, numOfGroups = convertListIntoMap(groupAssignments)
        currentAssignmentHappiness = calculate_happiness(groupMap, G)
        if currentAssignmentHappiness > bestAssignmentHappiness:
            bestAssignment = groupMap
            bestAssignmentHappiness = currentAssignmentHappiness
            optimalK = numOfGroups
    if bestAssignment == None and optimalK == 0:
        sortedEdgesByS = sorted(G.edges(data=True), key = lambda tuple: tuple[2]['stress'])
        bestAssignment, optimalK = createPairGroups(G, sortedEdgesByS, s)
        if bestAssignment == None:
            print("No!")
            bestAssignment = getDefaultAssignment(numberOfStudents)
            optimalK = numberOfStudents
        else:
            print("YES! " + " happiness: " + str(calculate_happiness(bestAssignment,G)))
    # print("Optimal K: " + str(optimalK))
    # print("Group Assignment: " + str(groupAssignments))
    return bestAssignment, optimalK

def packRestOfStudents(G, groupAssignments, numberOfStudents, numOfCreatedGroups, maxGroupStress, sortedEdges):
	stressMappings = {}
	roomStressList = []
	for i in range(len(groupAssignments)):
		roomStress = calculate_stress_for_room(list(groupAssignments[i]), G)
		stressMappings[roomStress] = i
		roomStressList.append(roomStress)
	heapq.heapify(roomStressList)
	studentsInGroups = set()
	for i in range(len(groupAssignments)):
		for student in groupAssignments[i]:
			studentsInGroups.add(student)
	for student in range(numberOfStudents):
		if student in studentsInGroups:
			continue
		else:
			isStudentAssigned = False
			while not isStudentAssigned:
				if len(roomStressList) == 0:
					return None
				leastStressValue = heapq.heappop(roomStressList)
				roomToFillIndex = stressMappings[leastStressValue]
				groupAssignments[roomToFillIndex].add(student)
				roomStressWithStudent = calculate_stress_for_room(list(groupAssignments[roomToFillIndex]), G)
				if roomStressWithStudent > maxGroupStress:
					groupAssignments[roomToFillIndex].remove(student)
				else:
					isStudentAssigned = True
					stressMappings[roomStressWithStudent] = i
					heapq.heappush(roomStressList, roomStressWithStudent)
	return groupAssignments
            
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
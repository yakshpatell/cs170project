import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys


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
    maxHappinessPerK = [0 for i in range(numOfStudents+1)]

    edges = G.edges(data=True)
    sortedEdges = sorted(edges, key = lambda tuple: tuple[2].get['happiness'], reverse = True)
    
    for i in range(1, len(maxHappinessPerK)):
        ''' 
            calculate Sgroup depending on current k iteration 
            for each k:
                currentHappiness = 0
                while k is not reached and Sgroup is not reached:
                    make new group
                    using the decreasing sort, enumerate group until Sgroup is reached
                maxHappinessPerK[k] = currentHappiness
            
            return max()
        '''
        pass
                

                
            
            
                


    
    pass


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

if __name__ = "__main__":
    main()



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
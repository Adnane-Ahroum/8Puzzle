# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    
    counter_expanded=0
    fringe_len=0

    #states to be explored (LIFO). holds nodes in form (state, action)
    frontier = util.Stack()
    #previously explored states (for path checking), holds states
    exploredNodes = []
    #define start node
    startState = problem.getStartState()
    startNode = (startState, [])
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():
        fringe_len= max(len(frontier.list), fringe_len)        

        
        #begin exploring last (most-recently-pushed) node on frontier
        currentState, actions = frontier.pop()
        
        if currentState not in exploredNodes:
            #mark current node as explored
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return actions, counter_expanded, fringe_len, len(actions)
            else:
                #increment the expanded nodes counter
                counter_expanded+=1

                #get list of possible successor nodes in 
                #form (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                #push each successor to frontier
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    frontier.push(newNode)
            
                fringe_len= len(frontier.list)

    return actions, counter_expanded, fringe_len, len(actions) 

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    counter_expanded=0
    fringe_len=0

    #to be explored (FIFO)
    frontier = util.Queue()
    
    #previously expanded states (for cycle checking), holds states
    exploredNodes = []
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():

        fringe_len= max(len(frontier.list), fringe_len)        
        #begin exploring first (earliest-pushed) node on frontier
        currentState, actions, currentCost = frontier.pop()
        
        if currentState not in exploredNodes:
            #put popped node state into explored list
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return actions, counter_expanded, fringe_len, len(actions)
            else:
                #increment the expanded nodes counter
                counter_expanded+=1

                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    frontier.push(newNode)
                
                fringe_len= len(frontier.list)

    return actions,counter_expanded, fringe_len, len(actions)
        
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    counter_expanded=0
    fringe_len=0

    #to be explored (FIFO): holds (item, cost)
    frontier = util.PriorityQueue()

    #previously expanded states (for cycle checking), holds state:cost
    exploredNodes = {}
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    frontier.push(startNode, 0)
    
    while not frontier.isEmpty():
        
        fringe_len= max(len(list(frontier.heap)), fringe_len)        

        #begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost = frontier.pop()
       
        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            #put popped node's state into explored list
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                return actions, counter_expanded, fringe_len, len(actions)
            else:
                #increment the expanded nodes counter
                counter_expanded+=1

                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    frontier.update(newNode, newCost)

                

    return actions, counter_expanded, fringe_len, len(actions)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

"""/*=====Start Change Task i=====*/"""

def h1(state, problem=None):
    """
    This heuristic caclulate misplaced tiles
    """
    #a is the number of misplaced tiles
    a=0
    #actual_arr is the current state of the board
    actual_arr = (state.cells[:])
    #goal_arr is the goal state of the board
    goal_arr =[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    #we compare the current state with the goal state and increment a if the tiles are misplaced
    for i in range(3):
        for j in range(3):
            if(goal_arr[i][j] != actual_arr[i][j] and state.cells[i][j]!=0):
                a+=1 
    return a

def h2(state, problem =None):
    """
    This heuristic caclulate euclidian distance
    """
    euclidian_sum=0
    # I calculate the euclidian distance (0 if the number in right place) for each cell and sum them up 
    for i in range(3):
        for j in range(3):
            if (state.cells[i][j]!=0):
                euclidian_sum += ((i - (state.cells[i][j] // 3))**2 + (j -  (state.cells[i][j] % 3))**2)**0.5
    return round(euclidian_sum, 2)

def h3(state, problem=None):
    """
    This heuristic caclulate manhattan distance
    """
    
    manhattan_sum=0
    # I calculate the manhattan distance (0 if the number in right place) for each cell and sum them up 
    for i in range(3):
        for j in range(3):
            if(state.cells[i][j]!=0):
                manhattan_sum += abs(i - (state.cells[i][j] // 3)) + abs(j -  (state.cells[i][j] % 3))
    return manhattan_sum

def h4(state, problem=None):
    """
    This heuristic caclulate number of tiles out of row and column
    """
    total_misplaced=0
    for i in range(3):
        for j in range(3):
            if(state.cells[i][j]//3 != i and state.cells[i][j]!=0):
                total_misplaced+=1
            if(state.cells[i][j]%3 != j and state.cells[i][j]!=0):
                total_misplaced+=1
    return total_misplaced
"""/*=====End Change Task i =====*/"""


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    #to be explored (FIFO): takes in item, cost+heuristic
    frontier = util.PriorityQueue()

    exploredNodes = [] #holds (state, cost)
    
    counter_expanded=0
    fringe_len=0
    #tree_data= [0,0,0] #holds (nb_explored_nodes, fringe_len, depth)

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)

    frontier.push(startNode, 0)
    
    while not frontier.isEmpty():

        fringe_len= max(len(list(frontier.heap)), fringe_len)        
        #begin exploring first (lowest-combined (cost+heuristic) ) node on frontier
        currentState, actions, currentCost = frontier.pop()

        #put popped node into explored list
        currentNode = (currentState, currentCost)
        exploredNodes.append((currentState, currentCost))
        
        if problem.isGoalState(currentState): 
            return actions, counter_expanded, fringe_len, len(actions)

        else:
            #increment the expanded nodes counter
            counter_expanded+=1                    
            
            #list of (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)

            #examine each successor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                newNode = (succState, newAction, newCost)

                #check if this successor has been explored
                already_explored = False
                for explored in exploredNodes:
                    #examine each explored node tuple
                    exploredState, exploredCost = explored

                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True

                #if this successor not explored, put on frontier and explored list
                if not already_explored:
                    frontier.push(newNode, newCost + heuristic(succState, problem))
                    exploredNodes.append((succState, newCost))


    return actions, counter_expanded, fringe_len, len(actions)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

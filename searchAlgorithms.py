import codecs
import sys
import os
import heapq
import queue

#https://www.w3schools.com/python/python_dictionaries.asp
#https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
#https://www.geeksforgeeks.org/queue-in-python/
#https://www.geeksforgeeks.org/python-nested-dictionary/
#https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/
#https://www.geeksforgeeks.org/priority-queue-in-python/



class node:

    def __init__(self, state, parent=None, cost=0.0, funct=0.0):
        self.parent= parent
        self.cost=cost
        self.state=state
        self.funct=funct


    def expand(self, states):
        temp =states.get(self.state)
        successors= queue.Queue()
        for k, v in temp.items():
            new_state=k
            new_cost= self.cost + int(v)
            new_parent= self
            new_node= node(new_state, new_parent, new_cost)
            successors.put(new_node)

        return successors

    def cost_and_heur(self, heur):
        return int(heur) + self.cost


    def __lt__(self, other):

        if self.funct==0:
            return self.cost<other.cost
        else:
            return (self.cost+ int(self.funct) < (other.cost+ int(other.funct)))

# def path(self):


def output(algorithm, heuristic, found_solution, visited, length, cost, path):
    if algorithm == 'A-STAR':
        print('# {0} {1}'.format(algorithm, heuristic))
    else:
        print('# {0}'.format(algorithm))

    if found_solution == 'no':
        print('[FOUND_SOLUTION]: {0}'.format(found_solution))

    else:
        print('[FOUND_SOLUTION]: {0}'.format(found_solution))
        print('[STATES_VISITED]: {0}'.format(visited))
        print('[PATH_LENGTH]: {0}'.format(length))
        print('[TOTAL_COST]: {0}'.format(cost))

        formattedPath=' => '.join(n for n in path)
        print('[PATH]: {0} '.format(formattedPath))

def heurLoading(path):

    heuristics= {}

    with codecs.open(path, 'r', 'utf-8') as heur:

        for line in heur:

            splitLine=line.strip().split(':')

            heuristics[splitLine[0]]=splitLine[1]

    return heuristics



def dataLoading(path):
    states = {}

    start=''
    goals=[]
    with codecs.open(path, 'r', 'utf-8') as stat:
        for  line in stat:

            if '#' in line:
                continue
            elif ':' not in line:
                if start == '':
                    start = line.replace('\n', '')
                else:
                    goals=line

            else:
                state, next_state = line.strip().split(':')

                test=next_state.strip().split(' ')

                transitions = {}
                for t in test :
                    if t != '':
                        k, v = t.split(',')
                        transitions[k]=v




                states[state.strip()] = transitions



    return states, start, goals

def BFS(s0, succ, goal):

    open =queue.Queue()

    open.put(s0)

    visited= set()
    visited.add(s0.state)

    while not open.empty() :
        n= open.get()

        if n.state in goal:
            path = []
            cost = n.cost
            while n:
                path.append(n.state)
                n = n.parent

            return 'yes', len(visited), len(path), cost, path[::-1]

        expanded = n.expand(succ)

        while not expanded.empty():

            exp= expanded.get()

            if exp.state not in visited:
                visited.add(exp.state)
                open.put(exp)

    return 'no'


def UCS(s0, succ, goal):

    open=queue.PriorityQueue()

    open.put(s0)

    visited = set()



    while not open.empty():

        n=open.get()

        if n.state in goal:
            path = []
            cost=n.cost
            while n:
                path.append(n.state)
                n = n.parent



            return 'yes',  len(visited),len(path),  cost, path[::-1]

        expanded= n.expand(succ)
        visited.add(n.state)
        while not expanded.empty():

            exp=expanded.get()

            if exp.state not in visited:

                open.put(exp)

    return 'no'

def ASTAR(s0, succ, goal, h):

    open=queue.PriorityQueue()

    open.put(s0)

    closed=set()

    while not open.empty():
        n=open.get()

        if n.state in goal:
            path = []
            cost = n.cost
            while n:
                path.append(n.state)
                n = n.parent


            return 'yes', cost ,path[::-1] , len(closed),len(path)
        closed.add(n.state)
        expanded=n.expand(succ)

        while not expanded.empty():
            exp=expanded.get()
            if exp in closed:
                continue

            exp.funct=h.get(exp.state)

            open.put(exp)



    return 'no'


def is_optimistic(heuristic, states, goal, path):

        optimistic=True
        print('# HEURISTIC-OPTIMISTIC {}'.format(path))

        for state, value in heuristic.items():

            new_node=node(state=state)

            s,v, p, cost , m= UCS(new_node,states, goal )

            if float(value) > float(cost):
                optimistic=False
                print('[CONDITION]: [ERR] h({0}) <= h*: {1} <= {2}'.format(state, float(value), float(cost)))

            else:
                print('[CONDITION]: [OK] h({0}) <= h*: {1} <= {2}'.format(state, float(value), float(cost)))

        if optimistic:
            print('[CONCLUSION]: Heuristic is optimistic.')
        else:
            print('[CONCLUSION]: Heuristic is not optimistic.')

def is_consistent(heuristic, states, path):

    print('# HEURISTIC-CONSISTENT {0}'.format(path))
    is_consistent=True
    for state, value in states.items():

        for inner_state, inner_value in value.items():

            if float(heuristic.get(state))  <= float(heuristic.get(inner_state)) + float(inner_value):
                print('[CONDITION]: [OK] h({0}) <= h({1}) + c: {2}  <= {3} + {4}'.format(state, inner_state, float(heuristic.get(state)), float(heuristic.get(inner_state)) , float(inner_value)))

            else:
                print('[CONDITION]: [ERR]  h({0}) <= h({1})  + c: {2} <= {3} + {4}'.format(state, inner_state, float(heuristic.get(state)), float(heuristic.get(inner_state)) , float(inner_value)))
                is_consistent=False




    if is_consistent:
        print('[CONCLUSION]: Heuristic is consistent.')
    else:
        print('[CONCLUSION]: Heuristic is not consistent.')

def main():
    data = []

    data = sys.argv

    if 'bfs' in data:

        index = data.index('--ss')

        states = data[index + 1]


        states, start, goals= dataLoading(states)

        start_node= node(state=start)

        found,visited, pathlen, cost, path=BFS(start_node,states, goals )

        output('BFS', '',found, visited, pathlen, cost, path)

    elif 'ucs' in data:
        index = data.index('--ss')

        states = data[index + 1]

        states, start, goal = dataLoading(states)

        start_node=node(start)

        found,visited, pathlen, cost, path=UCS(start_node,states,goal)

        output('UCS', 'no',found, visited, pathlen, cost, path)

    elif 'astar' in data:

        index = data.index('--ss')
        heuristicIndex = data.index('--h')

        states = data[index + 1]
        heuristic = data[heuristicIndex + 1]

        states, start, goals = dataLoading(states)

        start_node = node(start)

        heur=heurLoading(heuristic)

        found,cost, path, visited, lenpath=ASTAR(start_node,states,goals,heur)

        output('A-STAR', heuristic, found, visited, lenpath, cost, path )

    elif '--check-optimistic' in data:

        index=data.index('--ss')

        path= data[index+1]

        states, start, goal = dataLoading(path)

        heurindex=data.index('--h')

        pathheur=data[heurindex+1]

        heur=heurLoading(pathheur)

        is_optimistic(heur,states, goal,pathheur)

    elif '--check-consistent' in data:

        index = data.index('--ss')

        path = data[index + 1]

        states, start, goal = dataLoading(path)

        heurindex = data.index('--h')

        pathheur = data[heurindex + 1]

        heur = heurLoading(pathheur)

        is_consistent(heur, states, pathheur)

if __name__ == '__main__':
    main()

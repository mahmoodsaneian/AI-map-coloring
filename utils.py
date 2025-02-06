import random
from queue import PriorityQueue
from collections import deque
def is_consistent(graph, variable_value_pairs):
    """
        returns True if the variables that have been assigned a value so far are consistent with the constraints, 
        and False otherwise.
        
        variable_value_pairs can be used to access any value of any variable from the variable as a key
        you can use variable_value_pairs.items() to traverse it as (state, color) pairs
                    variable_value_pairs.keys() to get all the variables,         
                and variable_value_pairs.values() to get all the values
    """
    for state, color in variable_value_pairs.items():
        if(variable_value_pairs[state] != None):
            for neihgbor in graph[state]:
                if variable_value_pairs[neihgbor] == color:
                    return False
    return True

def is_solved(graph, variable_value_pairs):
    """
        returns True if the CSP is solved, and False otherwise
    """
    for state in variable_value_pairs.keys():
        if variable_value_pairs[state] == None:
            return False
        color = variable_value_pairs[state]
        for neighbor in graph[state]:
            if variable_value_pairs[neighbor] == color:
                return False
    return True
    

def get_next_variable(variable_value_pairs, domains):
    """
        returns the index of the next variable from the default order of the unassinged variables
    """
    for i, state in enumerate(domains):
        if variable_value_pairs[i] == None:
            return i
    return None
    

def get_chosen_variable(graph, variable_value_pairs, domains):
    """
        returns the next variable that is deemed the best choice by the proper heuristic
        use a second heuristic for breaking ties from the first heuristic
    """
    "MRV & degree heuristic"
    return min([state for state in graph if variable_value_pairs[state] is None],
               key=lambda x: (len(domains[x]), -len(graph[x])))
    
    
def get_ordered_domain(graph, domains, state):
    """
        returns the domain of the varibale after ordering its values by the proper heuristic
        (you may use imports here)
    """
    priority_queue = PriorityQueue()
    for value in domains[state]:
        priority_queue.put((sum(1 for neighbour in graph[state] if value in domains[neighbour]), value))
    ordered_values = []
    while not priority_queue.empty():
        ordered_values.append(priority_queue.get()[1])
    return ordered_values
    

def forward_check(graph, variable_value_pairs, domains, state, value):
    """
        removes the value assigned to the current variable from its neighbors
        returns True if backtracking is necessary, and False otherwise
    """
    for neighbor in graph[state]:
        if variable_value_pairs[neighbor] is None:
            if value in domains[neighbor]:
                domains[neighbor].remove(value)
            if len(domains[neighbor]) == 0:
                return True
    return False
    
def ac3(graph, variable_value_pairs, domains):
    """
        maintains arc-consistency
        returns True if backtracking is necessary, and False otherwise
    """
    queue = []
    for vertex in set(graph.keys()):
        for neighbour in graph[vertex]:
            queue.append((vertex, neighbour))
    while not queue == []:
        vertex_a, vertex_b = queue.pop(0)
        changed = False
        if variable_value_pairs[vertex_b] is not None and variable_value_pairs[vertex_b] in domains[vertex_a]:
            domains[vertex_a].remove(variable_value_pairs[vertex_b])
            changed = True
        if changed:
            for vertex in set(graph.keys()) - {vertex_a}:
                if vertex_a in graph[vertex]:
                    queue.append((vertex, vertex_a))
    return any(domain == [] for domain in domains)


def random_choose_conflicted_var(graph, variable_value_pairs):
    """
        returns a random variable that is conflicting with a constrtaint
    """
    conflicted_vars = []
    for state, value in variable_value_pairs.items():
        for neighbor in graph[state]:
            if neighbor in variable_value_pairs and variable_value_pairs[neighbor] == value:
                conflicted_vars.append(state)
                break
    if conflicted_vars: 
        return random.choice(conflicted_vars)
    else:
        return None
    
def get_chosen_value(graph, variable_value_pairs, domains, state):
    """
        returns the value by using the proper heuristic
        NOTE: handle tie-breaking by random
    """
    neighbor_colors = {neighbor: variable_value_pairs[neighbor] for neighbor in graph[state]}
    conflicts = []
    for value in domains[state]:
        conflicts.append((value,sum(1 for neighbor in graph[state] if neighbor_colors.get(neighbor) == value)))

    min_conflict_value = min(conflicts, key=lambda x: x[1])[1]
    min_tuples = [tuple for tuple in conflicts if tuple[1] == min_conflict_value]
    return random.choice(min_tuples)[0]
    
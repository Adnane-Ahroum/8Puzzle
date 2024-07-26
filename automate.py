import random, csv, search, util
import eightpuzzle
from os import path
import time
import pandas as pd



def generate_senarios(seed=0, n=3, nb_senarios=100):
    """
    This function is used to generate different senarios for the n*n puzzle game
    """
    
    senarios = set()
    for i in range(nb_senarios):
        puzzle = eightpuzzle.createRandomEightPuzzle(2)
        #flatten the puzzle to a list
        puzzle_elems = [item for sublist in puzzle.cells for item in sublist]
        senarios.add(tuple(puzzle_elems))

    return list(senarios)

def save_to_csv(senarios, file_name):
    """
    This function is used to save the senarios to a csv file
    """
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(senarios)

def load_from_csv(file_name):
    """
    This function is used to load the senarios from a csv file
    """
    senarios = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            senarios.append([int(x) for x in row])
    return senarios
   
def task2_solve_and_compare(senario, senario_index):
    """
    This function is used to solve the puzzle using A* with different heuristics and compare the results 
    """
    puzzle = eightpuzzle.EightPuzzleState(senario)
    print('current: ,', puzzle.cells)
    problem = eightpuzzle.EightPuzzleSearchProblem(puzzle)

    summary_data=[]

    ########### The Different Heuristics ##############
    #1
    path1, counter_expanded, fringe_len, depth = search.aStarSearch(problem, search.h1)
    summary_data.append({'Index':f's{senario_index}:h1', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path1})
    #2
    path2, counter_expanded, fringe_len, depth = search.aStarSearch(problem, search.h2)
    summary_data.append({'Index':f's{senario_index}:h2', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path2})
    #3

    path3,counter_expanded, fringe_len, depth = search.aStarSearch(problem, search.h3)
    summary_data.append({'Index':f's{senario_index}:h3', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path3})

    #4
    path4,counter_expanded, fringe_len, depth = search.aStarSearch(problem, search.h4)
    summary_data.append({'Index':f's{senario_index}:h4', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path4})

    if(not path1 == path2 == path3 == path4):
        save_to_csv( [senario, path1,path2,path3, path4], 'ASdiffSearch.csv')

    ###################################################"""
    return summary_data

def task3_solve_and_compare(senario, senario_index):
    """
    This function is used to solve the puzzle different approaches and compare the results 
    """
    puzzle = eightpuzzle.EightPuzzleState(senario)
    print('current: ,', puzzle.cells)
    problem = eightpuzzle.EightPuzzleSearchProblem(puzzle)

    summary_data=[]
    #BFS
    path1, counter_expanded, fringe_len, depth = search.breadthFirstSearch(problem)
    summary_data.append({'Index':f's{senario_index}:BFS', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path1})
    #DFS
    path2, counter_expanded, fringe_len, depth = search.depthFirstSearch(problem)
    summary_data.append({'Index':f's{senario_index}:DFS', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path2})
    #UCS
    path3, counter_expanded, fringe_len, depth = search.uniformCostSearch(problem)
    summary_data.append({'Index':f's{senario_index}:UCS', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path3})
    #A*
    path4, counter_expanded, fringe_len, depth = search.aStarSearch(problem, search.h3)
    summary_data.append({'Index':f's{senario_index}:A*', 'Expanded': counter_expanded, 'Fringe': fringe_len, 'Depth': depth, 'Path': path4})
    
    print(path1 == path4, path2 == path4, path3 == path4)
    return summary_data


# TASK 2: Test the different heuristics
def task2(senarios):
    result_task2= pd.DataFrame()
    counter = 1
    print('Senarios: ', len(senarios))
    ('--------------TASK2---------------')
    for senario in senarios:
        print('Senario: ', counter)
        summary_data = task2_solve_and_compare(senario, counter)
        result_task2 = result_task2.append(summary_data, ignore_index=True)
        counter += 1
        print(f'Senario: {counter}: Done')

    result_task2.set_index('Index', inplace=True)
    result_task2.to_csv('result_task2.csv', index=True)

#TASK 3: comparasion with different Search Algorithms
def task3(senarios):
    result_task3= pd.DataFrame()
    counter = 1
    print('Senarios: ', len(senarios))
    ('--------------TASK3---------------')
    for senario in senarios:
        print('Senario: ', counter)
        summary_data = task3_solve_and_compare(senario, counter)
        result_task3 = result_task3.append(summary_data, ignore_index=True)
        counter += 1
        print(f'Senario: {counter}: Done')

    result_task3.set_index('Index', inplace=True)
    result_task3.to_csv('result_task3.csv', index=True)


if(path.isfile('senarios_2.csv') == False):
    save_to_csv(generate_senarios(seed=0, n=3, nb_senarios=100), 'senarios_2.csv')
senarios = load_from_csv('senarios_2.csv')

task3(senarios)


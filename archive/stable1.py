# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 17:32:32 2023

@author: alexa
"""

import json
json_file_path = "example-argumentation-framework.json"
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

arguments = json_data['Arguments']
attack_relations = json_data['Attack Relations']

import itertools

def generate_label_combinations(graph):
    # Get the unique nodes from the graph
    nodes = set()
    for edge in graph:
        nodes.add(edge[0])
        nodes.add(edge[1])

    # Define the possible labels for each node
    labels = [True, False, None]

    # Generate all label combinations using itertools.product
    label_combinations = list(itertools.product(labels, repeat=len(nodes)))

    return label_combinations

# Example graph structure

graph = attack_relations
graph = [["0","1"],["1","0"],["2","2"]]
# Generate all label combinations for the nodes in the graph
label_combinations = generate_label_combinations(graph)

# Print the label combinations
for i, combination in enumerate(label_combinations):
    print(f"Combination {i + 1}: {dict(zip(sorted(set(node for edge in graph for node in edge)), combination))}")

test_argument = 0

believed_combinations = []
for combination in label_combinations:
    if combination[test_argument]:
        believed_combinations.append(combination)
print("_"*10,"believed")
for i, combination in enumerate(believed_combinations):
    print(f"Combination {i + 1}: {dict(zip(sorted(set(node for edge in graph for node in edge)), combination))}")
#In rule:
# All attackers are out

In_believed_combinations = []
for idx, combination in enumerate(believed_combinations):
    
    print(f"combi nr {idx }: {combination}")
    all_out = True
    for i, node in enumerate(combination):
        
        if node:
            for relation in graph:
                
                print(f"attaked: {relation[1] },current_node: {str(i)}")
                if relation[1] == str(i):
                   # print("Hi")
                    if combination[int(relation[0])]:
                        all_out = False
                        break
        
    
            # print("broke")
    print(all_out)
    if all_out:
        In_believed_combinations.append(combination)
                    
print("_"*10,"believed_in")
for i, combination in enumerate(In_believed_combinations):
    print(f"Combination {i + 1}: {dict(zip(sorted(set(node for edge in graph for node in edge)), combination))}")

# Out rule:
# There is an attackers that is in 

Out_In_believed_combinations = []
for idx, combination in enumerate(In_believed_combinations):
    print(f"combi nr {idx }: {combination}")
    for i, node in enumerate(combination):
        print(node)
        if node is False:
            One_In = False
            #print(i,"Hi_not_node")
            for relation in graph:
                print(f"attaked: {relation[1] },current_node: {str(i)}")
                if relation[1] == str(i):
                    # print("Hi")
                    if combination[int(relation[0])]:
                        print("True_attaker")
                        One_In = True
                        break

       # print(i)
    if One_In:
        
        Out_In_believed_combinations.append(combination)
                        
            
        
                    
print("_"*10,"believed_in_out")
for i, combination in enumerate(Out_In_believed_combinations):
    print(f"Combination {i + 1}: {dict(zip(sorted(set(node for edge in graph for node in edge)), combination))}")      
#Idea is to start with the argument of interest and then create new nodes, recursively till a dictionary is filled
#not done at at all yet

import json
json_file_path = "example-argumentation-framework.json"
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

arguments = json_data['Arguments']
attack_relations = json_data['Attack Relations']

assignments = []
test_argument = 0

n_arguments = len(arguments)

class Node(argument_nr, label, label_assignment):
    def __init__(self):
        self.argument_nr = argument_nr
        self.label = label
        self.label_assignment = label_assignment
        
        self.check_attack()
    
    def check_attack(self):
        if not None in self.label_assignment.values:
            assignments.append(self.label_assignment)
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

n_arguments = len(arguments)
assignments = {}
for arg_idx in range(n_arguments):
    assignments[str(arg_idx)] = None

test_argument = "0"
latest_assignments = [test_argument]
relation_dict = {}

# for relation in attack_relations:
#     relation_dict[relation[0]] = []
# for relation in attack_relations:
#     relation_dict[relation[0]].append(relation[1])
    
assignments[test_argument] = True

contradiction = False
new_assignments = []

# while len(relation_dict) != 0 and not contradiction:
#     print("while")
#     print("latest:", latest_assignments)
#     for latest_assignment in latest_assignments:
#         if not latest_assignment in relation_dict.values():
#             continue
        
#         if assignments[latest_assignment] == "In":
            
#             for attacked_argument in relation_dict[latest_assignment]:
#                 if assignments[attacked_argument] == "In":
#                     contradiction = True
#                     break
#                 elif assignments[attacked_argument] == "Out":
#                     continue
#                 elif assignments[attacked_argument] == None:
#                     assignments[attacked_argument] = "Out"
#                     new_assignments.append(attacked_argument)
#                 else:
#                     print(assignments[attacked_argument])
#                     raise ValueError("weird assignment")
#                 del relation_dict[latest_assignment]
#             if contradiction:
#                 break
            
#         elif assignments[latest_assignment] == "Out":
            
#             for attacked_argument in relation_dict[latest_assignment]:
#                 if assignments[attacked_argument] == "Out":
#                     contradiction = True
#                     break
#                 elif assignments[attacked_argument] == "In":
#                     continue
#                 elif assignments[attacked_argument] == None:
#                     assignments[attacked_argument] = "In"
#                     new_assignments.append(attacked_argument)
#                 else:
#                     print(assignments[attacked_argument])
#                     raise ValueError("weird assignment")
#                 del relation_dict[latest_assignment]
#             if contradiction:
#                 break
#         else:
#             print(assignments[attacked_argument])
#             raise ValueError("weird assignment")
#     print("assignments",assignments)
#     latest_assignment = new_assignments

# print(contradiction)
# print(assignments)
        
# count = 0
# while not contradiction and len(attack_relations) > 0 :
#     if count == 3:
#         break
#     for relation in attack_relations:
#         print("rel:",relation)
#         print(assignments[relation[0]])
        
#         if not assignments[relation[0]]==None:
#             print(relation[0], "not None")
#             if assignments[relation[1]] == None:
#                 print("new assignment",relation[1], "now:", not assignments[relation[0]])
#                 assignments[relation[1]] = not assignments[relation[0]]
#             else:
#                 print("contra:",assignments[relation[1]] == assignments[relation[0]])
#                 contradiction = assignments[relation[1]] == assignments[relation[0]]
#                 if contradiction:
#                     break
#     True_arguments = [key for key, value in assignments.items() if value == True]
    
#     for relation in attack_relations:
#         for true_argument in True_arguments:
#             if relation[0] == None
            

#     count +=1
#     print(assignments)
contradiction = False
count = 0
while not contradiction:
    if count == 3:
        break
    for relation in attack_relations:
        attaker = relation[0]
        attacked = relation[1]
        #print(attaker)
        if assignments[attaker] != None or assignments[attacked] != None:
            #print(attaker)
            if assignments[attaker] == assignments[attacked]:
                if assignments[attaker] and assignments[attacked]:
                    contradiction = True
                    break
            else: 
                if assignments[attaker] is None and assignments[attacked] != None:
                    assignments[attaker] = not assignments[attacked]
                    print(f"{attaker} is now {not assignments[attacked]}")
                elif assignments[attaker] != None and assignments[attacked] == None:
                    assignments[attacked] = not assignments[attaker]
                    print(f"{attacked} is now {not assignments[attaker]}")
    count += 1
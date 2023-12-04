import json
import sys 
import random

def attack(attack_relations, current_argument, used, arguments):
    arg_key = random.choice([i for i in arguments if arguments[i]==current_argument])
    for attack in attack_relations:
        if attack[1] == arg_key and arguments[attack[0]] not in used:
            new_argument = arguments[attack[0]]
            used.append(new_argument)
            return new_argument, used
    return False, used

def argumentation(json_file_path, start_arg):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    arguments = json_data['Arguments']
    attack_relations = json_data['Attack Relations']

    winner = False
    used = [start_arg]
    new_arg = start_arg
    while winner is False:
        new_arg, used = attack(attack_relations, new_arg, used, arguments)
        if new_arg is False:
            winner = True
            break
        new_arg = input(new_arg + "\n")
        used.append(new_arg)
        print(used)
    



if __name__ == "__main__":
    json_file_path = sys.argv[1]
    starting_argument = sys.argv[2]
    argumentation(json_file_path, starting_argument)
    print("testestduvbbeltest")

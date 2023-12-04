import json
import sys 
import random

def attack(attack_relations, current_argument, used, arguments, used_op):
    arg_key = random.choice([i for i in arguments if arguments[i]==current_argument])

    for attack in attack_relations:

        if attack[1] == arg_key and arguments[attack[0]] not in used:
            new_argument = arguments[attack[0]]
            used.append(new_argument)
            if new_argument in used_op:
                return False, 1
            return new_argument, used
    return False, used

def argumentation(json_file_path, start_arg):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    arguments = json_data['Arguments']
    attack_relations = json_data['Attack Relations']

    winner = False
    used_op = [start_arg]
    used_pro = ['']
    new_arg = start_arg

    while winner is False:
        new_arg, used_pro = attack(attack_relations, new_arg, used_pro, arguments, used_op)
        if new_arg is False and used_pro != 1:
            winner = True
            print('User wins!')
            break
        elif new_arg is False and used_pro == 1:
            winner = True
            print("Opponent contradicted itself!")
            break

        for attacks in attack_relations:
            if arguments[[attacks[0]][0]] == used_pro[-1]:
                arg_key = attacks[0]

        found = False
        for attacks in attack_relations:
            if arg_key == attacks[1]:
                found = True


        if found == False:
            winner = True
            print(used_pro[-1])
            print('User out of options!')
            break

        new_arg = input(new_arg + "\n")

        if new_arg in used_pro:
            winner = True
            print("Proponent contradicted itself")
            break

        while new_arg in used_op:
            print('User is not allowed to use the same argument more than 1 time.')
            new_arg = input(new_arg + "\n")

        used_op.append(new_arg)

    



if __name__ == "__main__":
    json_file_path = sys.argv[1]
    starting_argument = sys.argv[2]
    argumentation(json_file_path, starting_argument)

import json
import sys 
import random
import numpy as np

def attack(attack_relations, current_argument, used, arguments, used_op):
    arg_key = random.choice([i for i in arguments if arguments[i]==current_argument])
    attacker = []
    for attack in attack_relations:
        if attack[1] == arg_key:
            attacker.append(attack[0])

    weak_arg = [0] * len(attacker)

    for attack in range(len(attacker)):
        for relation in attack_relations:
            if attacker[attack] == relation[1]:
                weak_arg[attack] += 1

    if len(attacker) == 0:
        return False, used

    new_argument = attacker[weak_arg.index(min(weak_arg))]
    used.append(new_argument)

    if new_argument in used_op:
            return False, 1

    else:
        return new_argument, used


def check_attackers(attack_relations, arguments, used_pro, attack_counter, new_arg):

    for attacks in attack_relations:

        if arguments[[attacks[0]][0]] == new_arg and arguments[[attacks[1]][0]] in used_pro:
            attack_counter += 1

    return attack_counter

def argumentation(json_file_path, start_arg):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    arguments = json_data['Arguments']
    attack_relations = json_data['Attack Relations']

    winner = False
    used_op = []
    used_pro = [start_arg]
    new_arg = start_arg
    new_arg = input(new_arg + "\n")
    attack_counter = 0
    attack_counter = check_attackers(attack_relations, arguments, used_pro, attack_counter, new_arg)

    while attack_counter == 0:
        print('User need to pick an argument that attacks the proponent')
        new_arg = input(new_arg + "\n")
        attack_counter = check_attackers(attack_relations, arguments, used_pro, attack_counter, new_arg)
    used_op.append(new_arg)

    if new_arg in used_pro:
        print("Opponent contradicted itself!")
        winner = True

    while winner is False:

        #new_arg = input(new_arg + "\n")
        new_arg, used_pro = attack(attack_relations, new_arg, used_pro, arguments, used_op)
        if new_arg is False and used_pro != 1:
            winner = True
            print('User wins!')
            break
        elif new_arg is False and used_pro == 1:
            winner = True
            #print(used_op[-1])
            print("Opponent contradicted itself!")
            break

        for attacks in attack_relations:
            #print(arguments[[attacks[0]][0]])
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
        #used_op.append(new_arg)

        attack_counter = 0
        attack_counter = check_attackers(attack_relations, arguments, used_pro, attack_counter, new_arg)

        while attack_counter == 0:
            print('User need to pick an argument that attacks the proponent')
            new_arg = input(new_arg + "\n")
            attack_counter = check_attackers(attack_relations, arguments, used_pro, attack_counter, new_arg)


        #PROBLEM
        if new_arg in used_pro:
            winner = True
            print("Proponent contradicted itself")
            break

        attack_count = 0
        while new_arg in used_op:
            #PROBLEM
            #print(used_op)
            if [str(new_arg), str(used_pro[-1])] in attack_relations and [str(used_pro[-1]), str(new_arg)] in attack_relations:

                for at in attack_relations:
                    if new_arg == at[0]:
                        attack_count += 1

                if attack_count > 0:
                    print('User is out of options')
                    winner = True
                    break

            print('User is not allowed to use the same argument more than 1 time.')
            new_arg = input(new_arg + "\n")

        used_op.append(new_arg)

    



if __name__ == "__main__":
    json_file_path = sys.argv[1]
    starting_argument = sys.argv[2]
    argumentation(json_file_path, starting_argument)

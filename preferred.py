import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_attack_relations_dict(attack_relations):
    attack_dict = {}
    for attack in attack_relations:
        attacker, attacked = attack
        if attacker not in attack_dict:
            attack_dict[attacker] = []
        attack_dict[attacker].append(attacked)
    return attack_dict

def is_conflict(arguments, labeling, attack_relations, arg1, arg2):
    # Check if arg1 and arg2 are attacking each other
    return arg2 in attack_relations.get(arg1, []) and arg1 in attack_relations.get(arg2, [])

def is_complete_extension(arguments, labeling, attack_relations):
    for arg, label in labeling.items():
        if label == 'in':
            for attacked_arg in attack_relations.get(arg, []):
                if labeling.get(attacked_arg) == 'in':
                    return False
    return True

def count_labels(labeling, label):
    return sum(1 for l in labeling.values() if l == label)

def find_best_labeling(arguments, attack_relations, current_labeling, best_labeling, start_key=0):
    if len(current_labeling) == len(arguments):
        if is_complete_extension(arguments, current_labeling, attack_relations):
            in_count = count_labels(current_labeling, 'in')
            out_count = count_labels(current_labeling, 'out')
            if in_count + out_count > best_labeling['max_count']:
                best_labeling['labeling'] = current_labeling.copy()
                best_labeling['max_count'] = in_count + out_count
        return

    current_arg = start_key
    while current_arg in current_labeling:
        current_arg += 1

    current_labeling[current_arg] = 'in'

    # Check for conflicts and resolve them
    for arg in range(len(arguments)):
        if arg != current_arg and is_conflict(arguments, current_labeling, attack_relations, arg, current_arg):
            current_labeling[arg] = 'undecided'
            find_best_labeling(arguments, attack_relations, current_labeling, best_labeling, start_key=current_arg + 1)
            current_labeling[arg] = 'out'  # Also try labeling the conflicting argument as 'out'
            break

    find_best_labeling(arguments, attack_relations, current_labeling, best_labeling, start_key=current_arg + 1)
    current_labeling[current_arg] = 'out'
    find_best_labeling(arguments, attack_relations, current_labeling, best_labeling, start_key=current_arg + 1)
    current_labeling.pop(current_arg)

def main(file_path):
    data = read_json(file_path)
    arguments = data['Arguments']
    attack_relations = create_attack_relations_dict(data['Attack Relations'])

    best_labeling = {'labeling': None, 'max_count': 0}
    find_best_labeling(arguments, attack_relations, {}, best_labeling)

    print("Best Labeling:", best_labeling['labeling'])

if __name__ == "__main__":
    json_file_path = "example-argumentation-framework.json"
    main(json_file_path)
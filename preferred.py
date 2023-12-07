import json
import copy

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

def is_conflict(labeling, arg, attack_relations):
    # Check if there is an 'in' node attacking an 'in' node
    for attacker in attack_relations.get(arg, []):
        if labeling[attacker] == 'in':
            return True
    return False

def node_labeling(arguments, attack_relations):
    labeling = {}
    for arg in arguments:
        labeling[arg] = 'undecided'

    # Continue until there are no constraint violations
    while True:
        # Create a copy of the current labeling to track changes
        prev_labeling = copy.deepcopy(labeling)

        for arg in arguments:
            if labeling[arg] == 'undecided' and not is_conflict(labeling, arg, attack_relations):
                # If the current node is 'undecided' and has no conflict, label it 'in'
                labeling[arg] = 'in'
            elif labeling[arg] == 'undecided':
                # If there is a conflict, label it 'out'
                labeling[arg] = 'out'

        # Check for constraint conflicts
        for arg, arg_label in labeling.items():
            for attacker in attack_relations.get(arg, []):
                if labeling[arg] == 'in' and labeling[attacker] == 'in':
                    # Constraint conflict, set the label to 'undecided'
                    labeling[arg] = 'undecided'
                elif labeling[arg] == 'out' and labeling[attacker] == 'out':
                    labeling[arg] = 'undecided'
                    break

        # Break the loop if no changes were made to the labeling
        if prev_labeling == labeling:
            break

    return labeling

def main(file_path):
    data = read_json(file_path)
    arguments = list(data['Arguments'].keys())
    attack_relations = create_attack_relations_dict(data['Attack Relations'])

    labeling = node_labeling(arguments, attack_relations)

    print("Labeling:", labeling)

if __name__ == "__main__":
    json_file_path = "example-argumentation-framework.json"
    main(json_file_path)

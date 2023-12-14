import json
import itertools

def parse_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["Arguments"], data["Attack Relations"]

def parse_attacks(attacks):
    """ Parse the attack relations into a more usable form. """
    attack_dict = {}
    for attacker, attacked in attacks:
        if attacked in attack_dict:
            attack_dict[attacked].add(attacker)
        else:
            attack_dict[attacked] = {attacker}
    return attack_dict

def check_acceptance(labeling, attack_dict, argument):
    """ Check if an argument is credulously accepted under a given labeling. """
    argument = str(argument)  # Ensure the argument is in string format for key matching
    if labeling[argument] == 'IN':
        return True
    if labeling[argument] == 'OUT':
        return False
    # Check if there's a labeling where argument can be IN
    for attacker in attack_dict.get(argument, []):
        if labeling[str(attacker)] == 'OUT':
            return True
    return False

def valid_labeling(labeling, attack_dict):
    """ Check if a labeling is valid according to the rules. """
    for arg, label in labeling.items():
        attackers = attack_dict.get(arg, set())
        if label == 'IN' and any(labeling.get(attacker, 'OUT') == 'IN' for attacker in attackers):
            return False
        if label == 'OUT' and all(labeling.get(attacker, 'OUT') != 'IN' for attacker in attackers):
            return False
        if label == 'UNDECIDED' and (all(labeling.get(attacker, 'OUT') == 'OUT' for attacker in attackers) or 
                                     any(labeling.get(attacker, 'OUT') == 'IN' for attacker in attackers)):
            return False
    return True

def compute_extensions(arguments, attacks, semantics):
    """ Compute the extensions based on the semantics. """
    attack_dict = parse_attacks(attacks)
    all_labelings = itertools.product(['IN', 'OUT', 'UNDECIDED'], repeat=len(arguments))
    extensions = []
    for labeling_tuple in all_labelings:
        labeling = dict(zip(arguments.keys(), labeling_tuple))
        if valid_labeling(labeling, attack_dict):
            if semantics == 'stable' and 'UNDECIDED' not in labeling.values():
                extensions.append(labeling)
            elif semantics == 'grounded' and 'UNDECIDED' in labeling.values():
                extensions.append(labeling)
            elif semantics == 'preferred':
                # This is a simplified check for preferred semantics
                # It's not fully accurate but serves as a basic implementation
                extensions.append(labeling)
    
    return extensions

# Main execution
if __name__ == "__main__":
    filename = 'example-argumentation-framework.json'  # Replace with the path to your JSON file
    argument_of_interest = 0  # Replace with your argument of interest

    arguments, attacks = parse_json(filename)
    attacks = [[int(a), int(b)] for a, b in attacks]  # Converting strings to integers

    # Compute extensions for each semantics
    for semantics in ["preferred", "grounded", "stable"]:
        extensions = compute_extensions(arguments, attacks, semantics)
        print(extensions)
        accepted = any(check_acceptance(labeling, parse_attacks(attacks), argument_of_interest) for labeling in extensions)
        
        print(f"Argument {argument_of_interest} is credulously accepted under {semantics} semantics: {accepted}")

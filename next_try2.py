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

def generate_extensions(arguments, attacks):
    """ Compute the extensions based on the semantics. """
    attack_dict = parse_attacks(attacks)
    extensions = itertools.product(['IN', 'OUT', 'UNDECIDED'], repeat=len(arguments))
        
    return extensions, attack_dict

def filter_extensions_with_argument_in():
    pass

def valid_labeling(labeling, attack_dict):
    """ Check if a labeling is valid according to the rules. """
    for arg, label in labeling.items():
        attackers = attack_dict.get(int(arg), set())
        
        #print("attackers:", attackers, "label",label, "arg",arg)
        #my_list = []
        # for attacker in attackers:
        #     attacker = str(attacker)
        #     my_list.append(labeling.get(attacker) == 'IN' or labeling.get(attacker) =="UNDECIDED" )
        # if label == 'IN' and any(my_list):
        #     return False
        if label == 'IN' and any(labeling.get(str(attacker)) == 'IN' or labeling.get(str(attacker)) == "UNDECIDED" for attacker in attackers):
            #print("1")
            return False
        if label == 'OUT' and all(labeling.get(str(attacker)) != 'IN' for attacker in attackers):
            #print("2")
            return False
        # print(attackers)
        # print(not attackers)
        #print([attacker for attacker in attackers])
        # print([labeling.get(str(attacker),"UNDECIDED") for attacker in attackers])
        # print([labeling.get(str(attacker)) == 'IN' for attacker in attackers])
        if label == "UNDECIDED" and not attackers:
            continue
        
        if label == 'UNDECIDED' and (all(labeling.get(str(attacker)) == 'OUT' for attacker in attackers) or 
                                      any(labeling.get(str(attacker)) == 'IN' for attacker in attackers)):
             return False
        
    return True

# Main execution
if __name__ == "__main__":
    filename = 'example-argumentation-framework1.json'  # Replace with the path to your JSON file
    argument_of_interest = 0  # Replace with your argument of interest

    arguments, attacks = parse_json(filename)
    attacks = [[int(a), int(b)] for a, b in attacks]  # Converting strings to integers

    extensions, attack_dict = generate_extensions(arguments, attacks)
    # ext_list = list(extensions)
    # print(len(ext_list))
    # print(ext_list)'
    i = 0
    for labeling_tuple in extensions:
        
        #print("hi")
        labeling = dict(zip(arguments.keys(), labeling_tuple))
        print(labeling)
        print(valid_labeling(labeling, attack_dict))
        # if i ==0:
        #     break

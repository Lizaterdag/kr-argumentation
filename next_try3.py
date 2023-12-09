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

def aoi_is_in(labeling,argument_of_interest): #argument of interest is in
    # print("______")
    # print(labeling)
    # print(argument_of_interest)
    if labeling.get(str(argument_of_interest)) == "IN":
        return True
    return False

def is_stable(labeling):
    return "UNDECIDED" not in labeling.values()

def get_preferred_extensions(dictionaries):
    max_in_value = 0
    max_out_value = 0
    result_in = []
    result_out = []

    for d in dictionaries:
        count_in = sum(1 for value in d.values() if value == 'IN')
        count_out = sum(1 for value in d.values() if value == 'OUT')

        if count_in > max_in_value:
            max_in_value = count_in
            result_in = [d]
        elif count_in == max_in_value:
            result_in.append(d)

        if count_out > max_out_value:
            max_out_value = count_out
            result_out = [d]
        elif count_out == max_out_value:
            result_out.append(d)

    return result_in + result_out

def get_grounded_extensions(dictionaries):
    min_in_value = float('inf')
    min_out_value = float('inf')
    result_min_in = []
    result_min_out = []

    for d in dictionaries:
        if all([str(value) == "UNDECIDED" for value in d.values()]):
            continue
        count_in = sum(1 for value in d.values() if value == 'IN')
        count_out = sum(1 for value in d.values() if value == 'OUT')

        if count_in < min_in_value:
            min_in_value = count_in
            result_min_in = [d]
        elif count_in == min_in_value:
            result_min_in.append(d)

        if count_out < min_out_value:
            min_out_value = count_out
            result_min_out = [d]
        elif count_out == min_out_value:
            result_min_out.append(d)

    return result_min_in + result_min_out

def valid_labeling(labeling, attack_dict):
    """ Check if a labeling is valid according to the rules. """
    for arg, label in labeling.items():
        attackers = attack_dict.get(int(arg), set())
        #in ⇔ all attackers are out
        if label == 'IN' and any(labeling.get(str(attacker)) == 'IN' or labeling.get(str(attacker)) == "UNDECIDED" for attacker in attackers):
            return False
        #out ⇔ there is an attacker that is in
        if label == 'OUT' and all(labeling.get(str(attacker)) != 'IN' for attacker in attackers):
            return False
        #undec ⇔ not all attackers are out, and no attacker is in
        #first empty set handling, no attacker => empty set => okay for undecided labeling
        #but remaining labeling must also be valid, so continue to check next argument
        if label == "UNDECIDED" and not attackers:
            continue
        #empty set would otherwise cause problems in all() 
        if label == 'UNDECIDED' and (all(labeling.get(str(attacker)) == 'OUT' for attacker in attackers) or 
                                      any(labeling.get(str(attacker)) == 'IN' for attacker in attackers)):
             return False 
    return True

# Main execution
if __name__ == "__main__":
    filename = 'example-argumentation-framework.json'  # Replace with the path to your JSON file
    argument_of_interest = 6  # Replace with your argument of interest

    arguments, attacks = parse_json(filename)
    attacks = [[int(a), int(b)] for a, b in attacks]  # Converting strings to integers

    all_extensions, attack_dict = generate_extensions(arguments, attacks)
    # ext_list = list(extensions)
    # print(len(ext_list))
    # print(ext_list)'
    i = 0
    valid_extensions = []
    all_stable_extensions = []#valid extensions of interest
    for labeling_tuple in all_extensions:
        
        #print("hi")
        labeling = dict(zip(arguments.keys(), labeling_tuple))
        # print(labeling)
        # print(filter_extensions_with_argument_in(labeling, argument_of_interest))
        # print(valid_labeling(labeling, attack_dict))
        # if i ==0:
        #     break
        #if aoi_is_in(labeling,argument_of_interest):
        if valid_labeling(labeling, attack_dict):
            
            valid_extensions.append(labeling)
            if is_stable(labeling):
                all_stable_extensions.append(labeling)
    
            
    print(valid_extensions)
    print(all_stable_extensions)

#no check wether aoi is in
all_preferred_extensions = get_preferred_extensions(valid_extensions)
all_grounded_extensions = get_grounded_extensions(valid_extensions)

stable_extensions = []
for extension in all_stable_extensions:
    if aoi_is_in(extension, argument_of_interest):
        stable_extensions.append(extension)

preferred_extensions = []
for extension in all_preferred_extensions:
    if aoi_is_in(extension, argument_of_interest):
        preferred_extensions.append(extension)
        
grounded_extensions = []
for extension in all_grounded_extensions:
    if aoi_is_in(extension, argument_of_interest):
        grounded_extensions.append(extension)

import networkx as nx
import matplotlib.pyplot as plt


def visualize_graph(labels, edges,semantic,filename, argument_of_interest):
    G = nx.DiGraph()

    # Add nodes with labels
    for node, label in labels.items():
        G.add_node(node, label=label)

    # Add edges
    G.add_edges_from([(str(src), str(target)) for src, target in edges])

    # Define positions for the nodes
    pos = nx.spring_layout(G)

    # Map node colors based on labels
    node_colors = {'IN': 'green', 'OUT': 'red', 'UNDECIDED': 'grey'}
    colors = [node_colors[label] for node, label in nx.get_node_attributes(G, 'label').items()]

    # Draw nodes
    node_labels = {node: f"{node}\n{label}" for node, label in labels.items()}
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=colors, alpha=0.8)
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Draw edges with more prominent arrows
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2.0, alpha=0.7, edge_color='blue', connectionstyle="arc3,rad=0.1", arrowsize=20, arrows=True)
    file = filename.split(".")[0]
    # Show the plot
    plt.title(f"{semantic} labeling for argument {argument_of_interest}")
    plt.suptitle(f"{file}", fontsize=8, y=0.87, style='italic', color='grey')

    plt.axis('off')
    plt.show()
    plt.savefig(f"{semantic}_{argument_of_interest}_{file}")
    




if len(stable_extensions) != 0:
    print(f"Argument {argument_of_interest} is credulously accepted under stable semantics: TRUE")
    visualize_graph(stable_extensions[0], attacks,"stable", filename,argument_of_interest)
else:
    print(f"Argument {argument_of_interest} is credulously accepted under stable semantics: FALSE")

if len(preferred_extensions) != 0:
    print(f"Argument {argument_of_interest} is credulously accepted under preferred semantics: TRUE")
    visualize_graph(preferred_extensions[0], attacks,"preferred",filename,argument_of_interest)
else:
    print(f"Argument {argument_of_interest} is credulously accepted under preferred semantics: FALSE")
    
if len(grounded_extensions) != 0:
    print(f"Argument {argument_of_interest} is credulously accepted under grounded semantics: TRUE")
    visualize_graph(grounded_extensions[0], attacks,"grounded", filename,argument_of_interest)
else:
    print(f"Argument {argument_of_interest} is credulously accepted under grounded semantics: FALSE")
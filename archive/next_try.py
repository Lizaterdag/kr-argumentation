import json
import itertools
import sys
import networkx as nx
import matplotlib.pyplot as plt

def parse_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["Arguments"], data["Attack Relations"]

def parse_attacks(attacks):
    attack_dict = {}
    for attacker, attacked in attacks:
        attack_dict.setdefault(attacked, set()).add(attacker)
    return attack_dict

def generate_extensions(arguments, attacks):
    attack_dict = parse_attacks(attacks)
    extensions = itertools.product(['IN', 'OUT', 'UNDECIDED'], repeat=len(arguments))
    return extensions, attack_dict

def aoi_is_in(labeling, argument_of_interest):
    return labeling.get(str(argument_of_interest)) == "IN"

def is_stable(labeling):
    return "UNDECIDED" not in labeling.values()

def get_extensions_count(dictionaries, label_type):
    max_value = 0
    result = []

    for d in dictionaries:
        count = sum(1 for value in dict(zip(arguments.keys(), d)).values() if value == label_type)

        if count > max_value:
            max_value, result = count, [d]
        elif count == max_value:
            result.append(d)

    return result


def valid_labeling(labeling, attack_dict):
    for arg, label in labeling.items():
        attackers = attack_dict.get(int(arg), set())

        if label == 'IN' and any(labeling.get(str(attacker)) in ('IN', 'UNDECIDED') for attacker in attackers):
            return False
        if label == 'OUT' and all(labeling.get(str(attacker)) != 'IN' for attacker in attackers):
            return False
        if label == "UNDECIDED" and not attackers:
            continue
        if label == 'UNDECIDED' and (all(labeling.get(str(attacker)) == 'OUT' for attacker in attackers) or 
                                      any(labeling.get(str(attacker)) == 'IN' for attacker in attackers)):
            return False 
    return True

def visualize_graph(labels, edges, semantic, filename, argument_of_interest):
    G = nx.DiGraph()

    for node, label in labels.items():
        G.add_node(node, label=label)

    G.add_edges_from([(str(src), str(target)) for src, target in edges])

    pos = nx.spring_layout(G)
    node_colors = {'IN': 'green', 'OUT': 'red', 'UNDECIDED': 'grey'}
    colors = [node_colors[label] for node, label in nx.get_node_attributes(G, 'label').items()]

    node_labels = {node: f"{node}\n{label}" for node, label in labels.items()}
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=colors, alpha=0.8)
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2.0, alpha=0.7, edge_color='blue', connectionstyle="arc3,rad=0.1", arrowsize=20, arrows=True)

    file = filename.split(".")[0]
    plt.title(f"{semantic} labeling for argument {argument_of_interest}")
    plt.suptitle(f"{file}", fontsize=8, y=0.87, style='italic', color='grey')

    plt.axis('off')
    plt.savefig(f"{semantic}_{argument_of_interest}_{file}")
    plt.show()

# Main execution
if __name__ == "__main__":
    filename = sys.argv[1]
    argument_of_interest = sys.argv[2]
    
    arguments, attacks = parse_json(filename)
    attacks = [[int(a), int(b)] for a, b in attacks]

    all_extensions, attack_dict = generate_extensions(arguments, attacks)

    valid_extensions = [labeling for labeling in all_extensions if valid_labeling(dict(zip(arguments.keys(), labeling)), attack_dict)]
    all_stable_extensions = [labeling for labeling in valid_extensions if is_stable(dict(zip(arguments.keys(), labeling)))]

    all_preferred_extensions = get_extensions_count(valid_extensions, 'IN') + get_extensions_count(valid_extensions, 'OUT')
    all_grounded_extensions = get_extensions_count(valid_extensions, 'IN') + get_extensions_count(valid_extensions, 'OUT')

    stable_extensions = [extension for extension in all_stable_extensions if aoi_is_in(extension, argument_of_interest)]
    preferred_extensions = [extension for extension in all_preferred_extensions if aoi_is_in(extension, argument_of_interest)]
    grounded_extensions = [extension for extension in all_grounded_extensions if aoi_is_in(extension, argument_of_interest)]

    credulously_accepted = lambda ext, sem: f"Argument {argument_of_interest} is credulously accepted under {sem} semantics: {bool(ext)}"
    
    print(credulously_accepted(stable_extensions, "stable"))
    visualize_graph(stable_extensions[0], attacks, "stable", filename, argument_of_interest) if stable_extensions else None
    
    print(credulously_accepted(preferred_extensions, "preferred"))
    visualize_graph(preferred_extensions[0], attacks, "preferred", filename, argument_of_interest) if preferred_extensions else None
    
    print(credulously_accepted(grounded_extensions, "grounded"))
    visualize_graph(grounded_extensions[0], attacks, "grounded", filename, argument_of_interest)

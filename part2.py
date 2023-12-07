import json

with open('example-argumentation-framework.json') as f:
   data = json.load(f)

attack = data['Attack Relations']

print(attack)

d = {}
for elem in attack:
    try:
        d[elem[1]].append(elem[0])
    except KeyError:
        d[elem[1]] = [elem[0]]
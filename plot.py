import json
import sys
import matplotlib.pyplot as plt


file = 'data.json'  # sys.argv[1]

with open(file, 'r') as fh:
    content = fh.readlines()

file_in = json.loads(content[0])

data = {'field1': [], 'field2': []}
for entry in file_in['feeds']:
    for key, values in entry.iteritems():
        if key in data:
            data[key].append(float(values))


for values in data.values():
    plt.plot(values)
plt.show()

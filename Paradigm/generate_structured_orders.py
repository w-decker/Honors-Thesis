# import numpy and csv
import numpy as np
import csv

# list of words
words = [['pi', 'tu', 'bi'], ['ba', 'du', 'pi'], ['du', 'ti', 'pa'], 
         ['bi', 'du', 'ti'], ['tu', 'di', 'ba'], ['bu', 'ti', 'pa']]

# create TPM
strucTPM = np.full((6, 6), fill_value=(1/5))
np.fill_diagonal(strucTPM, 0)
print(strucTPM)

# create orders
numstim = 144
initstate = np.random.choice(range(6))  # Random initial state
order = [words[initstate]]
current_state = initstate

while len(order) < numstim:
    next_state = np.random.choice(range(6), p=strucTPM[current_state])
    if words[next_state] != order[-1]:
        order.append(words[next_state])
        current_state = next_state

# print orders and un-embed word list
order1 = list(np.concatenate(order))
order2 = list(np.concatenate(order[::-1])) # order 2 = order 1 in reverse
print(order1)
print(order2)

# ouptut orders to .csv
filename = "structured_orders.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Order 1", "Order 2"])
    writer.writerows(zip(order1, order2))
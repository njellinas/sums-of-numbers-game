import pickle
from random import shuffle

sums = [(5, 105) , (205, 305), (405, 1005), (1105, 1205), (1305, 1405)]

NUM_CHILDREN = 5

for i in range(1, NUM_CHILDREN + 1):
    shuffle(sums)
    a = {'sums': sums, 'current_sum': 0}
    with open('child_data/child{}.pkl'.format(str(i)), 'wb') as f:
        pickle.dump(obj=a, file=f)
    print(a)

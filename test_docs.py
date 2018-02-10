from functools import reduce
from collections import Counter

all_keys = reduce(lambda x,y:x+y, [list(h.keys()) for h in holders])

c = Counter(all_keys)

print(c)
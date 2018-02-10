# Counter({'Attachment 1': 474,
#          'Attachment 2': 84,
#          'Attachment 3': 23,
#          'Attachment 4': 13,
#          'Attachment 5': 4,
#          'Categories : ': 8030,
#          'Cause': 5277,
#          'Details': 5008,
#          'Document': 16806,
#          'Document Id': 16806,
#          'Impact / Risks': 602,
#          'Keywords': 1685,
#          'Language : ': 16806,
#          'Permalink to: ': 16805,
#          'Product': 14961,
#          'Product Version': 15110,
#          'Purpose': 4674,
#          'Related Information': 7575,
#          'Request a Product Feature': 16806,
#          'Resolution': 11775,
#          'Solution': 5029,
#          'Symptoms': 9523,
#          'This Article Replaces': 118,
#          'Title': 16806,
#          'Total Views': 16806,
#          'Update History': 2901,
#          'Updated : ': 16806,
#          'Workaround': 104})

from functools import reduce
from collections import Counter

all_keys = reduce(lambda x,y:x+y, [list(h.keys()) for h in holders])

c = Counter(all_keys)

print(c)
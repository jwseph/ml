from micrograd.engine import Value
from micrograd.nn import Neuron, Layer, MLP

from collections import Counter

with open('names.txt') as f:
    names = f.read().splitlines()
names = ['.'+name+'.' for name in names]

chars = sorted(set(''.join(names)))
itos = chars
stoi = {c: i for i, c in enumerate(chars)}

print(chars)

# b = Counter()
# for name in names:
#     for l, r in zip(name, name[1:]):
#         b[l, r] += 1
# for c in chars:
#     tot = sum(b[c, d] for d in chars)
#     for d in chars:
#         if (c, d) in b:
#             b[c, d] /= 1.0*tot
# for c in chars:
#     for p, d in zip(chars, chars[1:]):
#         b[c, d] += b[c, p]
# print(b[chars[100//27], chars[100%27]])


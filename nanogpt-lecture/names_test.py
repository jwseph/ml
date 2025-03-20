from micrograd.engine import Value
from micrograd.nn import Neuron, Layer, MLP

from collections import Counter
import random

with open('names.txt') as f:
    names = f.read().splitlines()
names = ['.'+name+'.' for name in names]

chars = sorted(set(''.join(names)))
itos = chars
stoi = {c: i for i, c in enumerate(chars)}

print(chars)

b = Counter()
for name in names:
    for l, r in zip(name, name[1:]):
        b[l, r] += 1
for c in chars:
    tot = sum(b[c, d] for d in chars)
    for d in chars:
        if (c, d) in b:
            b[c, d] /= 1.0*tot
for c in chars:
    for p, d in zip(chars, chars[1:]):
        b[c, d] += b[c, p]
print(b[chars[100//27], chars[100%27]])

n = len(chars)
s = '.'
for _ in range(1000):
    rand = random.random()
    for d in chars:
        if rand < b[s[-1], d]:
            s += d
            break
print(s)

test = [14, 5,0, 0, 19, 20, 20, 0, 15, 14, 15, 0, 8, 6, 21]
for l, r in zip(test, test[1:]):
    print(b[chars[l], chars[r]])

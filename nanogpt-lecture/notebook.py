with open('input.txt') as f:
    text = f.read()

chars = sorted(list(set(text)))
vocab_size = len(chars)
# print(chars)
# print(len(chars))

stoi = {c: i for i, c in enumerate(chars)}
itos = chars.copy()
# print(stoi)
# print(itos)
def encode(s): return [stoi[c] for c in s]
def decode(l): return ''.join(itos[x] for x in l)
# print(encode('hello'))
# print(decode(encode('hello')))

import torch
data = torch.tensor(encode(text), dtype=torch.long)
# print(data.shape, data.dtype)
# print(data[:1000])

n = int(0.9*len(data))
train_data = data[:n]
val_data = data[n:]
# print(len(val_data))

# block_size = 8
# print(train_data[:block_size+1])

# x = train_data[:block_size+1]
# for i in range(block_size):
#     print(f'When the input is {x[:i+1]} the target is {x[i+1]}')

torch.manual_seed(1337)
batch_size = 4
block_size = 8

def get_batch(split):
    data = train_data if split == 'train' else val_data
    idx = torch.randint(len(data)-block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in idx])
    y = torch.stack([data[i+1:i+block_size+1] for i in idx])
    return x, y

xb, yb = get_batch('train')
print('inputs:')
print(xb.shape)
print(xb)
print('outputs:')
print(yb.shape)
print(yb)
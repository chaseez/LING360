"""_________________________________________________

DONE CREATING A BIGRAM LANGUAGE MODEL

TRANSFORMER ARCHITECTURE

https://arxiv.org/pdf/1706.03762.pdf

We'll be using GPT (Generative Pre-trained Transformer)

This is different from the transformer architecture in the paper, but it is very similar.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import mmap
import random
import pickle

block_size = 64
batch_size = 128
max_iters = 200
learning_rate = 3e-4
eval_iters = 100
eval_interval = 500
n_embd = 384
n_layer = 8
n_head = 8
dropout = 0.2 # Drops out 20% of neurons from the net to prevent over-fitting

device = torch.device('cuda')
# ./drive/MyDrive/LING 360 Final Project/Cleaned Data/char_set.txt
with open('char_set.txt', 'r', encoding='utf-8') as file:
  text = file.read()

chars = sorted(set(text))
vocab_size= len(chars)

# Encoding and decoding the text
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }

encode = lambda s: [stoi[c] for c in s] # s for string
decode = lambda l: ''.join([itos[i] for i in l]) # l for list

def get_random_chunk(split):
    # ./drive/MyDrive/LING 360 Final Project/Cleaned Data/train.txt
    # ./drive/MyDrive/LING 360 Final Project/Cleaned Data/val.txt
  filename = 'train.txt' if split == 'train' else \
              'val.txt'
  with open(filename, 'rb') as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
      # Determine the file size and a random position to start reading
      file_size= len(mm)
      start_pos = random.randint(0, (file_size) - block_size*batch_size)

      # Seek to the random position and read the block of text
      mm.seek(start_pos)
      block = mm.read(block_size*batch_size-1)

      # Decode the block to a string, ignoring any invalid byte sequences
      decoded_block = block.decode('utf-8', errors='ignore').replace('\r','')

      # Train and test splits
      data = torch.tensor(encode(decoded_block), dtype=torch.long)
  return data

def get_batch(split):
  data = get_random_chunk(split)
  ix = torch.randint(len(data) - block_size, (batch_size,))
  x = torch.stack([data[i:i+block_size] for i in ix])
  y = torch.stack([data[i+1:i+block_size+1] for i in ix])
  x,y = x.to(device), y.to(device)
  return x,y

x,y = get_batch('train')

class Head(nn.Module):
  def __init__(self, head_size):
    super().__init__()
    self.key = nn.Linear(n_embd, head_size, bias=False)
    self.query = nn.Linear(n_embd, head_size, bias=False)
    self.value = nn.Linear(n_embd, head_size, bias=False)
    # Helps save on computation time and complexity instead of initializing each
    # instance of the class. Think of a static method for the classes
    self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

    self.dropout = nn.Dropout(dropout)

  def forward(self, x):
    # input of size (batch, time-step, channels)
    # output of size (batch, time-step, head size)
    B,T,C = x.shape
    k = self.key(x) # (B,T,hs)
    q = self.query(x) # (B,T,hs)
    # compute attention scores ("affinities")

    # q = (B, T, hs) @ k.transpose(-2,-1) = (B, hs, T) -> (B, T, T)
    wei = q @ k.transpose(-2,-1) * (k.shape[-1]**-0.5) # this last bit is 1/sqrt(len(keys))
    # k.transpose(-2,-1) swaps the 2nd to last           # And is used to scale the individual
    # row with the last row                              # head with respect to the whole context


    wei = wei.masked_fill(self.tril[:T,:T] == 0, float('-inf')) # (B, T, T)
    wei = F.softmax(wei, dim=-1) # (B,T,T)
    wei = self.dropout(wei)
    # perform the weighted aggregation of the values
    v = self.value(x) # (B,T,hs)
    out = wei @ v # (B, T, T) @ (B, T, hs) -> (B, T, hs)
    return out

class MultiHeadAttention(nn.Module):
  """ Multiple heads of self-attention in parallel """

  def __init__(self, num_heads, head_size):
    super().__init__()
    self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
    self.proj = nn.Linear(head_size * num_heads, n_embd)
    self.dropout = nn.Dropout(dropout)

  def forward(self,x):
    # Take the output and concatenate it to the last dimension of the matrix (B,T)
    # (B,T,F) -> (B,T, [h1,h1,h1,h1,h2,h2,h2,h2,h3,h3,h3,h3])
    # Each h# is a feature of that head
    out = torch.cat([h(x) for h in self.heads], dim=-1)
    out = self.dropout(self.proj(out))
    return out

class FeedForward(nn.Module):
  """ A simple linear layer followed by a non-linearity """

  def __init__(self, n_embd):
    super().__init__()
    self.net = nn.Sequential(
        nn.Linear(n_embd, 4 * n_embd),
        nn.ReLU(),
        nn.Linear(4*n_embd, n_embd),

        # This will allow (dropout * 100) % of nodes to be forgotten to prevent over fitting
        nn.Dropout(dropout)
    )

  def forward(self, x):
    return self.net(x)

class Block(nn.Module):
  """ Transformer block: communication followed by computation """

  def __init__(self, n_embd, n_head):
    super().__init__()
    head_size = n_embd // n_head
    self.sa = MultiHeadAttention(n_head, head_size)
    self.ffwd = FeedForward(n_embd)
    self.ln1 = nn.LayerNorm(n_embd)
    self.ln2 = nn.LayerNorm(n_embd)

  def forward(self, x):
    y = self.sa(x)
    x = self.ln1(x + y)
    y = self.ffwd(x)
    x = self.ln2(x + y)
    return x


class GPTLanguageModel(nn.Module):
  def __init__(self, vocab_size):
    super().__init__()

    # Initialize a probability look up table, think SMT, where the model
    # will store the probability that one letter will follow another
    # (this only applies to bigrams)
    self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
    self.position_embedding_table = nn.Embedding(block_size, n_embd)
    # nn.Sequential neccessitates that each object goes to completion before moving on to the next item
    self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
    self.ln_f = nn.LayerNorm(n_embd)
    self.lm_head = nn.Linear(n_embd, vocab_size)

    self.apply(self._init_weights)

  def _init_weights(self, module):
    """
    Helps perform initializations on the weights, which allows for better
    training and increased performances for starting training of the model
    """
    if isinstance(module, nn.Linear):
      torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
      if module.bias is not None:
        torch.nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
      torch.nn.init.normal_(module.weight, mean=0.0, std=0.2)

  """
  This function is SUPER important! This is really good for debugging,
  better understanding your code, allows you to optimize and find better
  functions to use, and is best practice to write your own
  """
  def forward(self, index, targets=None):
    # Normalized percentages for the bigram at that specific index
    B, T = index.shape

    # B: Batch
    # T: Time Dimension
    # C: Channels (vocab size)

    # index and targets are both (B,T) tensor of integers
    tok_emb = self.token_embedding_table(index) # (B,T,C)
    pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
    x = tok_emb + pos_emb # (B,T,C)
    x = self.blocks(x) # (B,T,C)
    x = self.ln_f(x) # (B,T,C)
    logits = self.lm_head(x) # (B,T,vocab_size)

    if targets is None:
      loss = None
    else:
      B,T,C = logits.shape
      logits = logits.view(B*T, C)
      targets = targets.view(B*T)
      loss = F.cross_entropy(logits, targets)

    return logits, loss

  def generate(self, index, max_new_tokens):
    # index is (B,T) array of indices in the current context
    for _ in range(max_new_tokens):
      # get the prediction
      logits, loss = self.forward(index)
      # focus only on the last time step
      logits = logits[:,-1,:] # becomes (B,C)
      # apply softmax to get probabilities
      probs = F.softmax(logits, dim=-1) # (B,C)
      # sample from the distribution
      index_next = torch.multinomial(probs, num_samples=1) # (B,1)
      # append sampled index to the running sequence
      index = torch.cat((index,index_next), dim=-1) # (B,T+1)
    return index

@torch.no_grad()
def estimate_loss():
  out = {}
  model.eval()
  for split in ['train', 'eval']:
    losses = torch.zeros(eval_iters)
    for k in range(eval_iters):
      X,Y = get_batch(split)
      logits,loss = model(X,Y)
      losses[k] = loss.item()
    out[split] = losses.mean()
  model.train()
  return out

model = GPTLanguageModel(vocab_size)
print('loading model parameters...')
# ./drive/MyDrive/LING 360 Final Project/Models/model-01.pkl
with open('model-01.pkl', 'rb') as f:
  model = pickle.load(f)
print('model loaded')
m = model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
# Typical training loop for models
for iter in range(max_iters):

  if iter % eval_iters == 0:
    losses = estimate_loss()
    print(f'step: {iter}, train loss: {losses["train"]:.3f} eval loss: {losses["eval"]:.3f}')
  # Sample a batch of data
  xb, yb = get_batch('train')
  # print(iter)
  logits, loss = model.forward(xb, yb)
  # Make sure that the gradients don't add up over time
  # Trying to optimize current gradient
  optimizer.zero_grad(set_to_none=True)
  # set_to_none occupies a lot less space compared to int_64 of 0's
  loss.backward()
  optimizer.step()

print(loss.item())
# ./drive/MyDrive/LING 360 Final Project/Models/model-01.pkl
with open('model-01.pkl', 'wb') as f:
  pickle.dump(model, f)
print('model saved')
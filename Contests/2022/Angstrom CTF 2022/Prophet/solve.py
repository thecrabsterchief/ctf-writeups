from z3 import *

rngLen = 607
Tap = 273
class RNG:
  def __init__(self, VEC: list) -> None:
    assert len(VEC) == rngLen
    self.vec = VEC.copy()
    self.tap  = 0
    self.feed = rngLen - Tap
  
  def next(self):
    self.tap -= 1
    if self.tap < 0: self.tap = rngLen - 1

    self.feed -= 1
    if self.feed < 0: self.feed = rngLen - 1

    self.vec[self.feed] = (self.vec[self.feed] + self.vec[self.tap]) % (2**64)
    return self.vec[self.feed]
  
  def ignore(self):
    self.tap -= 1
    if self.tap < 0: self.tap = rngLen - 1

    self.feed -= 1
    if self.feed < 0: self.feed = rngLen - 1


s = Solver()
vec = [BitVec(f"vec_{i}", 64) for i in range(rngLen)]
rng = RNG(vec)

for _ in range(100000):
  rng.ignore()

xored_rng = [rng.next() for _ in range(4)]
xored_flag = [
  4301770859063564088,
  3588343789060400015,
  16743982520636489794,
  14486217089676259227,
]

with open("./chall.txt") as f:
  for _ in range(4): f.readline()
  leaks = [int(f.readline()) for _ in range(607)]
  gap = 0
  for i in range(607):
    s.add(rng.next() == leaks[i])
    
    for j in range(gap):
      rng.next()
    gap = (gap + 1) % 13
  
  if s.check() == sat:
    ans = s.model()
    vec = [ans[v].as_long() if ans[v] is not None else -1 for v in vec]

    # print(xored_rng)
    xored_rng = [
      (vec[488] + vec[154]) % 2**64,
      (vec[487] + vec[153]) % 2**64,
      (vec[486] + vec[152]) % 2**64,
      (vec[485] + vec[151]) % 2**64,
    ]
    flag = [
      int.to_bytes(x ^ y, 8, "little") for x, y in zip(xored_rng, xored_flag)
    ]
    print(b"".join(flag))
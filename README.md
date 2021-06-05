# pbar-pool

A straightforward, dependency free way to update multiple progress bars with python's multiprocessing library. 

Specifically designed to work with multiprocessing.Pool - for which I found all other available solutions to be either overcomplicated, or completely broken.

## Installation:
```bash
pip install pbar-pool
```

## Usage:

```python
from multiprocessing import Pool, cpu_count
from pbar_pool import PbarPool, Pbar
import time, random


def fn(x):
    for _ in Pbar(x, manager=pbars, name=f'Process {pbars.id()}', color=(255, 0, 0)):
        time.sleep(random.randint(0, 3))


to_process = [list(range(10)) for _ in range(100)]
pbars = PbarPool(width=100)

with Pool(processes=cpu_count(), initializer=pbars.initializer()) as p:
    global_pbar = Pbar(p.imap_unordered(fn, to_process), manager=pbars, name='global', total=len(to_process))
    for _ in global_pbar:
        pass
```
--> 
```
global: 56/100 ████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 56% 3.9156s/it 02:52 remaining
 Process 4: 5/10 ██████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 50% 1.4075s/it 00:07 remaining
 Process 2: 2/10 ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 20% 1.5064s/it 00:12 remaining
 Process 3: 0/10 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0% 
 Process 1: 1/10 ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10% 0.0003s/it 00:00 remaining
```

it's as simple as adding the `initializer=pbars.initializer()` option to your Pool object to give each Pool process access to the global progress bars pool.

Then, in each process, wrap your iterator in a `Pbar()` object, passing in the global PbarPool object as the `manager` argument. 

You can also add a global progress bar to track the progress of the outer function, as seen in the example above.

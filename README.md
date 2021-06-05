# pbar-pool

A straightforward, dependency free way to update multiple progress bars with python's multiprocessing library. 

Specifically designed to work with multiprocessing.Pool - for which I found all other available solutions to be either overcomplicated, or completely broken.

below is a minimal example:

```python
from multiprocessing import Pool, cpu_count
from pbar_pool import PbarPool
import time, random


def fn(x):
    pbars.init(total=len(x), name=f"My Process {pbars.id()}")
    for i, y in enumerate(x):
        pbars.update(i)
        time.sleep(random.random())
    pbars.close()


to_process = [list(range(5)) for _ in range(100)]
pbars = PbarPool()

with Pool(processes=cpu_count(), initializer=pbars.initializer()) as p:
    pbars.init(name='global', total=len(to_process))
    for i, _ in enumerate(p.imap_unordered(fn, to_process)):
        pbars.update(i)

```

it's as simple as adding the `initializer=pbars.initializer()` option to your Pool object, to give each Pool process access to the global progress bars pool.

Then, in each process call `pbars.init()` (optionally passing in a `total` or `name`) to initialize a progress bar, and at each update step call `pbar.update(iteration_no)` to update the progress. Once done, call pbars.close().

You can also add a global progress bar to track the progress of the outer function, as seen in the example above.

TODO:
    - [] add ability to wrap iterators like tqdm
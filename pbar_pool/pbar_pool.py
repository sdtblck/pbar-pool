import multiprocessing
import os
import time
import datetime
from typing import Tuple


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def _id():
    if multiprocessing.current_process()._identity:
        return multiprocessing.current_process()._identity[0] - 1
    else:
        return 0


class Pbar:

    def __init__(self, iterable, manager, name: str = "", total: int = None,
                 color: Tuple[int, int, int] = (0, 255, 125)):
        if not name:
            name = str(self.id())
        if color:
            assert isinstance(color, tuple)
            assert len(color) == 3
        self.iterable = iterable
        if total is None:
            if hasattr(self.iterable, '__len__'):
                total = len(self.iterable)
        self.data = {"name": name, "total": total, "iters": 0, "start_time": time.time(), "total_time": 0,
                     "color": color}
        assert isinstance(manager, PbarPool)
        self.manager = manager
        self.manager.pbars[self.id()] = self.data

    def id(self):
        return _id()

    def __iter__(self):
        for i, e in enumerate(self.iterable):
            yield e
            self.manager.update(i)
        else:
            self.manager.close()


class PbarPool:

    def __init__(self, width=None, color=(0, 255, 125)):
        manager = multiprocessing.Manager()
        self.pbars = manager.dict()
        self.width = width
        self.color = color

    def init(self, name: str = "", total: int = None, color: Tuple[int, int, int] = None):
        if not name:
            name = str(self.id())
        if color:
            assert isinstance(color, tuple)
            assert len(color) == 3
        self.pbars[self.id()] = {"name": name, "total": total, "iters": 0, "start_time": time.time(),
                                 "total_time": 0, "color": color or self.color}

    def close(self):
        del self.pbars[self.id()]

    def update(self, i):
        assert isinstance(i, int)
        assert self.pbars.get(self.id()) is not None
        i = i + 1
        d = self.pbars.get(self.id())
        d['iters'] = i
        d['total_time'] = time.time() - d['start_time']
        self.pbars[self.id()] = d
        self.print()

    def bar(self, i, total):
        width = self.width
        if width is None:
            _, width = os.get_terminal_size(0)
        pct = i / total
        _pct = int(pct * width)
        pct = int(pct * 100)
        string = ""
        for _ in range(_pct):
            string += "█"
        for _ in range(width - _pct):
            string += "░"
        string += f" {pct}% "
        return string

    def id(self):
        return _id()

    def print(self):
        os.system('clear')
        string = ""
        for k, v in self.pbars.items():
            _string = ""
            iters = v['iters']
            total = v['total']
            total_time = v["total_time"]
            if total is not None:
                remaining = total - iters
            else:
                remaining = None
            it_per_s = total_time / iters if iters > 0 else None
            _string += f"{v['name']}: {iters}"
            if total is not None:
                _string += f"/{total} "
                _string += self.bar(iters, total)
            else:
                _string += f"/? "
            if it_per_s is not None:
                _string += f'{it_per_s:.4f}s/it '
                if remaining is not None:
                    remaining_str = str(datetime.timedelta(seconds=int(remaining * it_per_s)))
                    if remaining_str.startswith("0:"):
                        remaining_str = remaining_str[2:]
                    _string += f'{remaining_str} remaining'
            _string += "\n"
            string += colored(*v['color'], _string)
        print(f"\r{colored(*self.color, string)}", end='')

    def initializer(self):
        global pbars
        pbars = self

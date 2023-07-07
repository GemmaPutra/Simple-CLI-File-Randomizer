import pathlib
import random
import string
import time
from enum import Enum, auto
from typing import Self, Iterable


class ChaosMethod(Enum):
    Scramble = auto()
    Random = auto()

class FileIsNotFolder(Exception):
    ...

def rename_file(_file: str, _new_name: str, /) -> str:
    if not isinstance(_file, str):
        raise ValueError("wrong value type, expected 'str'")
    file_path = pathlib.Path(_file)
    if not file_path.is_file():
        raise ValueError("wrong value, expected 'file'")
    suff = file_path.suffix
    return file_path.with_name(_new_name).with_suffix(suff).name


def scramble_name(_name: str, /, randomize_for: int = 25) -> str:
    if randomize_for < 25:
        randomize_for = 25

    random_loop = random.randint(randomize_for // 2, randomize_for)
    name_list = list(_name)
    name_len = len(name_list)

    for n in range(random_loop + 1):
        rand_idx1 = random.randint(0, name_len - 1)
        rand_idx2 = random.randint(0, name_len - 1)

        while rand_idx2 == rand_idx1:
            rand_idx2 = random.randint(0, name_len - 1)

        if random.randint(0, 1):
            rand_idx1 = (rand_idx1 + n) % name_len

            if random.randint(0, 1):
                rand_idx2 = (rand_idx2 + n) % name_len

        if random.randint(0, 100) <= random.randint(
            randomize_for, randomize_for + randomize_for // random.randint(1, 5)
        ):
            name_list[rand_idx1], name_list[rand_idx2] = (
                name_list[rand_idx2],
                name_list[rand_idx1],
            )
        else:
            name_list[rand_idx1], name_list[rand_idx2] = (
                _name[rand_idx2],
                _name[rand_idx1],
            )

    return "".join(name_list)


def randomize_name(_length: int, /) -> str:
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(_length)]
    )


class RandomizeIterFile:
    def __init__(
        self, _path: str | bytes | pathlib.Path, _set_random_len: int = 5
    ) -> Self:
        if isinstance(_path, str) or isinstance(_path, bytes):
            _path = pathlib.Path(_path)
        else:
            raise ValueError("wrong value type, expected 'Path'")
        self.path = _path.absolute()
        self.randomize_len = _set_random_len

        if not self.path.exists():
            raise FileNotFoundError("file does not exist")
        if not self.path.is_dir():
            raise FileIsNotFolder("file must be a folder type")

    def __str__(self) -> str:
        return f"{tuple([f_.name for f_ in iter(self)])}"

    def __repr__(self) -> str:
        return f"RandomizeIterFile({tuple(iter(dir))})"

    def __len__(self) -> int:
        return len(iter(self))

    def __iter__(self) -> Iterable[pathlib.Path]:
        return iter([f_.absolute() for f_ in self.path.iterdir() if f_.is_file()])

    def is_valid(self) -> bool:
        result = True
        if not self.path.exists():
            result = False
        if not self.path.is_dir():
            result = False
        return result

    def chaos_naming(
        self, method: ChaosMethod = ChaosMethod.Random
    ) -> tuple[pathlib.Path, ...]:
        """return 'n' of unnamed file"""
        unnamed_file = []

        for file_ in self:
            set_end = time.time() + 30
            try:
                while True:
                    # in this will implement time counting, to prevent naming something too long
                    match method:
                        case ChaosMethod.Scramble:
                            new_file = file_.with_name(
                                f"{scramble_name(file_.with_suffix('').name)}"
                            ).with_suffix(file_.suffix)
                        case ChaosMethod.Random:
                            new_file = file_.with_name(
                                f"{randomize_name(self.randomize_len)}"
                            ).with_suffix(file_.suffix)
                    if (
                        new_file in self.path.iterdir()
                    ):  # preventing same name occurence
                        if time.time() >= set_end: # preventing choosing the name too long for short amount of time
                            file_.rename(new_file)
                            break
                        continue
                    else:
                        file_.rename(new_file)
                        break
            except:
                unnamed_file.append(file_)

        return tuple(unnamed_file)


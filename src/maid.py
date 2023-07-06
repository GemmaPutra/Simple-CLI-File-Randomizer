from dataclasses import dataclass
from typing import Literal, Any

@dataclass(frozen=True)
class BGColor:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def printwarning(*values: object, sep: str | None = " ", end: str | None = "\n", file: Any | None = None, flush: Literal[False] = False) -> None:
    values = list(values)
    values.insert(0, f"{BGColor.WARNING}Warning:{BGColor.ENDC} ")
    print(*values, sep=sep, end=end, file=file, flush=flush)

def printerror(*values: object, sep: str | None = " ", end: str | None = "\n", file: Any | None = None, flush: Literal[False] = False) -> None:
    values = list(values)
    values.insert(0, f"{BGColor.FAIL}Error:{BGColor.ENDC} ")
    print(*values, sep=sep, end=end, file=file, flush=flush)

def printgood(*values: object, sep: str | None = " ", end: str | None = "\n", file: Any | None = None, flush: Literal[False] = False) -> None:
    values = list(values)
    values[0] = f"{BGColor.OKGREEN}{values[0]}"
    values[-1] = f"{values[-1]}{BGColor.ENDC}"
    print(*values, sep=sep, end=end, file=file, flush=flush)

def printok(*values: object, sep: str | None = " ", end: str | None = "\n", file: Any | None = None, flush: Literal[False] = False) -> None:
    values = list(values)
    values[0] = f"{BGColor.OKBLUE}{values[0]}"
    values[-1] = f"{values[-1]}{BGColor.ENDC}"
    print(*values, sep=sep, end=end, file=file, flush=flush)

if __name__ == "__main__":
    printwarning("some warning")
    printerror("some warning")
    printgood("some warning")
    printok("some warning")
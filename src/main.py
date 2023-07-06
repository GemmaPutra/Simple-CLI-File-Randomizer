import sys
from iterfile import RandomizeIterFile, FileIsNotFolder, ChaosMethod
from maid import printerror, printwarning, printok, printgood

def main() -> None:
    method_comm = {
        "scramble": ["/s", "-s", "/scramble", "--scramble"],
        "random": ["/r", "-r", "/random", "--random"],
    }

    _, *term_arg = sys.argv

    if len(term_arg) == 1 and term_arg[-1] in ["/h", "-h", "/help", "--help"]:
        print("help!")
        quit()

    try:
        path, method, *detail = term_arg
        itf = RandomizeIterFile(path)

        # if not valid method '/r' or '/s'
        if method not in method_comm["random"] and method not in method_comm["scramble"]:
            printerror("flag has to be either '/random | /r' or '/scramble | /s'")
            quit(4)

        if method in method_comm["random"]:
            try:
                rand_len, *detail = detail
            # if method is random and random length is not exist
            except ValueError as _:
                printerror("randomize command lack randomize length argument")
                quit(7)

            # if not valid number
            if not rand_len.isdigit():
                printerror("random length must be a whole number")
                quit(5)

            rand_len = int(rand_len)

            # if lower than allowed limit
            if rand_len < 5:
                printerror("random length cannot exceed lower than '5'")
                quit(6)

            itf.randomize_len = rand_len
        elif method in method_comm["scramble"]:
            itf.randomize_len = 5
    # if argument cannot met the requirements
    except ValueError as _:
        printerror("command lack argument at least more than '2' argument")
        quit(1)
    # if path is not exist
    except FileNotFoundError as _:
        printerror("destination cannot be found")
        quit(2)
    # if path is not a folder
    except FileIsNotFolder as _:
        printerror("file target is not a folder")
        quit(3)

    if term_arg[1] in method_comm["random"]:
        unnamed_cand = itf.chaos_naming(method=ChaosMethod.Random)
    if term_arg[1] in method_comm["scramble"]:
        unnamed_cand = itf.chaos_naming(method=ChaosMethod.Scramble)

    if not unnamed_cand:
        for unfile_ in unnamed_cand:
            printwarning(f"cannot rename : {unfile_.name!r}")

    col_det = None
    try:
        col_det, *detail = detail
    except ValueError as _:
        pass # ignore

    for det_ in detail:
        if col_det in ["/b", "-b"]:
            printok(det_)
        elif col_det in ["/g", "-g"]:
            printgood(det_)
        else:
            print(det_)

if __name__ == "__main__":
    main()
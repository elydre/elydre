'''    _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________
 - codé en : UTF-8
 - langage : python3
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
'''


PART_SIZE = 0x1000 # 4Ko

IMM_COUNT = 54
MLIST = [0] * IMM_COUNT


# imm (0: empty, 1: allocated, 2: hooked)

# portable function

def get_state(imm, index):
    last = -1
    for _ in range(index + 1):
        last = (last - last % 3) // 3 if last != -1 else imm
    return int(last % 3)


def set_state(imm, index, new):
    old = get_state(imm, index) * 3 ** index
    return imm - old + new * 3 ** index


def get_required_part(size):
    return (size + PART_SIZE - 1) // PART_SIZE

def alloc(size):  # sourcery skip: use-itertools-product
    required_part = get_required_part(size)
    suite = 0
    for mi in range(IMM_COUNT):
        for i in range(19):
            num = get_state(MLIST[mi], i)
            if num == 0: suite += 1
            else: suite = 0
            if suite != required_part: continue
            debut = i - required_part + 1
            imm_debut = mi

            if debut < 0:
                imm_debut = (-debut) // 19 + 1
                debut = 19 * imm_debut + debut
                imm_debut = mi - imm_debut

            for k in range(debut, debut + required_part):
                val = 1 if k == debut else 2
                MLIST[imm_debut + k // 19] = set_state(MLIST[imm_debut + k // 19], k % 19, val)
            return imm_debut * 19 + debut


def free(index):
    list_index = index // 19
    i = index % 19
    if get_state(MLIST[list_index], i) == 1:
        MLIST[list_index + i // 19] = set_state(MLIST[list_index + i // 19], i % 19, 0)
        i += 1
        while get_state(MLIST[list_index + i // 19], i % 19) == 2:
            MLIST[list_index + i // 19] = set_state(MLIST[list_index + i // 19], i % 19, 0)
            i += 1
        return True
    return False

def get_memory_usage():
    # sourcery skip: remove-unnecessary-cast, simplify-constant-sum, sum-comprehension, use-itertools-product
    useds = 0
    for mi in range(IMM_COUNT):
        for i in range(19):
            if get_state(MLIST[mi], i) > 0:
                useds += 1
    return useds * (PART_SIZE // 1024)


# python shell function

while True:

    inp = input("\033[95mb3-shell-> \033[0m").split(" ")
    cmd = inp[0]

    if cmd in ("plist", "l"):
        print(MLIST)

    elif cmd in ("print", "p"):
        for mi in range(IMM_COUNT):
            for i in range(19):
                val = get_state(MLIST[mi], i)
                if val == 0: print("0", end="")
                if val == 1: color = 41 + (i + mi) % 7
                if val > 0: print(end = f"\x1b[6;30;{color}m{val}\x1b[0m")
            print(end = "   ")
            if mi % 3 == 2: print()
    
    elif cmd in ("alloc", "a"):
        print("Allocated at:", alloc(int(f"0x{inp[1]}000", 16)))

    elif cmd in ("free", "f"):
        if free(int(inp[1])): print("Successfully freed")
        else: print("Error: not allocated or hooked")

    elif cmd in ("usage", "u"):
        print("Memory usage:", get_memory_usage(), "Ko")

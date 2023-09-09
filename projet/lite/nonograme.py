TOP  = 0
LEFT = 1

ISSUE    = 0
NO_ISSUE = 1
SOLVED   = 2

EMPTY = 0
CROSS = 1
DOT   = 2


def fail(msg):
    print(f"[FATAL] {msg}")
    exit(1)


def check_borders(borders, size):
    if len(borders) != 2:
        return False
    if (size == 0):
        size = len(borders[0])
    for i in range(2):
        if len(borders[i]) != size:
            return False
        for j in range(size):
            for k in range(len(borders[i][j])):
                if (not isinstance(borders[i][j][k], int)) or (borders[i][j][k] < 0 or borders[i][j][k] > size):
                    return False
    return True


def check_cnt(cnt, size):
    if len(cnt) != size:
        return False
    for i in range(size):
        if len(cnt[i]) != size:
            return False
        for j in range(size):
            if cnt[i][j] not in [0, 1, 2]:
                return False
    return True


def is_valid_line(line, values):
    def dots_at_ends(line, from_index):
        if from_index >= len(line):
            return False
        for i in range(from_index, len(line)):
            if line[i] == DOT:
                return True
        return False

    complet = not any([elem == EMPTY for elem in line])
    line_index = 0
    val_index = 0

    count = 0
    lgood = False
    dot_i = -1

    while line_index < len(line):
        val = values[val_index]

        if line[line_index] == DOT:
            if dot_i == -1:
                dot_i = line_index
            count += 1

        elif line[line_index] == CROSS:
            if (not lgood) and count != 0 and count < val:
                return ISSUE
            count = 0
            dot_i = -1

        elif line[line_index] == EMPTY:
            if lgood:
                count = 0
            elif count < val:
                count += 1

        if count >= val:
            if (dot_i == -1 or line_index - dot_i < val - 1) and dots_at_ends(line, line_index + 1):
                count -= 1
            elif count > val:
                return ISSUE

        lgood = False

        if count == val:
            val_index += 1

            if val_index == len(values):
                break

            lgood = True
        line_index += 1

    # print(f"{line=}, {values=}, {line_index=}, {val_index=}, {count=}, {dot_i=}")

    if val_index < len(values):
        return ISSUE
    
    if not dots_at_ends(line, line_index + 1):
        return SOLVED if complet else NO_ISSUE

    return ISSUE


class game:
    def __init__(self, size = 0, cnt = None, borders = None):
        if borders == None:
            fail("game: borders not specified")
        if not check_borders(borders, size):
            fail("game: borders are not valid")
        size = len(borders[0])
        if size == 0 or size > 99:
            fail("game: size is not valid")
        if cnt == None:
            cnt = [[0 for _ in range(size)] for __ in range(size)]
        else:
            check_cnt(cnt, size)
        self.size = size
        self.cnt = cnt
        self.borders = borders

    def ascii_display(self):
        top_maxlen = max([len(elem) for elem in self.borders[TOP]])
        left_maxlen = max([len(elem) for elem in self.borders[LEFT]])

        for i in range(top_maxlen):
            print(" " * left_maxlen * 2, end=" ")
            for j in range(self.size):
                dec = top_maxlen - len(self.borders[TOP][j])
                if i < dec:
                    print("  ", end="")
                else:
                    if len(str(self.borders[TOP][j][i - dec])) == 1:
                        print(".", end="")
                    print(self.borders[TOP][j][i - dec], end="")
            print()

        for i in range(self.size):
            for j in range(left_maxlen):
                dec = left_maxlen - len(self.borders[LEFT][i])
                if j < dec:
                    print("  ", end="")
                else:
                    if len(str(self.borders[LEFT][i][j - dec])) == 1:
                        print(".", end="")
                    print(self.borders[LEFT][i][j - dec], end="")
            print(" ", end="")
            for j in range(self.size):
                if self.cnt[i][j] == EMPTY:
                    print("  ", end="")
                elif self.cnt[i][j] == CROSS:
                    print("[]", end="")
                elif self.cnt[i][j] == DOT:
                    print("##", end="")
            print()

    def is_valid(self):
        # check if cnt is valid with nonogram rules
        # lines
        complet = True

        for i in range(self.size):
            values = self.borders[LEFT][i]
            line = self.cnt[i]

            tmp = is_valid_line(line, values)
            if tmp == ISSUE:
                return ISSUE
            elif tmp == NO_ISSUE:
                complet = False

        # columns
        for i in range(self.size):
            values = self.borders[TOP][i]
            column = [self.cnt[j][i] for j in range(self.size)]
            
            tmp = is_valid_line(column, values)
            if tmp == ISSUE:
                return ISSUE
            elif tmp == NO_ISSUE:
                complet = False

        return SOLVED if complet else NO_ISSUE

    def is_valid_fast(self, row, col):
        # line
        tmp = is_valid_line(self.cnt[row], self.borders[LEFT][row])
        if tmp == ISSUE:
            return ISSUE
        complet = tmp == SOLVED

        # column
        tmp = is_valid_line([self.cnt[j][col] for j in range(self.size)], self.borders[TOP][col])
        if tmp == ISSUE:
            return ISSUE
        complet = complet and tmp == SOLVED

        return SOLVED if complet else NO_ISSUE

    def rec_solve(self, i = 0, j = 0):
        if i == self.size:
            return self.is_valid() == SOLVED

        if j == self.size:
            return self.rec_solve(i + 1, 0)

        if self.cnt[i][j] != EMPTY:
            return self.rec_solve(i, j + 1)

        self.cnt[i][j] = CROSS
        if self.is_valid_fast(i, j) != ISSUE and self.rec_solve(i, j + 1):
            return True

        self.cnt[i][j] = DOT
        if self.is_valid_fast(i, j) != ISSUE and self.rec_solve(i, j + 1):
            return True

        self.cnt[i][j] = EMPTY

        return False


# plat = game(borders = [
#     [[2], [3, 1], [2, 2], [10], [2, 2], [2, 2], [5, 4], [2, 2], [3, 1], [2]],
#     [[1, 1], [1, 1], [1, 1], [8], [10], [2, 1, 2], [6], [8], [1, 1], [1, 1]]
# ])

plat = game(borders = [
    [[5], [1, 3], [1, 2, 3], [5, 3], [3, 4, 3], [4, 4, 3], [5, 2, 3], [5, 4], [7, 5], [14], [6, 6], [7], [11], [11], [9]],
    [[4], [8], [10], [11], [11], [11], [2, 2, 4], [1, 3, 2, 3], [1, 5, 2, 3], [1, 5, 2, 3], [1, 3, 3, 3], [2, 4, 2], [11], [9], [7]],
])

plat.ascii_display()
print(plat.rec_solve())
plat.ascii_display()

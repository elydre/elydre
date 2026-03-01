# read en parse markdown to manpage
import re

def read_file(file):
    with open(file, "r") as f:
        return f.readlines()

lines = read_file("Olivine.md")

output = ""

LIGHT_BLUE = "\033[94m"
LIGHT_GREEN = "\033[92m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GRAY = "\033[37m"
GREEN = "\033[32m"
PURPLE = "\033[35m"
END = "\033[0m"

"""
#define CHAR_VERT   0xB3
#define CHAR_HORI   0xC4
#define CHAR_CROSS  0xC3
#define CHAR_CORNER 0xC0
# """

VERT = ">"

def iswhitespace(c):
    return c == " " or c == "\n"

def compute_line(strin, color=CYAN, reset=END):
    # replace "`" by gray color
    string = re.sub(r"`(.*?)`", f"{GRAY if color == CYAN else color}\\1{reset}", strin)

    if strin != string:
        return string

    # replace bold, italic, underline by white color
    string = re.sub(r"\*\*(.*?)\*\*", f"{color}\\1{reset}", string)
    string = re.sub(r"\*(.*?)\*", f"{color}\\1{reset}", string)
    string = re.sub(r"_(.*?)_", f"{color}\\1{reset}", string)

    # replace "[...](...)" by green color
    string = re.sub(r"\[(.*?)\]\((.*?)\)", f"{PURPLE if color == CYAN else color}\\1{reset}", string)

    return string

i = 0
while i < len(lines):
    line = lines[i].strip()
    i += 1

    if line.startswith("#"):
        count = 0
        for e in line:
            if e == "#":
                count += 1
            else:
                break
        line = line[count:].strip()
        if (count == 1):
            line = line.upper()
        if not output.endswith("\n\n"):
            output += "\n"
        output += " " * (count - 1) + f"{LIGHT_BLUE if count < 3 else BLUE}{line}{END}\n\n"
    elif line.startswith("```"):
        if not output.endswith("\n\n"):
            output += "\n"
        while i < len(lines) and not lines[i].startswith("```"):
            output += f"{GRAY}{VERT} {lines[i][:-1]}{END}\n"
            i += 1
        output += "\n"
        i += 1
    elif line.startswith(">"):
        if not output.endswith("\n\n"):
            output += "\n"
        output += f"{GREEN}{compute_line(line[1:].strip(), LIGHT_GREEN, GREEN)}{END}"
        while i < len(lines) and lines[i].strip().startswith(">"):
            if not iswhitespace(output[-1]):
                output += " "
            output += f"{GREEN}{compute_line(lines[i][1:].strip(), LIGHT_GREEN, GREEN)}{END}"
            i += 1
        output += "\n\n"
    elif line.startswith("* ") or line.startswith("- "):
        if not output.endswith("\n\n"):
            output += "\n"
        output += f" - {line[1:].strip()}\n"
        while i < len(lines) and (lines[i].strip().startswith("* ") or lines[i].strip().startswith("- ")):
            output += f" - {lines[i][1:].strip()}\n"
            i += 1
        output += "\n"
    elif line.startswith("|"):
        if not output.endswith("\n\n"):
            output += "\n"
        output += f"{compute_line(line)}\n"
        while i < len(lines) and lines[i].strip().startswith("|"):
            output += f"{compute_line(lines[i])}"
            i += 1
        output += "\n"
    elif line == "":
        if not output.endswith("\n"):
            output += "\n\n"
    else:
        if not iswhitespace(output[-1]):
            output += " "
        output += compute_line(line)

while output.endswith("\n"):
    output = output[:-1]

print(output)

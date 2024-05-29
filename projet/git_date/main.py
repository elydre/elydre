from random import randint
import os

path = os.path.dirname(os.path.abspath(__file__))

def error_parse(cnd: bool, msg: str):
    if not cnd:
        return
    print(f"[ERROR IN PARSE] {msg}")
    exit(1)

def parse(string: str):
    string = string.replace(" ", "")
    part = string.split(",")
    exit_list = []

    for e in part:
        if e.isdigit():
            exit_list.append(int(e))

        elif "-" in e:
            temp = e.split("-")

            error_parse(len(temp) != 2, "Range must be in format 'a-b'")
            error_parse(not temp[0].isdigit(), f"Range start must be a number, not '{temp[0]}'")
            error_parse(not temp[1].isdigit(), f"Range end must be a number, not '{temp[1]}'")

            start, end = int(temp[0]), int(temp[1])

            error_parse(start > end, f"Range start must be less than end, not {start} - {end}")

            exit_list.extend(iter(range(start, end + 1)))

        else:
            error_parse(f"Invalid input: '{e}'")

    return exit_list

def push_at_dates(day_ago: list):
    for ida in day_ago:
        d = f"{ida} day ago"
        print(d)
        with open(f"{path}/date.txt", "w") as file:
            file.write(str(randint(0, 10000)))
        os.system("git add *")
        os.system(f"git commit --date=\"{d}\" -m \"update date.txt\"")

if __name__ == "__main__":
    dates = parse(input("DATES: "))
    confirm = input(f"Are you sure you want to push at {dates} day ago? [Y/n] ")
    
    if confirm.lower() in ["y", "yes", ""]:
        push_at_dates(dates)
    else:
        print("Canceled")

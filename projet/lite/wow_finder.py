def with_letters(word, letters):
    for letter in word:
        if letter not in letters:
            return False
        else:
            letters = letters.replace(letter, "", 1)
    return True

with open("words.txt") as f:
    word_list = f.read().splitlines()

def fix_word(word):
    replacements = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "î": "i",
        "ï": "i",
        "ô": "o",
        "ù": "u",
        "û": "u",
        "ç": "c",
        "œ": "oe",
        "æ": "ae",
    }
    word = word.lower()
    for k, v in replacements.items():
        word = word.replace(k, v)
    return word

def find_in_word_list(word_list, letters):
    old = None
    for word in word_list:
        patched = fix_word(word)
        if len(patched) < 3:
            continue
        if with_letters(patched, letters):
            if old == patched:
                print(end=" / ")
            elif old is not None:
                print()
            print(end=word)
            old = patched
    if old is not None:
        print("\n")

while True:
    letters = input("Letters: ").lower()
    find_in_word_list(word_list, letters)

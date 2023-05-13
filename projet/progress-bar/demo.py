from progress_bar import Bar
from time import sleep

def progress_loop():
    for i in range(42):
        test.progress(i+1)
        sleep(0.2)


# percentage mode
test = Bar(42, "*", "p")
progress_loop()

# steps mode
test = Bar(42, "-", "s")
progress_loop()

# clean mode
test = Bar(42, "#", "c")
progress_loop()

print()
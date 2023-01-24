print("runing")

for i in range(20000):
    max = int(i ** 0.5 + 1)
    if i%2 != 0:
        for x in range(max-2):
            x2 = x + 2
            if i%x2 == 0:
                break
            if x2 == max-1:
                print(i)
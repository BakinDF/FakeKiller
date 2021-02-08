import os

folder = 'data/true/'
dist = 'data/true_new/'

counter = 1
for path in os.listdir(folder):
    print(f'{dist}{path}')
    # with open(folder + path, mode='r+', encoding='utf-8') as file:
    with open(f'{dist}{str(counter)}.txt', mode='w', encoding='utf-8') as dist_file:
        with open(folder + path, mode='r+', encoding='utf-8') as file:
            f = file.read()
            res = ""
            f1 = f2 = f3 = True
            for i in f:
                if i == "&":
                    f1 = False
                if i == ";":
                    f1 = True
                if i == "<":
                    f2 = False
                if i == ">":
                    f2 = True
                if i == "[":
                    f3 = False
                if i == "]":
                    f3 = True
                if f1 and f2 and f3:
                    if i not in ";>]":
                        res += i
            if "МОСКВА. " in res[:8]:
                res = res[8:]
            dist_file.write(res)

    counter += 1

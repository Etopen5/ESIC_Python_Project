def table():
    i = 1
    while i <= 10 : 
        print("table de multiplication de ", i)
        y = 1
        while y <=10:
            print(i*y)
            y += 1
        i += 1
    return "done"

print(table())
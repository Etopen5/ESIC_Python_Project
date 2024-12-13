def compterVoyelles():
    res = 0
    liste = input("Entrer un phrase\n")
    for i in liste :
        if i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u' or i == 'y' :
            res += 1
    return res

print(compterVoyelles())
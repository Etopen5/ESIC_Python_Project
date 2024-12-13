def plusGrandNombre() :
    liste = []
    n = int(input("Entrer le nombre d'éléments: "))

    for i in range(n):
        élément = int(input(f"Entrer l\'élément {i+1}: "))
        liste.append(élément)
    res = 0
    for y in liste :
        if y > res :
            res = y
    print(res, "est le plus grand nombre")
    return "done"

print(plusGrandNombre())
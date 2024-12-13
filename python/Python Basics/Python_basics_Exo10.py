def factorielle(nnn):
    if nnn > 1 :
        return factorielle(nnn-1)*nnn
    return nnn

x = int(input("Entrer le nombre\n"))

print(factorielle(x))
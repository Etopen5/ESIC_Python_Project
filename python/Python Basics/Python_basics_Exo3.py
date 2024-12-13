def pairImpair():
    print("Entrée un entier")
    try :
        x = int(input())
    except ValueError : 
        print('Entrée non valide : donner un entier')
    
    if (x%2 == 0):
        print(x, " est pair")
    elif (x%2 == 1):
        print(x, " est impair")
    return "Done"    

print(pairImpair())
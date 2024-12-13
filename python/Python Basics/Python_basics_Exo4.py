def somme():
    try :
        x = int(input())
    except ValueError : 
        print('Entrée non valide : donner un entier')

    i = 1
    res = 0
    while i <= x :
        res += i 
        i += 1
    
    return res

print(somme())
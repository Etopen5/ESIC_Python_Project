import datetime

def calculeAge():
    ajd = datetime.date.today()
    print('Entrer l\'annee')
    try :
        annee = int(input())
    except ValueError : 
        print('Entrée non valide : donner un entier')

    print('Entrer le mois')
    try :
        mois = int(input())
    except ValueError : 
        print('Entrée non valide : donner un entier')

    print('Entrer le jour')
    try :
        jour = int(input())
    except ValueError : 
        print('Entrée non valide : donner un entier')

    naissance = datetime.date(annee, mois, jour)

    age = ajd.year - naissance.year - ((ajd.month, ajd.day) < (naissance.month, naissance.day))

    return age

print(calculeAge(), "years")
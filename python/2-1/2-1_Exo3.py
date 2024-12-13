def majuscule_mot(chaine):
    res = ''
    tmp = 0
    chaine = chaine.capitalize()
    for i in chaine :
        if tmp == 1:
            res += i.upper()
            tmp = 0
        else :
            res += i

        if i == ' ':
            tmp = 1

    return res

print(majuscule_mot("je mange du fromage"))
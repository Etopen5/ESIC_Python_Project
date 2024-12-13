def retourne(chaine):
    res = ''
    list = chaine.split()
    list.reverse()
    for i in list :
        res += i
        res += ' '
    return res

print(retourne("J'en suis tout retourné"))
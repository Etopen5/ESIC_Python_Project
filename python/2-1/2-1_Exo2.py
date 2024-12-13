def premierMot(chaine):
    res = ''
    for i in chaine :
        if i == ' ':
            break
        res += i
    return res

print(premierMot("samedi soir, je vais au cinema"))
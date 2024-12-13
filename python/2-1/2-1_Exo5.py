def image(chaine):
    chainebis = chaine + ' '
    cpt = 0
    lastletter = chainebis[0]
    res = ''
    for i in chainebis:
        if i == lastletter : 
            cpt += 1

        else :
            res += str(cpt) + lastletter
            cpt = 1

        lastletter = i
    
    return res

def dix_image():
    i = 1
    res = "1"
    while i <= 10 :
        res = image(str(res))
        print("u",i," = ",res)
        i += 1
    return "done"

print(dix_image())
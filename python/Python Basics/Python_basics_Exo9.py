def isAPalindrome():
    liste = input("Entrer le mot à tester\n")
    palindrome = liste[::-1]
    if liste == palindrome:
        return "c'est un palindrome"
    return "ce n'est pas un palindrome"
    
print(isAPalindrome())
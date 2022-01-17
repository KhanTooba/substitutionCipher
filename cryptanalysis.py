import random
import sys
from ngram_score import ngram_score
from random import shuffle
from datetime import datetime

fitness = ngram_score('quadgrams.txt')

def readCipherText(fileName):
    f = open(fileName, "r")
    text = f.read()
    return text

def firstTimeDecipher(text, freq, substitue):
    count = 0
    while(freq.items()):
        maxVal = -1
        maxKey = ""
        for key,value in freq.items():
            if maxVal < value:
                maxVal = value
                maxKey = key
        text=text.replace(chr(maxKey),substitue[count])
        count = count + 1
        freq.pop(maxKey)
    return text

def calculateIC(text):
    freq = {}
    ic=0

    for c in text:
        if c==" " or c==' ' or c=="," or c=="." or c=="!" or c==";":
            continue
        i=ord(c)
        freq[i] = freq.get(i, 0) + 1

    for key,value in freq.items():
        ic=ic+value*(value-1)
    
    l=len(text)
    icFinal = ic/(l*(l-1))

    return freq, icFinal

def decipher(ciphertext, key):
    mapping = {}
    for k in range(0,len(key)):
        mapping[key[k]]=chr(k+65)
    str1=""
    # print(mapping)
    for l in range(0,len(ciphertext)):
        currentChar = ciphertext[l]
        # print(currentChar)
        if currentChar==" " or currentChar=="," or currentChar=="." or currentChar=="!" or currentChar==";":
            str1=str1+currentChar
        else:
            str1=str1+mapping[ciphertext[l]]
    return str1

def gen(text, now):
    max = -sys.maxsize
    key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    masterKey, masterScore = key[:], max

    generation = 0
    cipher = text
    while (1):
        second = datetime.now()
        diff = str(second-now)
        ftr = [3600,60,1]
        s = sum([a*b for a,b in zip(ftr, map(float,diff.split(':')))])
        # print(s)
        if s>5:
            break

        count = 0
        
        random.shuffle(masterKey)
        masterScore = fitness.score(decipher(cipher, masterKey).replace(" ",""))

        while(count<1000):
            tempKey = masterKey[:]
            i = random.randint(0,25)
            j = random.randint(0,25)
            a = tempKey[i]
            b = tempKey[j]
            tempKey[i] = b
            tempKey[j] = a
            
            tempPlain = decipher(cipher, tempKey)
            tempScore = fitness.score(tempPlain.replace(" ",""))
            if tempScore > masterScore:
                masterScore = tempScore
                masterKey = tempKey[:]
                count = count/2 #Try with count=count/2
            count = count+1
        
        if max<masterScore:
            max = masterScore
            key = masterKey[:]
            # print("Best achieved thus far is in generation ", generation)
            tempPlain = decipher(cipher, key)
            # print(key)
            # print(tempPlain)
            # print(max)
        generation = generation+1
    return key, max, cipher

def runner(fileNumber):
    now = datetime.now()
    # fileNumber = "1"
    fileName = "ciphertext-"+fileNumber+".txt"
    text = readCipherText(fileName)
    # print(text)
    freq, ic = calculateIC(text)
    substitue="ETAOINHSRDLUMCWFGYPBVKJXQZ"
    text = firstTimeDecipher(text, freq, substitue)
    # print(text)
    # print(fitness.score(text.replace(" ","")))
    key , max , cipher= gen(text, now)
    # print("The final key is: ",key)
    # print("Deciphered text is: ", decipher(cipher, key))
    plainText = decipher(cipher, key)
    return key, plainText

def getOriginalKey(key, plain, fileNumber):
    originalKey = key[:]
    cipherCharacters = ['1','2','3','4','5','6','7','8','9','0','@','#','$','n','o','p','q','r','s','t','u','v','w','x','y','z']
    fileName = "ciphertext-"+fileNumber+".txt"
    cipherText = readCipherText(fileName)
    print("\nThe cipher text was: \n", cipherText,"\n\n")
    i = 0
    while(i<26):
        # print("for index :",i)
        for j in range(0,len(plain)):
            originalKey[i] = ''
            if plain[j]==chr(i+65):
                # print(j,"---",plain[j],"---",cipherText[j])
                originalKey[i] = cipherText[j]
                cipherCharacters.remove(cipherText[j])
                break
        i = i+1
    # print(cipherCharacters)
    i = 0
    # print(originalKey)
    for j in range(0,len(originalKey)):
        if originalKey[j]=='':
            originalKey[j] = cipherCharacters[i]
            i=i+1
    return originalKey

def getKey(fileNumber):
    key, plainText = runner(fileNumber)
    originalKey = getOriginalKey(key, plainText, fileNumber)
    print("The original and final Key is: \n", originalKey)
    return key

def getPlainText(fileNumber):
    key, plainText = runner(fileNumber)
    return plainText

def enter():
    fileNumber = input("Enter the cipher text number you want to decrypty:")
    return fileNumber

fileNumber = enter()
print("\n----------Searching for Key----------\n")
k = getKey(fileNumber)
# print("The final Key is------: ",k)
p = getPlainText(fileNumber)
print("\n----------Searching for plainText----------\n")
print("The plain Text is: \n",p,"\n")
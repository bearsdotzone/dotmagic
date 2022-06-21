import time
import requests
import urllib.parse
import json
import requests_cache

def oracleText(oracle_text):
    lines = []

    if(len(oracle_text) == 0):
        return lines

    toCut = oracle_text.split('\n')
    
    for x in toCut:
        wordSplit = x.split(' ')
        
        toAdd = str()
        while(len(wordSplit) > 0):
            peek = wordSplit[0]
            if len(toAdd) + len(peek) + 1 <= 26:
                toAdd += wordSplit.pop(0) + " "
            else:
                lines += [toAdd]
                toAdd = str()
        if len(toAdd) > 0:
            lines += [toAdd]

    return lines

def returnCard(inputJSON):
    toReturn = str()
    toReturn += '/' + ('-' * 28) + '\\\n'
    toReturn += '| {0}{1}{2} |\n'.format(inputJSON['name'], (26 - len(inputJSON['name']) - len(inputJSON['mana_cost'])) * ' ', inputJSON['mana_cost'] )
    toReturn += '|' + ('-' * 28) + '|\n'

    availableLines = 16
    if 'power' not in inputJSON.keys():
        availableLines = 18

    oracle = oracleText(inputJSON['oracle_text'])
    if(len(oracle) > availableLines):
        print("noncritical error, cannot print card ", inputJSON['name'])
        return None
    artSize = availableLines - len(oracle)
    if artSize > 1:
        toReturn += ('|' + (' ' * 28) + '|\n') * artSize
        toReturn += '|' + ('-' * 28) + '|\n'

    # Type Line

    if len(inputJSON['type_line']) > 28:
        print("noncritical error, type line too long to print")
        return None
    toReturn += '|{0}{1}{2}|\n'.format(' ' if (len(inputJSON['type_line']) != 28) else '',
                                        inputJSON['type_line'],
                                        (27 - len(inputJSON['type_line'])) * ' ')
    if 'power' in inputJSON.keys() or len(inputJSON['oracle_text']) > 0:
        toReturn += '|' + ('-' * 28) + '|\n'
    
    # Oracle Text

    if(len(oracle) > 0):
        for x in oracle:
            toReturn += '| {0}{1} |\n'.format(x, (26-len(x)) * ' ')
        if 'power' in inputJSON.keys():
            toReturn += '|' + ('-' * 28) + '|\n'

    # P/T

    if 'power' in inputJSON.keys():
        pt = '[' + inputJSON['power'] + '/' + inputJSON['toughness'] + ']'
        toReturn += '| {0}{1} |\n'.format((26 - len(pt)) * ' ', pt)
    toReturn += '\\' + ('-' * 28) + '/\n'
    return toReturn.replace('{', '[').replace('}', ']')

f = open("input.txt", "r")

cardList = []

requests_cache.install_cache(expire_after=600)
# print(requests_cache.cache.urls)

for x in f:
    firstSplit = x.find(' ')
    howMany = int(x[:firstSplit].strip())
    for y in range(0,howMany):
        cardList+=[x[firstSplit+1:].strip()]

# cache = dict()

toWrite = open("test.txt", "w+")

for x in cardList:
    # Pull from Scryfall
    # if(x not in cache.keys()):
    queryString = 'https://api.scryfall.com/cards/named?fuzzy=' + urllib.parse.quote_plus(x)
    request = requests.get(queryString)
    if request.status_code != 200:
        print('non-critical error on', x, 'code', request.status_code)
    # cache[x] = json.loads(request.text)
    thisCard = returnCard(json.loads(request.text))
    print(thisCard)
    toWrite.write(thisCard)

    time.sleep(0.1)
    # Print Name
    # print('{0} {1}'.format())
    # Print CMC
    # Print Types
    # Print Oracle
    # Print Power
    # Print Toughness
# print(cardList)



toWrite.close()

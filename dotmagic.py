import time
import requests
import urllib.parse
import json
import requests_cache
import re


# Format the oracle text into appropriate paragraph breaks
# Max 26 chars per line
# TODO add vowel removal to fit long text
# TODO change from hardcoded 26
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
                # TODO figure out if we can be marginally more efficient by not
                # assuming a space
                toAdd += wordSplit.pop(0) + " "
            else:
                lines += [toAdd]
                toAdd = str()
        if len(toAdd) > 0:
            lines += [toAdd]

    return lines

# Formats the card based off the whole JSON blob
# TODO pull formatting out into a more modular system
# TODO allow for different sizes of card
# TODO work for two sided cards
def returnCard(inputJSON):
    print(inputJSON['name'])
    toReturn = str()
    toReturn += '/' + ('-' * 28) + '\\\n'

    if 26 - len(inputJSON['name']) - len(inputJSON['mana_cost']) < 0:
        inputJSON['name'] = re.sub('[AEIOUaeiou]', '', inputJSON['name'][::-1], (-1 * (26 - len(inputJSON['name']) - len(inputJSON['mana_cost']))))[::-1]

    toReturn += '|{3}{0}{1}{2}{4}|\n'.format(inputJSON['name'], (26 - len(inputJSON['name']) - len(inputJSON['mana_cost'])) * ' ', inputJSON['mana_cost'], '' if len(inputJSON['name']) + 1 + len(inputJSON['mana_cost']) > 26 else ' ',  '' if len(inputJSON['name']) + 1 + len(inputJSON['mana_cost']) > 27 else ' ')
    toReturn += '|' + ('-' * 28) + '|\n'

    availableLines = 16
    if 'power' not in inputJSON.keys():
        availableLines = 18

    oracle = oracleText(inputJSON['oracle_text'])
    if(len(oracle) > availableLines):
        # TODO debug argument
        print("noncritical error, cannot print card ", inputJSON['name'])
        # return None
    artSize = availableLines - len(oracle)
    if artSize >= 1:
        toReturn += ('|' + (' ' * 28) + '|\n') * artSize
        toReturn += '|' + ('-' * 28) + '|\n'
    if artSize == 0:
        toReturn += ('|' + (' ' * 28) + '|\n')

    # Type Line

    if len(inputJSON['type_line']) > 28:
        # TODO debug argument
        print("noncritical error, type line too long to print")
        inputJSON['type_line'] = re.sub('[AEIOUaeiou]', '', inputJSON['type_line'], (-1 * (28 - len(inputJSON['type_line']))))
        # return None
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

def main():
    # TODO argument
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

    returnedCards = []

    for x in cardList:
        # Pull from Scryfall

        # TODO integrate with requests-cache more effictively, ala rate limiting
        # TODO flag to wipe cache
        queryString = 'http://api.scryfall.com/cards/named?fuzzy=' + urllib.parse.quote_plus(x)
        request = requests.get(queryString)
        if request.status_code != 200:
            print('non-critical error on', x, 'code', request.status_code)
        # cache[x] = json.loads(request.text)
        thisCard = returnCard(json.loads(request.text))
        # print(thisCard)
        # toWrite.write(thisCard)
        returnedCards += [thisCard]

        time.sleep(0.1)


    # TODO Print these guys out more intelligently

    for x in range(0, len(returnedCards), 4):
        workingFile= open("out{0}.txt".format(x), "w+")

        split0 = returnedCards[x].split('\n')
        split1 = returnedCards[x+1].split('\n')
        split2 = returnedCards[x+2].split('\n')
        split3 = returnedCards[x+3].split('\n')

        for y in range(len(split0)):
            workingFile.write('{0} {1}\n'.format(split0[y], split1[y]))
        for y in range(len(split0)):
            workingFile.write('{0} {1}\n'.format(split2[y], split3[y]))


        workingFile.close()

if __name__ == "__main__":
    main()
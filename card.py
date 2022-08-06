import re

# def shakerPad(toAdd, *items):
#     if len(items) > 1:


def createPadding(desiredWidth, *items):
    freeSpace = desiredWidth - (len(x) for x in items)
    if freeSpace <= 0:
        # will need to cut characters
        freeSpace-=1
    else:
        if len(items) == 1:
            freeSpace-=1
            return ' ' + items + ' ' * freeSpace
        
    

class card:
    field = [[]]
    width = 0
    height = 0
    workingWidth = 0
    workingHeight = 0
    numFaces = 1

    def __init__(self, width, height):
        self.field = [' ' * width] * height
        self.width = width
        self.height = height

        self.workingWidth = width - 2
        self.workingHeight = height - 2

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
    
    def setCard(self, inputJSON):
        # Multiple faces
        if 'card_faces' in inputJSON.keys():
            self.setMultiCard(inputJSON)
            return

        workingLine = 0

        self.field[workingLine] = '/' + ('-' * self.workingWidth) + '\\'

        workingLine = 1
        # Card Name

        cardName = inputJSON['name']
        manaCost = inputJSON['mana_cost']



        if 26 - len() - len(inputJSON['mana_cost']) < 0:
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

    def setMultiCard(self, inputJSON):
        self.numFaces = len(inputJSON['card_faces'])
        self.field = [[' ' * self.width] * self.height] * self.numFaces
# need a way to get identify adjacent numbers in same row as entire integers. Need a way to find characters in adjacent coordinates.



# function that finds numbers within the row.
# function that finds numbers within the row.
def findNums(line, line_index):
    keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    numbers = []
    number = {'value': '', 'coords': []}
    
    for i, char in enumerate(line):
        next_char = line[i+1] if i < len(line) - 1 else ''
        
        if char in keys:
            number['value'] += char
            number['coords'].append([line_index, i])
        
        if char in keys and next_char not in keys:
            numbers.append(number)
            number = {'value': '', 'coords': []}
    
    return numbers

# scans a single number for adjacent symbols and returns true or false depending on what it finds
def scanAdjacentCoords(lines, number):
    isPartNumber = False
    allowed_chars = set('0123456789.')
    for coord in number['coords']:
        adjacentValues = []
        for adjacentCoord in getAdjacentCoords(coord):
            adjacentValues.append(lines[adjacentCoord[0]][adjacentCoord[1]])
        if any(char not in allowed_chars for char in adjacentValues):
            isPartNumber = True
            break
    return isPartNumber

# returns an array of validated adjacent coordinates for any given coordinate
def getAdjacentCoords(coord):
    topLeft = [coord[0]-1, coord[1]-1]
    middleLeft = [coord[0]-1, coord[1]]
    bottomLeft = [coord[0]-1, coord[1]+1]
    topMiddle = [coord[0], coord[1]-1]
    bottomMiddle = [coord[0], coord[1]+1]
    topRight = [coord[0]+1, coord[1]-1]
    middleRight = [coord[0]+1, coord[1]]
    bottomRight = [coord[0]+1, coord[1]+1]
    adjacentCoords = [topLeft, middleLeft, bottomLeft, topMiddle, bottomMiddle, topRight, middleRight, bottomRight]
    validatedCoords = []
    for coord in adjacentCoords:
        valid = True
        for num in coord:
            if num < 0 or num > 139:
                valid = False
        if valid: validatedCoords.append(coord)
    return validatedCoords



with open('day-3-input.txt') as f:
    lines = [list(line) for line in f.read().splitlines()]
    numbers = []
    line_index = 0
    for i, line in enumerate(lines):
        numbers.append(findNums(line, i))
    partNumbers = []
    flattened_numbers = [number for sublist in numbers for number in sublist]
    for number in flattened_numbers:
        if scanAdjacentCoords(lines, number): partNumbers.append(int(number['value']))
    total = 0
    for partNumber in partNumbers:
        total += partNumber
    print(total)
# parse through the whole file and store as a 2-d array
# identify numbers (consecutive integers that are not separated by a new line or symbol or period)
# store as an object number.value, number.coords
# scan adjacent coordinates for symbols (any character that is not a number or a period)
# if an adjacent coordinate has a symbol, push to partNumbers array
# sum values of part numbers
            
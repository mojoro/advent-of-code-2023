class Symbol:
    def __init__(self, value, coords):
        self.value = value
        self.coords = coords
        self.adjacent_numbers = []

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.value == other.value and self.coords == other.coords
        return False
    
    def __hash__(self):
        return hash((self.__repr__()))

    def __repr__(self):
        return f"Symbol(value={self.value}, coords={self.coords})"

# return an array of symbols that match the key
def get_symbols(line, line_index, keys):
    symbols = []
    symbol = Symbol('', [])
    
    for i, char in enumerate(line):
        next_char = line[i+1] if i < len(line) - 1 else ''
        
        if char in keys:
            symbol.value += char
            symbol.coords.append([line_index, i])
        
        if char in keys and next_char not in keys:
            symbols.append(symbol)
            symbol = Symbol('', [])
    
    return symbols

def construct_grid(lines, numbers, gears):
    grid = lines
    for number in numbers:
        for coord in number.coords:
            x, y = coord
            grid[x][y] = number
    for gear in gears:
        for coord in gear.coords:
            x, y = coord
            grid[x][y] = gear
    return grid

def scan_adjacent_coords(lines, number):
    is_part_number = False
    allowed_chars = set('0123456789.')
    for coord in number.coords:
        adjacent_values = []
        for adjacent_coord in get_adjacent_coords(coord):
            adjacent_values.append(lines[adjacent_coord[0]][adjacent_coord[1]])
        if any(char not in allowed_chars for char in adjacent_values):
            is_part_number = True
            break
    return is_part_number

def get_valid_gears(gears, grid):
    adjacent_numbers = []
    validated_gears = []
    for gear in gears:
        for adjacent_coord in get_adjacent_coords(gear.coords[0]):
            x, y = adjacent_coord
            if isinstance(grid[x][y], str):
                continue
            if grid[x][y].value != '*':
                adjacent_numbers.append(grid[x][y])
        
        gear.adjacent_numbers = set(adjacent_numbers)
        if len(gear.adjacent_numbers) == 2:
            validated_gears.append(gear)
        adjacent_numbers = []
    return validated_gears
            


# returns an array of validated adjacent coordinates for any given coordinate
def get_adjacent_coords(coord):
    x, y = coord
    top_left = [x-1, y-1]
    middle_left = [x-1, y]
    bottom_left = [x-1, y+1]
    top_middle = [x, y-1]
    bottom_middle = [x, y+1]
    top_right = [x+1, y-1]
    middle_right = [x+1, y]
    bottom_right = [x+1, y+1]
    adjacent_coords = [top_left, middle_left, bottom_left, top_middle, bottom_middle, top_right, middle_right, bottom_right]
    validated_coords = []
    for coord in adjacent_coords:
        valid = True
        for num in coord:
            if num < 0 or num > 139:
                valid = False
        if valid: validated_coords.append(coord)
    return validated_coords

with open('day-3-input.txt') as f:
    lines = [list(line) for line in f.read().splitlines()]
    numbers = []
    gears = []
    line_index = 0
    for i, line in enumerate(lines):
        numbers.append(get_symbols(line, i, set('0123456789')))
        gears.append(get_symbols(line, i, set('*')))

    flattened_numbers = [number for sublist in numbers for number in sublist]
    flattened_gears = [gear for sublist in gears for gear in sublist]

    grid = construct_grid(lines, flattened_numbers, flattened_gears)
    valid_gears = get_valid_gears(flattened_gears, grid)

    total = 0
    for valid_gear in valid_gears:
        num1, num2 = valid_gear.adjacent_numbers
        total += int(num1.value) * int(num2.value)
    print(total)

# extract all '*' as objects with adjacentNumbers as an array field (by nature, these are all part numbers)
    # def get_gear_symbols returns an array with all '*' as an object with their coordinates
    # def get_adjacent_numbers takes in gear_symbols and flattened_numbers
        # iterating through gear_symbols, get_adjacent_coords and compare the 
# iterate through all '*' objects, if len(adjacentNumbers) == 2, multiply the values and add to total
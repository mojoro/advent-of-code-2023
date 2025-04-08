def findNumFromText(line):
    first_num = None
    final_num = None
    switcher = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    for i in range(len(line)):
        for word in switcher.keys():
            if line[i:i+len(word)] == word:
                if first_num == None:
                    first_num = {"num": switcher[word], "index": i}
                elif first_num != None:
                    final_num = {"num": switcher[word], "index": i}
    if first_num != None and final_num == None:
        final_num = first_num
    return (first_num, final_num)


def findNumFromNums(line):
    first_num = None
    final_num = None
    for j, char in enumerate(line):
        try:
            num = int(char)
            if first_num == None:
                first_num = {"num": num, "index": j}
            elif first_num != None:
                final_num = {"num": num, "index": j}
        except:
            continue
    if first_num != None and final_num == None:
        final_num = first_num
    return (first_num, final_num)

def compareResults(numberResults, textResults):
    if numberResults[0] != None and textResults[0] != None:
        if numberResults[0]["index"] < textResults[0]["index"]:
            first_num = numberResults[0]["num"]
        else:
            first_num = textResults[0]["num"]
        if numberResults[1]["index"] > textResults[1]["index"]:
            final_num = numberResults[1]["num"]
        else:
            final_num = textResults[1]["num"]
        return (str(first_num) + str(final_num))
        
    # if only one result is valid, return that one
    elif numberResults[0] != None and textResults[0] == None:
        return (str(numberResults[0]["num"]) + str(numberResults[1]["num"]))
    elif numberResults[0] == None and textResults[0] != None:
        return (str(textResults[0]["num"]) + str(textResults[1]["num"]))

first_num = None
final_num = None
combined_num = None
sum_total = 0
with open ('puzzle-input.txt', 'r') as file:
    puzzle_input = file.read().splitlines()
    for i, line in enumerate(puzzle_input):
        numberResults = findNumFromNums(line)
        textResults = findNumFromText(line)
        combined_num = compareResults(numberResults, textResults)
        sum_total += int(combined_num)
print(sum_total)

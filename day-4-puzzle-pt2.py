import re

# go through the array[string] representation of the txt file and extract the winning numbers 
# and card numbers
def process_numbers(lines):
  winning_numbers = []
  card_numbers = []
  for line in lines:
    split_line = re.split(r'\s*\|\s*', line)
    scratch_numbers = [int(num) for num in re.split(r'\s+', split_line[1])]
    win_numbers = [int(num) for num in re.split(r'\s+', re.split(r':\s*', split_line[0])[1])]
    scratch_numbers.sort()
    win_numbers.sort()
    winning_numbers.append(win_numbers)
    card_numbers.append(scratch_numbers)

  return [winning_numbers, card_numbers]

# return the amount of matching winning numbers appear in a given card's numbers
def evaluate_cards(winning_numbers, card_numbers):
  i = 0
  j = 0
  x = 0
  results = []
  while i < len(winning_numbers):
    wins = 0
    winning_row = winning_numbers[i]
    card_row = card_numbers[i]
    while j < len(winning_row):
      if x < len(card_row) and winning_row[j] == card_row[x]:
        wins += 1
        x += 1 
      elif x < len(card_row) and winning_row[j] != card_row[x]:
        x += 1
      elif x >= len(card_row):
        x = 0
        j += 1
    results.append(wins)
    j = 0
    i += 1
  return results

# return an array of the appropriate copies based on the question logic
def construct_copies_array(results):
  copy_index = 0
  resulting_cards = [[result] for result in results]
  x = 0
  while x < len(results):
    result = resulting_cards[x]
    if result[0] == 0:
      x += 1
      continue
    for copy in result:
      copy_index = copy
      while copy_index > 0:
        i = x + copy_index
        current_card_array = resulting_cards[i]
        current_card_array.append(results[i])
        copy_index -= 1
    x += 1
    
  return resulting_cards

# flattens and counts the cards
def evaluate_results(results):
  copies_array = construct_copies_array(results)
  flattened_copies_array = [result for sublist in copies_array for result in sublist]
  return len(flattened_copies_array)

with open('day-4-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  winning_numbers, card_numbers = process_numbers(lines)
  results = evaluate_cards(winning_numbers, card_numbers)
  print(evaluate_results(results))
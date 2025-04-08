import re

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

def evaluate_results(results):
  total = 0
  for result in results:
    if result == 0:
      continue
    result_total = pow(2, result-1)
    total += result_total
  
  return total

      



with open('day-4-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  winning_numbers, card_numbers = process_numbers(lines)
  results = evaluate_cards(winning_numbers, card_numbers)
  print(evaluate_results(results))
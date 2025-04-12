import re

def get_possible_outcomes(times):
  all_outcomes = []
  for time in times:
    race_outcomes = []
    for hold_duration in range(0, time+1):
      remaining_time = time - hold_duration
      distance = remaining_time * hold_duration
      race_outcomes.append(distance)
    all_outcomes.append(race_outcomes)
  return all_outcomes

def get_winning_outcomes(record_distances, possible_outcomes):
  all_winning_outcomes = []
  for record_distance, possible_outcome in zip(record_distances, possible_outcomes):
    winning_outcomes = []
    for outcome in possible_outcome:
      if outcome > record_distance: winning_outcomes.append(outcome)
    all_winning_outcomes.append(winning_outcomes)
  return all_winning_outcomes

## This also worked, but getting the winning outcomes first felt like a better step to take, so I did that instead.
# def compare_outcomes_to_records(record_distances, possible_outcomes):
#   win_totals = []
#   for record_distance, possible_outcome in zip(record_distances, possible_outcomes):
#     winning_outcomes = 0
#     for outcome in possible_outcome:
#       winning_outcomes += 1 if outcome > record_distance else 0
#     win_totals.append(winning_outcomes)
#   return win_totals

def get_ways_to_win(all_winning_outcomes):
  total = 1
  for winning_outcomes in all_winning_outcomes:
    total *= len(winning_outcomes)
  return total

# for every alloted time, calculate all possible outcomes of the races.
# compare the outcomes to the distance of that race
# count how many outcomes beat the record distance
# multiply the counts together and print the result
with open('day-6-input.txt') as f:
  lines = [line for line in f.read().splitlines()]

  rate_of_increase = 1
  times = [int(num) for num in re.split(r'\s+', lines[0].split(':')[1].strip())]
  record_distances = [int(num) for num in re.split(r'\s+', lines[1].split(':')[1].strip())]
  possible_outcomes = get_possible_outcomes(times)
  winning_outcomes = get_winning_outcomes(record_distances, possible_outcomes)
  print(get_ways_to_win(winning_outcomes))
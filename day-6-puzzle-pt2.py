import re
import math

# had to do a bit of algebra for this one. Previously we figured out distance using holding_time and time (distance = (time - holding_time)holding_time)
# solving for holding_time resulted in (holding_time = +-sqrt(time^2/4 - distance) + time/2)
def get_holding_times_from_distance(time, record_distance):
  holding_times = [-math.sqrt(time**2/4 - record_distance) + time/2, math.sqrt(time**2/4 - record_distance) + time/2]
  return holding_times

def get_winning_holding_time_range(record_holding_times):
  return range(math.ceil(record_holding_times[0]), math.floor(record_holding_times[1]+1))

# calculate the durations the current record could have done, return the length of the range between those amounts
with open('day-6-input.txt') as f:
  lines = [line for line in f.read().splitlines()]

  rate_of_increase = 1
  time = int(''.join([num for num in re.split(r'\s+', lines[0].split(':')[1].strip())]))
  record_distance = int(''.join([num for num in re.split(r'\s+', lines[1].split(':')[1].strip())]))

  record_holding_times = get_holding_times_from_distance(time, record_distance)
  winning_holding_time_range = get_winning_holding_time_range(record_holding_times)
  ways_to_win = winning_holding_time_range.stop - winning_holding_time_range.start
  print(ways_to_win)
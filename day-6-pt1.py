import re

with open('day-6-input.txt') as f:
  lines = [line for line in f.read().splitlines()]

  times = [int(num) for num in re.split(r'\s+', lines[0].split(':')[1].strip())]
  distances = [int(num) for num in re.split(r'\s+', lines[1].split(':')[1].strip())]
  speeds = [distance/time for distance, time in zip(distances, times)]

  print(speeds)
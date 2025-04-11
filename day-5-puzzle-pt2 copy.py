class ConversionMap:
  def __init__(self, map_data):
    self.map_data = map_data
    self.source_ranges = []
    self.destination_ranges = []
    for dataset in self.map_data:
      destination_num, source_num, range_length = dataset
      self.source_ranges.append(range(source_num, source_num + range_length))
      self.destination_ranges.append(range(destination_num, destination_num + range_length))

  def __eq__(self, other):
    if isinstance(other, ConversionMap):
        return self.map_data == other.map_data
    return False
  
  def get(self, key):
    value = key
    for dataset in self.map_data:
      destination_num, source_num, range_length = dataset
      if (key in range(source_num, source_num + range_length)):
        offset = destination_num - source_num
        value = key + offset
        break
      else: continue
    return value

  def convert_ranges (self, input_ranges):
    results = []
    if not isinstance(input_ranges, list): input_ranges = [input_ranges]
    for input_range in input_ranges:
      results.append(self.convert_range(input_range)[0])
    return simplify_ranges(results)

  # needs to start with one input range
  def convert_range(self, input_ranges):
    to_be_processed = []
    if not isinstance(input_ranges, list): to_be_processed = [input_ranges]
    else: to_be_processed = input_ranges
    results = []
    for destination_range, source_range in zip(self.destination_ranges, self.source_ranges):
      results, remaining = self.__process_input_ranges(to_be_processed, destination_range, source_range, results)
      to_be_processed = [remainder for remainder in remaining]
    if len(to_be_processed) > 0:
      for remainder in to_be_processed: results.append(remainder)

    return simplify_ranges(results)
  

  def __process_input_ranges(self, input_ranges, destination_range, source_range, results):
    remaining = []
    for input_range in input_ranges:
      offset = destination_range.start - source_range.start
      starts_equal, ends_equal, input_contains_map, map_contains_input, overlap_start, overlap_end = self.__get_range_conditionals(source_range, input_range)

      if (starts_equal and ends_equal) or input_contains_map or map_contains_input or overlap_start or overlap_end:
        overlapped_range = range(max(source_range.start, input_range.start), min(source_range.stop, input_range.stop))
        results.append(range(overlapped_range.start + offset, overlapped_range.stop + offset))
        if input_range.start < source_range.start:
          remaining.append(range(input_range.start, source_range.start))
        if input_range.stop > source_range.stop:
          remaining.append(range(source_range.stop, input_range.stop))
      else:
        remaining.append(input_range)
    
    return [results, remaining]

  
  def __get_range_conditionals(self, map_range, input_range):
    starts_equal = map_range.start == input_range.start
    ends_equal = map_range.stop == input_range.stop
    input_contains_map = map_range.start >= input_range.start and map_range.stop <= input_range.stop
    map_contains_input = map_range.start <= input_range.start and map_range.stop >= input_range.stop
    overlap_start = map_range.start > input_range.start and map_range.start < input_range.stop and map_range.stop > input_range.stop
    overlap_end = map_range.start < input_range.start and map_range.stop > input_range.start and map_range.stop < input_range.stop
    return [starts_equal, ends_equal, input_contains_map, map_contains_input, overlap_start, overlap_end]

class ConversionPipe:
  def __init__(self, all_map_data):
    self.conversion_maps = []
    for map_data in all_map_data:
      self.conversion_maps.append(ConversionMap(map_data))
    
  def __eq__(self, other):
    if isinstance(other, ConversionPipe):
      return self.conversion_maps == other.conversion_maps
    return False
  
  def get_location(self, key):
    for conversion_map in self.conversion_maps:
      key = conversion_map.get(key)
    return key
  
  def convert_range(self, input_range):
    if not isinstance(input_range, list): [input_range]
    for conversion_map in self.conversion_maps:
      results = conversion_map.convert_ranges(input_range)
    return results
  
def get_seed_ranges(seed_nums):
  seed_ranges = []
  i = 0
  while i < len(seed_nums):
    seed_range = range(seed_nums[i], seed_nums[i] + seed_nums[i+1])
    seed_ranges.append(seed_range)
    if seed_range.start > seed_range.stop: raise ValueError("Range start cannot be greater than range stop.")
    i += 2

  return seed_ranges

def extract_map_instructions(lines):
  keys = set('0123456789')
  map_instructions = []
  section = -2
  for line in lines:
    if (line == ''):
      continue
    elif (list(line)[0] in keys):
      map_instructions[section].append([int(num) for num in line.split(' ')])
    else:
      map_instructions.append([])
      section += 1
  map_instructions.pop()
  return map_instructions

def simplify_ranges(ranges):
  sorted_ranges = sorted(ranges, key=lambda r: r.start)
  simplified_ranges = []

  for current_range in sorted_ranges:
    if current_range.start > current_range.stop: raise ValueError("Range start cannot be greater than range stop.")
    if not simplified_ranges or simplified_ranges[-1].stop < current_range.start - 1:
      simplified_ranges.append(current_range)
    else:
      # Merge the current range with the last range in simplified_ranges
      last_range = simplified_ranges.pop()
      merged_range = range(last_range.start, max(last_range.stop, current_range.stop))
      simplified_ranges.append(merged_range)

  return simplified_ranges

# refactor code to covert ranges instead of integers
with open('day-5-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  seed_nums = [int(seed) for seed in lines[0].split(': ')[1].split(' ')]
  seed_ranges = get_seed_ranges(seed_nums)
  all_map_data = extract_map_instructions(lines)
  pipe = ConversionPipe(all_map_data)
  print(pipe.convert_range(seed_ranges[0]))
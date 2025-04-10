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
  
  def convert_range(self, input_range):
    to_be_processed = [input_range]
    results = []
    for destination_range, source_range in zip(self.destination_ranges, self.source_ranges):
      while len(to_be_processed) > 0:
        offset = destination_range.start - source_range.start
        starts_equal, ends_equal, input_contains_map, map_contains_input, overlap_start, overlap_end = get_range_conditionals(source_range, to_be_processed[0])
        if (starts_equal and ends_equal) or input_contains_map or map_contains_input or overlap_start or overlap_end:
          overlapped_range = range(max(source_range.start, to_be_processed[0].start), min(source_range.stop, to_be_processed[0].stop))
          results.append(range(overlapped_range.start + offset, overlapped_range.stop + offset))
          if to_be_processed[0].start < source_range.start:
            to_be_processed.append(range(to_be_processed[0].start, source_range.start))
          if to_be_processed[0].stop > source_range.stop:
            to_be_processed.append(range(source_range.stop, to_be_processed[0].stop))
        else:
          results.append(to_be_processed[0])
          
        to_be_processed.pop(0)
# TODO Work out range comparison more thoroughly on paper before implementing this. I basically want to tell
# it to convert the whole thing if the ranges match, or just convert the portions that match while moving the 
# unmatched portions to the stack to be evaluated on the remaining source_ranges
def get_range_conditionals(map_range, input_range):
  starts_equal = map_range.start == input_range.start
  ends_equal = map_range.end == input_range.end
  input_contains_map = map_range.start >= input_range.start and map_range.end <= input_range.end
  map_contains_input = map_range.start <= input_range.start and map_range.end >= input_range.end
  overlap_start = map_range.start > input_range.start and map_range.end > input_range.end
  overlap_end = map_range.start < input_range.start and map_range.end < input_range.end
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
  
def get_seed_ranges(seed_nums):
  seed_ranges = []
  i = 0
  while i < len(seed_nums):
    seed_ranges.append(range(seed_nums[i], seed_nums[i+1]))
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

# refactor code to covert ranges instead of integers
with open('day-5-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  seed_nums = [int(seed) for seed in lines[0].split(': ')[1].split(' ')]
  seed_ranges = get_seed_ranges(seed_nums)
  all_map_data = extract_map_instructions(lines)
  
  
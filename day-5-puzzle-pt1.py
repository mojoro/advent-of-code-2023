class ConversionMap:
  def __init__(self, map_data):
    self.map_data = map_data

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
  
def get_nearest_location(seed_nums, all_map_data):
  conversion_pipe = ConversionPipe(all_map_data)
  location_nums = []
  for seed_num in seed_nums:
    location_nums.append(conversion_pipe.get_location(seed_num))
  return min(location_nums)

with open('day-5-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  seeds = [int(seed) for seed in lines[0].split(': ')[1].split(' ')]
  all_map_data = extract_map_instructions(lines)
  seed_to_soil_data, soil_to_fertilizer_data, fertilizer_to_water_data, water_to_light_data, light_to_temperature_data, temperature_to_humidity_data, humidity_to_location_data = all_map_data
  
  print(get_nearest_location(seeds, all_map_data))
  
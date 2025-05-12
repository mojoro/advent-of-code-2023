class CamelMap:
  def __init__(self, map):
    self.left = map.split('(')[1].split(', ')[0]
    self.right = map.split('(')[1].split(', ')[1][:3]
    self.key = map.split(' = ')[0]

def constructGraph(maps):
  graph = {}
  for map in maps:
    graph[map.split(' = ')[0]] = CamelMap(map)

  return graph

def navigateToEnd(instructions, graph, aMaps, zMaps):
  steps = 0
  currentMaps = aMaps
  destinationSet = set(zMaps)
  destinationReached = False
  directions = list(instructions)
  while not destinationReached:
    for direction in directions:
      nextMaps = []
      if direction == 'L':
        for map in currentMaps:
          nextMaps.append(graph[map].left)
        currentMaps = nextMaps
        steps += 1
      elif direction == 'R':
        for map in currentMaps:
          nextMaps.append(graph[map].right)
        currentMaps = nextMaps
        steps += 1
      if set(currentMaps) == destinationSet:
        destinationReached = True
        break
  return steps

def returnAMaps(maps):
  aMaps = []
  for map in maps:
    if map[2] == 'A':
      aMaps.append(CamelMap(map).key)
  
  return aMaps

def returnZMaps(maps):
  zMaps = []
  for map in maps:
    if map[2] == 'Z':
      zMaps.append(CamelMap(map).key)
  
  return zMaps

with open('day-8-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  instructions = lines[0]
  maps = lines[2:]
  graph = constructGraph(maps)
  aMaps = returnAMaps(maps)
  zMaps = returnZMaps(maps)
  steps = navigateToEnd(instructions, graph, aMaps, zMaps)
  print(steps)

  # collect all things ending with A. while they don't all end in Z, Navigate all according to their direction, counting steps.
  # evaluate if they all end in Z
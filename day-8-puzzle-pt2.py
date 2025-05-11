class CamelMap:
  def __init__(self, map):
    self.left = map.split('(')[1].split(', ')[0]
    self.right = map.split('(')[1].split(', ')[1][:3]

def constructGraph(maps):

  graph = {}
  for map in maps:
    graph[map.split(' = ')[0]] = CamelMap(map)

  return graph

def navigateToEnd(instructions, graph):
  steps = 0
  origin = 'AAA'
  currentLocation = origin
  destination = 'ZZZ'
  destinationReached = False
  directions = list(instructions)
  while not destinationReached:
    for direction in directions:
      if direction == 'L':
        currentLocation = graph[currentLocation].left
        steps += 1
      elif direction == 'R':
        currentLocation = graph[currentLocation].right
        steps += 1
      if currentLocation == destination:
        destinationReached = True
        break
  return steps




with open('day-8-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  instructions = lines[0]
  maps = lines[2:]
  graph = constructGraph(maps)
  steps = navigateToEnd(instructions, graph)
  print(steps)
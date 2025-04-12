class Hand:
  def __init__(self, cards, bid):
    self.cards = cards
    self.card_strengths = calculate_card_strengths(self.cards)
    self.type = self.calculate_type()
    self.bid = bid

  def __eq__(self, other):
    return (self.type == other.type and self.total_card_strength == other.total_card_strength and isinstance(other, Hand))
  
  def __lt__(self, other):
    if not isinstance(other, Hand):
      return NotImplemented
    if self.type != other.type:
      return self.type < other.type
    for strength1, strength2 in zip(self.card_strengths, other.card_strengths):
        if strength1 < strength2:
            return True
        elif strength1 > strength2:
            return False
    return False
  
  def __gt__(self, other):
    if not isinstance(other, Hand):
      return NotImplemented
    if self.type != other.type:
      return self.type > other.type
    for strength1, strength2 in zip(self.card_strengths, other.card_strengths):
        if strength1 > strength2:
            return True
        elif strength1 < strength2:
            return False
    return False
  
  def __le__(self, other):
    return self == other or self < other
  
  def __ge__(self, other):
    return self == other or self > other

  def __str__(self):
    return f'Cards: {self.cards}, Bid: {self.bid}, Type: {self.type}'
  
  # def calculate_total_card_strength(self):
  #   max_strength = 12
  #   total = 0
  #   for i, card_strength in enumerate(reversed(self.card_strengths), 2):
  #     if (i == 0): total += card_strength
  #     else: 
  #       slot_weight = 10**(i)
  #       slot_strength = slot_weight + card_strength*slot_weight
  #       total += slot_strength
  #   return total
  
  def calculate_type(self):
    wild_card = 'J'
    sorted_cards = sorted(self.cards)
    card_set = set(sorted_cards)
    if wild_card in card_set: card_set.remove(wild_card)
    matches = []
    for card in card_set:
      match = self.cards.count(card)
      if match > 1: matches.append(match + self.cards.count(wild_card))
    return self.__evaluate_matches(matches)
  
  # There must be a better way, but they are all quite unique, no?
  def __evaluate_matches(self, matches):
    # high-card
    if len(matches) == 0: return 0
    elif len(matches) == 1: 
      # 4-5 of a kind
      if matches[0] >= 4: return matches[0] + 1
      # 2 of a kind
      elif matches[0] == 2: return matches[0] - 1
      # 3 of a kind
      else: return matches[0]
    elif len(matches) == 2: 
      # full house
      if matches[0] == 3 or matches[1] == 3: return 4
      # 2 pair
      else: return 2
    else: raise ValueError('Invalid number of matches. 3 pairs or more is not possible in hands of five cards')


def calculate_card_strengths(cards):
  keys = list('J23456789TQKA')
  strength_list = list(range(0, 13))
  strength_map = dict(zip(keys, strength_list))
  strength_arr = []

  for card in cards:
    strength_arr.append(strength_map.get(card))

  return strength_arr

def get_total_winnings(hands):
  total = 0
  for rank, hand in enumerate(hands, 1):
    total += hand.bid * rank
  return total

with open('day-7-input.txt') as f:
  lines = [line for line in f.read().splitlines()]
  hands = [Hand(line.split(' ')[0], int(line.split(' ')[1])) for line in lines]
  hands.sort()
  for i, hand in enumerate(hands, 1):
    print(f'Rank: {i}, {hand}')
  print(get_total_winnings(hands))
  
    
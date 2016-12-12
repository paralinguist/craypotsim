import random
#seeding the random number generator is important in a sim!
random.seed()
#Starts with: 1 boat, 5 pots and no cash
#Each boat only has capacity for 10 pots
#Boats are $100, pots are $5
#        IN      OUT
#GOOD    $2      $8
#BAD     $4      LOST

#Constants - modify these in code to change the simulation parameters
NUM_SIMS = 1000
DAYS = 20
BOAT_COST = 100
BOAT_CAPACITY = 10
POT_COST = 5
IN_GOOD = 2
IN_BAD = 4
OUT_GOOD = 8
OUT_BAD = 0
GOOD_WEATHER = [1,2,3]
BAD_WEATHER = [5,6]
SAME_WEATHER = [4]

DIE_SIZE = len(GOOD_WEATHER) + len(BAD_WEATHER) + len(SAME_WEATHER)

def purchase_items(cash, pots, boats):
  if (cash >= BOAT_COST and pots//BOAT_CAPACITY > boats - 1):
    boats = boats + 1
    cash = cash - BOAT_COST
  while (pots//BOAT_CAPACITY < boats and cash >= POT_COST):
    pots = pots + 1
    cash = cash - POT_COST
    if (pots//BOAT_CAPACITY >= boats and cash >= BOAT_COST):
      boats = boats + 1
      cash = cash - BOAT_COST
  return cash, pots, boats

#Oh for a case statement
def place_pots(strategy, pots, last_weather):
  #Default strategy - probs not a winner!
  pots_in = 0
  pots_out = 0
  if ("thirds" == strategy):
    pots_out = pots // 3
    pots_in = pots - pots_out
  elif ("halves" == strategy):
    pots_out = pots // 2
    pots_in = pots - pots_out
  elif ("cautious" == strategy):
    if (last_weather in BAD_WEATHER):
      pots_out = pots // 5
      pots_in = pots - pots_out
    else:
      pots_out = pots // 2
      pots_in = pots - pots_out
  elif ("aggressive" == strategy):
    pots_out = pots - 1
    pots_in = pots - pots_out
  return pots_in, pots_out

def run_sim():
  #Initialise variables
  boats = 1
  pots = 5
  cash = 0
  pots_out = 0
  pots_in = 0
  last_weather = 1
  weather = 1
  for day in range(1, DAYS+1):
    cash, pots, boats = purchase_items(cash, pots, boats)
    #place pots based on chosen strategy - amend to include your own
    pots_in, pots_out = place_pots("aggressive", pots, last_weather)
    weather = random.randint(1, DIE_SIZE)
    if (weather in SAME_WEATHER):
      weather = last_weather
    last_weather = weather
    if (weather in GOOD_WEATHER):
      cash = cash + IN_GOOD * pots_in + OUT_GOOD * pots_out
    else:
      cash = cash + IN_BAD * pots_out + OUT_BAD * pots_out
      pots = pots - pots_out
  
  total_value = cash + pots*POT_COST + boats*BOAT_COST
  return total_value

total_value_sims = 0
for sim in range(0, NUM_SIMS):
  total_value_sims = run_sim() + total_value_sims
ave_value = total_value_sims / NUM_SIMS
print("Ave value: " + str(ave_value))

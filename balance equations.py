##from curses import wrapper
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

class Element:
    "Creates an element"

    def __init__(self, symbol, num = 1):
        self.name = symbol
        self.amount = num

    def draw(self):
        print(self.name, self.amount, end = '', sep = '')
##        stdscr.addstr("Pretty text", curses.color_pair(1))
##        stdscr.refresh()

##wrapper(Element.draw)

class Compound:
    "A collection of elements"
    elements = []

    def __init__(self, *elementTuple):
        for i in elementTuple:
            self.elements.append(i)
        self.amount = 1

    def draw(self):
        print(self.amount, '(', end = '', sep = '')
        for i in self.elements:
            i.draw()
        print(')')

##wrapper(Element.draw)


print("Welcome to Copeland's equation balancer! Enter your equation below (case sensitive, use \"->\" to seperate sides) (press q to quit):\n")
equation = input()

##equation = "C8H18 + O2 -> CO2 + H2O"
if(equation.size() == 1) and (equation.front().lower() == 'q'):
    abort("Goodbye.")

if not equation.front().isupper() or not equation.front().isalpha():
    abort("Invalid equation (first character is incorrect).")

# parse the equation


i = 0
it = 0
isRight = False
leftSide = Compound[]
rightSide = Compound[]

##while it < equation.size()
for it in equation:
    # ...\0... (you're at the end)
    if not it:
        break

    # ...+...
    elif(it == '+'):
      ++i
      ++it

    # ...CP... or ...C ... or ...C+...
    elif it.upper() and ((it + 1).upper() or (it + 1 == ' ') or (it + 1 == '+') or (it + 1 == '\0'))):
      if isRight:
        rightSide.append(Element(it))

      else:
        leftSide.append(Element(it))

      ++it

    # ...CoP...
    elif(it.upper() and (it + 1).lower() and (it + 2).upper()):
      if (isRight):
        rightSide.append(Element(it + (it + 1)))

      else:
        leftSide.append(Element(it + (it + 1)))

      it += 2

    # ...C6...
    elif(isupper(it) and isdigit(*(it + 1)) and not isdigit(*(it + 2))):
      if (isRight):
        rightSide(Element(tmp, it + 1))

      else:
        leftSide(Element(tmp, it + 1))

      it += 2

    # ...Cg6...
    elif(isupper(it) and islower(*(it + 1)) and isdigit(*(it + 2)) and not isdigit(*(it + 3))):
      if (isRight):
        rightSide(Element(it + (it + 1), it + 2))

      else:
        leftSide(Element(it + (it + 1), it + 2))

      it += 3

    # ...C12...
    elif(isupper(it) and isdigit(*(it + 1)) and isdigit(*(it + 2))):
      if (isRight):
        rightSide(Element(it, (it + 1) + (it + 2)))

      else:
        leftSide(Element(it, (it + 1) + (it + 2)))

      it += 3

    # ...Cg12...
    elif(isupper(it) and islower(*(it + 1)) and isdigit(*(it + 2)) and isdigit(*(it + 3))):
      if (isRight):
        rightSide(Element(it + (it + 1), (it + 2) + (it + 3)))

      else:
        rightSide(Element(it + (it + 1), (it + 2) + (it + 3)))

      it += 4

    #
    elif it == '(':
      abort("Hold up. I haven't finished that feature yet.")
      ++it

    #
    elif it == ')':
      abort("Hold up. I haven't finished that feature yet.")
      ++it

    # ...->...
    elif(it == '-') and (*(it + 1) == '>'):
      isRight = true
      it += 2

    # ... ...
    elif(it == ' '):
      ++it

    # ...6...
    elif(it.digit()):
      abort("Sorry, we haven't implemented that feature yet.")
      ++it

    # garbage
    else:
      print(it, "is here when it's not supposed to be\n")
      # abort("Unrecognized symbols in the equation!")
      break




  for(auto compounds:amountsLeft):
    if(compounds.size())
      # compounds.insert(compounds.begin(), 1)
    compounds.front() = 1

  for(auto compounds:amountsRight):
    if(compounds.size())
      # compounds.insert(compounds.begin(), 1)
    compounds.front() = 1


  # do math

  debug(amountsLeft)
  displayVectors(amountsLeft)
  debug(amountsRight)
  displayVectors(amountsRight)

  debug(\n\n\n)

  # loop through the left side, and if you see a match to the element you're looking at,
  #  get the lowest common multiple of the amounds of each of them, and assign the
  #  compound multiplier of the compound it's in to that lowest common multiple.

  # check all occurences of a given element on both sides, then set the multiplier of
  #  each compound it's in to the least common multiple of the 2 current multipliers
  for(int lc = 0 lc < elementsLeft.size() ++lc):
    for(int lce = 0 lce < elementsLeft[lc].size() ++lce):
      for(int rc = 0 rc < elementsRight.size() ++rc):
        for(int rce = 0 rce < elementsRight[rc].size() ++rce):
          if(elementsLeft[lc][lce] == elementsRight[rc][rce]):
            int tmp = lcm(amountsLeft[lc][lce], amountsRight[rc][rce])
            amountsLeft[lc].front()  = tmp
            amountsRight[rc].front() = tmp






  # then get the lowest common multiple of the compound multipliers
  vector<int> multipliers(64)
  for(auto current:amountsLeft)
    if(current.size())
      multipliers.push_back(current.front())

  for(auto current:amountsRight)
    if(current.size())
      multipliers.push_back(current.front())


  # ...and divide each by it
  int tmp = lcmAll(multipliers)
  for(auto adj:amountsLeft)
    if(adj.size())
      adj.front() = tmp / adj.front()

  for(auto adj:amountsRight)
    if(adj.size())
      adj.front() = tmp / adj.front()

  string ss

  # reconstruct the formula into something human readable again
  #  (deparse, if you will)

  debug(amountsLeft)
  displayVectors(amountsLeft)
  debug(amountsRight)
  displayVectors(amountsRight)

  for(int lc = 0 lc < elementsLeft.size() ++lc):
    if(amountsLeft[lc].size()):
      # if(amountsLeft[lc].front() != 1)
        ss += to_string(amountsLeft[lc].front())
        ss += '('

    for(int lce = 0 lce < elementsLeft[lc].size() ++lce):
      ss += elementsLeft[lc][lce]

      if(amountsLeft[lc][lce] != 1)
        ss += to_string(amountsLeft[lc][lce])

    if(elementsLeft[lc].size())
      ss += ") + "


  ss.erase(ss.end() - 3, ss.end())
  ss += " -> "

~flag~

for(int rc = 0 rc < elementsRight.size() ++rc):
  if(amountsRight[rc].size()):
    # if(amountsRight[rc].front() != 1)
      ss += to_string(amountsRight[rc].front())
      ss += '('

    for(int rce = 0 rce < elementsRight[rc].size() ++rce):
      ss += elementsRight[rc][rce]

      if(amountsRight[rc][rce] != 1)
        ss += to_string(amountsRight[rc][rce])

  if(elementsRight[rc].size())
    ss += ") + "



  ss.erase(ss.end() - 3, ss.end())
  cout << endl << ss << endl

  return 0


void abort(string error):
  cout << endl << error << endl
  exit(0)

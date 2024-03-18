import numpy as np

class smartRobot:
  def __init__(self, g, n, s, o, w):
    self.gamma = g
    self.noise = n
    self.states = s
    self.outBounds = o
    self.wall = w
    self.moves = [['.' for _ in range(len(s[0]))] for _ in range(len(s))]
    self.steps = [[[] for _ in range(len(s[0]))] for _ in range(len(s))]

  # Checks if a candidate state is valid and not out of bounds
  def is_valid_state(self, state):
    row, col = state
    r = len(self.states)
    c = len(self.states[0])
    return (
        0 <= row < r and
        0 <= col < c and
        state != self.wall
    )

  # Figures out candidate next states (s`) and put them in a list for each state (steps)
  def get_possible_actions(self):
    for i in range(len(self.states)):
      for j in range(len(self.states[0])):
        if (i, j) not in self.outBounds:
          actions = []
          if self.is_valid_state((i - 1, j)):
            actions.append('up') # up
          if self.is_valid_state((i + 1, j)):
            actions.append('down') # down
          if self.is_valid_state((i, j - 1)):
            actions.append('left') # left
          if self.is_valid_state((i, j + 1)):
            actions.append('right') # right
          self.steps[i][j] = actions

  # Calculates the next state's indices
  def s_dash(self, state, action):
    i, j = state
    action_map = {'up': (i - 1, j),
                  'down': (i + 1, j),
                  'left': (i, j - 1),
                  'right': (i, j + 1)}
    return action_map[action]

  def learn(self):
    self.get_possible_actions()
    for i in range(len(self.states)):
      for j in range(len(self.states[i])):
        state = (i, j)
        if state not in self.outBounds:
          actions = self.steps[i][j]
          if actions:
            div = len(actions) - 1 # number of ways to divide the noise upon
            # this loop calculates max(sum(Bellman's Equation for each candidate action))
            for action in actions:
              x, y = self.s_dash(state, action) # gets next state's index
              sum = (1 - self.noise) * self.gamma * self.states[x][y]
              for rest in actions:
                if rest != action:
                  l, m = self.s_dash(state, rest)
                  sum += (self.noise/div) * self.gamma * self.states[l][m]
              # a condition to check if the current summation of bellman
              # for this action is greater than the previous action
              if sum > self.states[i][j]:
                self.states[i][j] = sum
                self.moves[i][j] = action

  # prints the states in a formatted way
  def print_states(self):
    print('States:')
    width = 8
    for i in range(len(self.states)):
      for j in range(len(self.states[i])):
        if (i, j) == wall:
          print('w'.center(width), end='')
        else:
          print(f'{self.states[i][j]:.3f}'.center(width), end='')
      print()

  # prints the actions in a formattted way
  def print_actions(self):
    width = 8
    for i in range(len(self.moves)):
      for j in range(len(self.moves[i])):
        if (i, j) == self.wall:
          print('W'.center(width), end='')
        else:
          print(f'{self.moves[i][j]}'.center(width), end='')
      print()

# Initial rewards and other parameters (walls)
rows = 3
cols = 4
gamma = 0.9
noise = 0.2
states = np.zeros((rows, cols))
states[0][3] = 1
states[1][3] = -1
out = [(1, 1), (0, 3), (1, 3)]
wall = (1, 1)

myRobot = smartRobot(gamma, noise, states, out, wall)
for _ in range(1000):
  myRobot.learn()

myRobot.print_states()
print()
myRobot.print_actions()
print()

# debugging the process of `actions` in the class
for a, b in zip(myRobot.steps, range(len(myRobot.states))):
  for c, d in zip(a, range(len(myRobot.states[0]))):
    print(f"({b}, {d}) can move {c}", end=' => ')
    for som in c:
       print(f"{myRobot.s_dash((b, d), som)}", end=' ')
    print()
# Define constants
NSTATES = 3         # total number of states
NCHARS = 128        # assuming ASCII input
INITIAL = 0
ERROR = -1

# Transition table (state x char) -> next_state
# Initialize with ERROR (-1)
trans_table = [[ERROR for _ in range(NCHARS)] for _ in range(NSTATES)]

# Example transitions:
# State 0 (INITIAL): if letter -> 1, if digit -> 2
for c in range(ord('a'), ord('z') + 1):
    trans_table[INITIAL][c] = 1  # letters lead to state 1
for c in range(ord('0'), ord('9') + 1):
    trans_table[INITIAL][c] = 2  # digits lead to state 2

# In state 1 (IDENTIFIER): more letters or digits continue in 1
for c in range(ord('a'), ord('z') + 1):
    trans_table[1][c] = 1
for c in range(ord('0'), ord('9') + 1):
    trans_table[1][c] = 1

# In state 2 (NUMBER): more digits continue in 2
for c in range(ord('0'), ord('9') + 1):
    trans_table[2][c] = 2

# Define accept states (token types)
# None = not accepting, otherwise token name
accept_states = [None, "IDENTIFIER", "NUMBER"]

# Input text
text = "abc123"
state = INITIAL

# Process each character
for ch in text:
    c = ord(ch)
    if c >= NCHARS:  # ignore non-ASCII
        state = ERROR
        break
    state = trans_table[state][c]
    if state == ERROR:
        break

# Determine result
if state != ERROR and accept_states[state]:
    print("Accepted token:", accept_states[state])
else:
    print("Error: Invalid token")

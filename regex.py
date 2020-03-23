# Project implementation
# Creating an NFA using Thompsons Construction
# Darragh Lally

##############################################################

# Fragment class
class Fragment:
    # Start state of NFA frag
    start = None
    # Accept state of NFA frag
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

##############################################################

# State Class
class State:
    # Every state has n arrows coming from it (0-2)
    edges = []
    # Label for arrow
    label = None

    # Constructor
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label

##############################################################

# Shunting Yard Algorithm
def shunt(infix):
    # Convert input to a stackish list put on a list, in reverse order
    infix = list(infix)[::-1]
    # Operator Stack
    opers = []
    # Output list
    postfix = []
    # Operator presidence 
    prec = {'*':100, '+':90, '?':80, '.':70, '|':60, ')':40, '(':20 }

    # Loop through the input one char at a time
    while infix:
        # Pop a char from the input
        c = infix.pop() # Returns and removes last element
        if c == '(':
            # If its an open bracket push to opers stack
            opers.append(c)
        elif c == ')':
            # Pop the operators stack until you find an open bracket
            while opers[-1] != '(':
                postfix.append(opers.pop())
            # Get rid of the open bracket
            opers.pop()
        # Decide what to do based on the char
        elif c in prec:
            # Push any operators on the opers stack with higher preference to the output
            while opers and prec[c] < prec[opers[-1]]:
                postfix.append(opers.pop())
            # Push c to opers stack
            opers.append(c)
        else:
            # Typically, we just push the char to the output
            postfix.append(c)

    # Pop all operators to the output
    while opers:
        postfix.append(opers.pop())
    # Convert output list to string
    return ''.join(postfix)

##############################################################

def compile(infix):
    # First convert infix to postfix
    postfix = shunt(infix)
    # Parse postfix string into a list and reverse
    postfix = list(postfix)[::-1]
    # NFA stact
    nfa_stack = []
    
    while(postfix):
        # Pop a char from postfix
        c = postfix.pop()
        if c == '.':
            # Pop two fragments from NFA stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)
            # Create new fragment using frag2's start state and frag1's accept state
            newfrag = Fragment(frag2.start, frag1.accept)
        elif c == '|':
            # Pop two fragments from NFA stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Create new start and accept states
            start = State()
            accept = State(edges=[frag2.start, frag1.accept])
            # Point the old accept states to the new one
            frag2.accept.edges.append(accept)
            frag1.accept.edges.append(accept)
            # Create a new fragment
            newfrag = Fragment(start, accept)
        elif c == '+':
            # Binary operator - pop just one
            frag = nfa_stack.pop()
            # New start and accept states
            start = State()
            accept = State(edges=[accept, frag.start])
            # Point to the old
            frag.accept.edges = [frag.start, accept]
            # Create a new frag
            newfrag = Fragment(start, accept)
        #elif c == '?':
            #
        elif c == '*':
            # Pop just one fragment, Kleene star is a binary operator!
            frag = nfa_stack.pop()
            # Create new start and accept states
            start = State()
            accept = State(edges=[accept, frag.start])
            # Point to old accept states
            frag.accept.edges = [frag.start,accept]
            # Create new fragment
            newfrag = Fragment(start, accept)
        else:
            accept = State()
            start = State(label=c, edges=[accept])
            #create a new fragment with initial and accept
            newfrag = Fragment(start, accept)
        
        # Push new fragment to the NFA stack
        nfa_stack.append(newfrag)

    # NFA stack should have exactly one NFA
    return nfa_stack.pop()

##############################################################

# Function to follow epsilon arrows
# Add state to set, and follow all of the 'e' arrows
def followepsilon(state, current):
    # Only do when we haven't already seen the state
    if state not in current:
        # Put state into current
        current.add(state)
        # See whether state is labelled by 'e'
        if state.label is None:
            # Loop through states pointed to by 'this'
            for x in state.edges:
                # Follow all their 'e' too - this form of recursion is not 
                # is not advised
                followepsilon(x, current)

##############################################################

# Function to return true if the regular expression 'regex'
# matches the string 's'
def match(regex, s):
    # Compile regex into NFA
    nfa = compile(regex)
    # Current set of states
    current = set()
    # Add first state, and follow all 'e' arrows
    followepsilon(nfa.start, current)
    # Previous set of states
    previous = set()
    # Loop through char's of 's'
    for c in s: 
        # Keep track of where we were
        previous = current
        # Create a new empty set for states we will soon be in
        current = set()
        # Loop through previous states
        for state in previous:
            # Only follow arrows not labeled by E - epsilon
            if state.label is not None:
                # If the label of the state is == to char
                if state.label == c:
                    # Add state at the end of the arrow to current
                    followepsilon(state.edges[0], current)
    
    # Only one accept state, if we are there, return true!
    return nfa.accept in current

##############################################################

# Testing match()
# print(match("a.b|b*", "xbbbbbbbbbbbb"))
# print(match("a.b", "ab"))
# print(match("a|b", "b")) # not working????
print(match("a.b|b*", "a"))


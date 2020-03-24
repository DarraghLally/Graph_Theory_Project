# Graph Theory Project implementation
# Creating an NFA using Thompsons Construction
# Darragh Lally - G00220290

##############################################################

class Fragment:
    """An NFA fragment, with a start and accept state"""
    # Constructor
    def __init__(self, start, accept):
        # Start state of NFA
        self.start = start  
        # Accept state of NFA
        self.accept = accept

##############################################################

class State:
    """A State with labelled edges"""
    # Constructor
    def __init__(self, label=None, edges=[]):
        # Each state has 0-2 edges
        self.edges = edges
        # Each edge is labelled
        self.label = label

##############################################################

def shunt(infix):
    """shunt

    Shunting Yard Algorithm to parse and return regex in postfix notation 
    """
    # Convert input to a stack, in reverse order
    infix = list(infix)[::-1]
    # Operator Stack
    opers = []
    # Postfix regex
    postfix = []
    # Operator presidence 
    prec = {'*':100, '+':100, '?':100, '.':70, '|':60, ')':40, '(':40 }

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
            # Push operators on the opers stack with higher pref to output
            while opers and prec[c] < prec[opers[-1]]:
                postfix.append(opers.pop())
            # Push c to opers stack
            opers.append(c)
        else:
            # Typically, we just push the char to the output
            postfix.append(c)

    while opers:
        # Pop all operators to the output
        postfix.append(opers.pop())

    # Convert output list to string
    return ''.join(postfix)

##############################################################

def compile(infix):
    """compile
    
    Function that returns an NFA fragment that represents the infix regex    
    """
    # First convert infix to postfix
    postfix = shunt(infix)
    # Parse postfix string into a stack
    postfix = list(postfix)[::-1]
    # NFA fragment stact
    nfa_stack = []
    
    while(postfix):
        # Pop a char from postfix
        c = postfix.pop()

        # Concatenation
        if c == '.':
            # Pop two fragments from NFA stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()  
            # Point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)
            # New start state
            start = frag2.start
            # New accept state
            accept = frag1.accept 
            # Point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)

        # Alternation
        elif c == '|':
            # Pop two fragments from NFA stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State(edges=[frag2.start, frag1.start])
            # Point the old accept states to the new one
            frag2.accept.edges.append(accept)
            frag1.accept.edges.append(accept)            

        # Any number of, incl. zero
        elif c == '*':
            # Pop just one fragment, Kleene star is a binary operator!
            frag = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])
            # Point to old accept states
            frag.accept.edges = [frag.start, accept]
        
        # I have referenced material in the project README as to
        # where I have researched the + and % operators

        # One or more
        elif c == '+':
            # Binary operator, pop just one
            frag = nfa_stack.pop()
            # New start and accept states
            accept = State()            
            start = frag.start
            # Point to the old
            frag.accept.edges = [start, accept]

        # Zero or One
        elif c == '?':
            # Binary operator, pop one
            frag = nfa_stack.pop()
            # New start and accept
            accept = State()
            start = State(edges=[frag.start, accept])
            # Point to the old
            frag.accept.edges = [accept, accept]
        else:
            accept = State()
            start = State(label=c, edges=[accept])
        #Create a new fragment
        newfrag = Fragment(start, accept)
        # Push new fragment to the NFA stack
        nfa_stack.append(newfrag)

    # NFA stack should have exactly one NFA
    return nfa_stack.pop()

##############################################################

def followepsilon(state, current):
    """followepsilon
    
    A function to follow any e(psilon) edges
    """
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

def match(regex, s):
    """match

    A function that returns True if regular expression
    (regex) matchs the string (s)
    """
    # Compile regex into NFA
    nfa = compile(regex)
    # Current set of states
    current = set()
    # Add first state, and follow all 'e' arrows
    followepsilon(nfa.start, current)
    # Previous set of states
    previous = set()

    for c in s: 
        # Keep track of where we were
        previous = current
        # Create a new empty set for states we will soon be in
        current = set()

        for state in previous:
            # Only follow arrows not labelled by E, epsilon
            if state.label is not None:
                # If label of the state is == to char
                if state.label == c:
                    # Add state at the end of the edge to current
                    followepsilon(state.edges[0], current)
    
    # Only one accept state, if we are there, return true!
    return nfa.accept in current

##############################################################

# Testing

# Will only run if this is ran as its own script
# if calling from another script these tests will not be ran
if __name__ == "__main__":
    # An array of tests
    tests = [
        ["a.b|b*", "bbbbb", True],
        ["a.b|b*", "bbbbbx", False],
        
        ["a.b", "ab", True], 
        ["a.b", "c", False], 
        
        ["b*", "", True],
        ["b**", "bbbbbb", True],

        ["b+", "bbb", True],
        ["b+", "", False],

        ["c?", "", True],
        ["c?", "aa", False],

        ["c|a", "c", True],
        ["c|a", "b", False]

    ]
    for test in tests:
        assert match(test[0], test[1]) == test[2], test[0] + " should match " if test[2] else " should not match " + test[1]

##############################################################

# Console args

# Get regex, print to verify
regex = raw_input("Enter regex: ")
print(regex)

# Get string, print to verify
inputstring = raw_input("Enter string: ")
print(inputstring)

# Pass into 'answer'
answer = match(regex, inputstring)

# Output result
if(answer):
    print("Accepted")
else:
    print("Not Accepted")

# Project implementation
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

# Testing block

# myInstance = State(label='a', edges=[])
# myOtherInstance = State(edges=[myInstance])
# print(myInstance.label)
# print(myOtherInstance.edges[0])

#End testing block

##############################################################

# Shunting Yard Algorithm
def shunt(infix):

# Below block used for testing...
    
    # Convert 'infix' to a stack list
    # infix = "(a|b).c*"
    # print("Input: (a|b).c*")
    # Expected output: ab|c*.
    # print("Expect: ", "ab|c*")

# End testing block

    # Convert input to a stackish list put on a list, in reverse order
    infix = list(infix)[::-1]

    # Operator Stack
    opers = []

    # Output list
    postfix = []

    # Operator presidence - add + operator in future
    prec = {'*':100, '.':80, '|':60, ')':40, '(':20}

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
    postfix = ''.join(postfix)

##############################################################

def regex_compile(infix):
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
            frag2.edges.append(accept)
            frag1.edges.append(accept)
            # Create a new fragment
            newfrag = Fragment(start, accept)
        #elif c == '+':
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
            start = State(label=c, edges=[accept])
            accept = State()
            #create a new fragment with initial and accept
            newfrag = Fragment(start, accept)
        
        # Push new fragment to the NFA stack
        nfa_stact.append(newfrag)

    # NFA stack should have exactly one NFA
    return nfa_stack.pop()

##############################################################

# Function to return true if the regular expression 'regex'
# matches the string 's'
def match(regex, s):
    # Compile regex into NFA
    nfa = regex_compile(regex)
    return nfa

##############################################################

# Testing match()
print(match("a.b|b*", "ab"))
















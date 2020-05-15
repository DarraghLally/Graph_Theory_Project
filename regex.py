# Graph Theory Project implementation
# Creating an NFA using Thompsons Construction
# Darragh Lally - G00220290


##############################################################

# Import for command line arguments
import argparse
# Import for testing
import unittest

##############################################################

# Command Line Arguments

parser = argparse.ArgumentParser(description="Python NFA Machine. The purpose of this project is to determine if a given string will be accepted by a given regular expression")
parser.add_argument('String', metavar='inputstring', type=str,
        help='String to be tested through the NFA')
parser.add_argument('Regular Expression', metavar='regex', type=str,
        help='The regular expression used to create the NFA')

args = parser.parse_args()
print(args.accumulate(args.String))
##############################################################

class AutoTesting(unittest.TestCase):
    """Class AutoTesting
    
    Main menu option to run automated testing with hard-coded
    values for both the regular expression and string for testing.
    """
    def test_and_or(self):
        self.assertTrue(match("a.b|b*", "bbbbb"))
        self.assertFalse(match("a.b|b*", "bbbbbn"))

    def test_and(self):
        self.assertTrue(match("a.b", "ab"))
        self.assertFalse(match("a.b", "c"))

    def test_or(self):
        self.assertTrue(match("c|a", "c"))
        self.assertFalse(match("c|a", "b"))

    def test_any_num(self):
        self.assertTrue(match("b*", ""))
        self.assertFalse(match("b**", "bbbbbbn"))

    def test_one_more(self):
        self.assertTrue(match("b+", "bbb"))
        self.assertFalse(match("b+", ""))

    def test_zero_one(self):
        self.assertTrue(match("c?", ""))
        self.assertFalse(match("c?", "aa"))

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
    def __init__(self, label=None, edges=None):
        # Each state has 0-2 edges
        self.edges = edges if edges else []
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
            #frag2.accept.edges.append(accept)
            #frag1.accept.edges.append(accept)            
            frag2.accept.edges = [accept]
            frag1.accept.edges = [accept]
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

def consoleinput():
    """consoleinput
    
    A simple function used when asking for user input from
    the console. 
    """

    # Get regex, print to verify
    regex = raw_input("Enter regex: ")
    print(regex)

    # Get string, print to verify
    inputstring = raw_input("Enter string: ")
    print(inputstring)

    # Pass args into match() and save into 'answer'
    answer = match(regex, inputstring)

    # Output appropriate result, depending on boolean 
    # returned from match()
    if(answer):
        print("The string " + inputstring + " IS accepted by the regular expression " + regex)
    else:
        print("The string " + inputstring + " IS NOT accepted by the regular expression " + regex)


##############################################################

def keepgoing():
    """keepgoing
    
    Function called to ask if user wants
    to continue.
    """
    # User asked if they would like to continue
    keeprunning = raw_input("Keep Going? y/n")

    while(keeprunning == "y"):
        # Call function again so user can input new data
        consoleinput()
        # Exit/re-run clause
        keeprunning = raw_input("Keep Going? y/n")
        print()

##############################################################

# Function ran first, asking user for regex and string
#consoleinput()
# Continue?
#keepgoing()
        
##############################################################

# Testing

# Will only run if this is ran as its own script
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

print
print("Welcome to a Python driven, NFA Machine")
print
print("Enter 1 for Manual Argument Entry")
print("Enter 2 for Automated Testing")
print("Enter 3 to Exit")
print

menuchoice = raw_input("Choose 1, 2 or 3")
while(menuchoice!="3"):
    if menuchoice == "1":
        consoleinput()
        keepgoing()
    elif menuchoice == "2":
        unittest.main()
    else:
        print("Incorrect Input")

    print
    print("Enter 1 for Manual Argument Entry")
    print("Enter 2 for Automated Testing")
    print("Enter 3 to Exit")
    print
    menuchoice = raw_input("Choose 1, 2 or 3")
    print

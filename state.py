# State class used in Thompsons Construction 
# Darragh Lally

class State:
    # Every state has n arrows coming from it (0-2)
    edges = []

    # Label for arrow
    label = None

    # Constructor
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label

myInstance = State(label='a', edges=[])
myOtherInstance = State(edges=[myInstance])

print(myInstance.label)
print(myOtherInstance.edges[0])


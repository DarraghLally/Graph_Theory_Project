# Fragment class for use in Thompsons Construction
# Darragh Lally

class Frag:
    # Start state of NFA frag
    start = None
    # Accept state of NFA frag
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

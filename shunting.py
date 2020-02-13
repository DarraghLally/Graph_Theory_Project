# Darragh Lally - G00220290
# Shunting Yard Algo

# input
infix = "(a|b).c*"
print("Imput is: ", infix)

# Expected output: ab|c*.
print("Expect: ", "ab|c*")

# Convert input to a stackish list
#   put on a list, in reverse order
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
    c = infix.pop() # returns and removes last element
    if c == '(':
        # if its an open bracket push to opers stack
        opers.append(c)
    elif c == ')':
        # pop the operators stack until you find an open bracket
        while opers[-1] != '(':
            postfix.append(opers.pop())
        # get rid of the open bracket
        opers.pop()
    # Decide what to do based on the char
    elif c in prec:
       # push any operators on the opers stack with higher preference to the output
       while opers and prec[c] < prec[opers[-1]]:
            postfix.append(opers.push())
        # Do something here, push c to opers stack
       opers.append(c)
    else:
        # Typically, we just push the char to the output
        postfix.append(c)

# Pop all operators to the output
while opers:
    postfix.append(opers.pop())

# Convert output list to string
postfix = ''.join(postfix)

# Print result
print("Result is: ", postfix)

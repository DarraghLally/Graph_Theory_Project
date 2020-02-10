# Graph_Theory_Project
by Darragh Lally - G00220290

**Thompson's Construction:** 
Is to construct an NFA from a regular expression

**REGEX operators:**
| -> or
. -> concat
* -> any number (including zero)
+ -> one or more, similar to * but does not include zero

**Shunting Yard Algorithm:**
Turns infix to postfix

Infix -> a.b , a|b , a* , a+b
Postfix -> ab. , ab| , a* , ab+

**Stack**
Take the following example: 4+5*2 (infix), 452*+ (postfix)

1. push 4 to stack - 4
2. push 5 to stack - 4,5
3. push 2 to stack - 4,5,2
4. meet first operator, pop last two from stack and operate - 5*2 - 4
5. push 10 to stack - 4,10
6. meet next operator, pop last two from stack and operate - 4+10 - blank
7. push 14 to stack. - 14
8. Answer found


**Reference links:**
https://www.cs.york.ac.uk/fp/lsa/lectures/REToC.pdf
https://www.tutorialspoint.com/automata_theory/constructing_fa_from_re.htm

**Creating a DFA from a regular expression (Regex).**
https://cs.stackexchange.com/questions/40819/how-to-create-dfa-from-regular-expression-without-using-nfa


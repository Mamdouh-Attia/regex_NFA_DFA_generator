#This file has old removed code for later reference
# Utility functions
# -----------------
def preprocess_regex(regex):
    """
    Preprocess the regex to add the missing '.' operators
    """
    check1_list = ['*', '+', '?', ')', ']']
    new_regex = ''
    for i,c in enumerate(regex):
        if i > 0 and c in check1_list and i+1 < len(regex) and regex[i+1] not in check1_list:
            new_regex += c + '.'
        elif c in alphanumeric and i+1 < len(regex) and ((regex[i+1] in alphanumeric) or regex[i+1] in ['(', '[']):
            new_regex += c + '.'
        else:
            new_regex += c
    return new_regex

# Test the function
print(preprocess_regex('AB'))
print(preprocess_regex('A(B|C)'))
print(preprocess_regex('A(B|C)*'))

def infix_to_postfix(regex):
    """
    Convert an infix regular expression to a postfix regular expression.

    Parameters:
    regex (str): The infix regular expression to convert to postfix.

    Returns:
    str: The postfix regular expression.
    """
    regex = preprocess_regex(regex)
    # Create a stack to hold the operators
    stack = []
    # Create a list to hold the postfix regular expression
    postfix = []
    square_brackets_open = False
    # Iterate over the characters in the infix regular expression
    for index,char in enumerate(regex):
        #1. '(' or '[': Push it onto the stack
        if char == '(' or char == '[':
            stack.append(char)
            square_brackets_open = True if char == '[' else False
        #2. ')' or ']': Pop operators from the stack and append them to the postfix list until '(' or '[' is found
        elif char == ')' :
            while stack[-1] != '(':
                postfix.append(stack.pop())
            #error handling : check empty stack
            if not stack:
                raise ValueError('Parentheses mismatch : found ")" in the stack without "("')
            stack.pop()
        elif char == ']':
            while stack[-1] != '[':
                postfix.append(stack.pop())
            #error handling : check empty stack
            if not stack:
                raise ValueError('Parentheses mismatch : found "]" in the stack without "["')
            stack.pop()
            square_brackets_open = False
        #3. Operator: Pop operators from the stack and append them to the postfix list until an operator with lower precedence is found
        elif char in regex_operators_precedence:
            #checks:
            # 1. if the stack is not empty
            # 2. if the stack[-1] is an operator => meaning the last element in the stack is an operator
            # 3. if the precedence of the operator in the stack is greater than or equal to the precedence of the current operator
            #examples :
            # 1. stack = ['*', '+'], char = '?' => stack[-1] = '+', precedence('+') = 4, precedence('?') = 3
            while stack and stack[-1] in regex_operators_precedence and regex_operators_precedence[stack[-1]] >= regex_operators_precedence[char]:
                postfix.append(stack.pop())
            stack.append(char)

        #4. TODO : Handing Ranges
        elif char == '-':

            #pop the last element from the stack
            last_element = postfix.pop() if last_element in alphanumeric else None
            if not last_element:
                raise ValueError('Range error: element after - is not alphanumeric')
            #access Char + 1
            first_element = regex[index + 1]
            #throw the - operator from the regex
            operating_list = []
            for i in alphanumeric:
                if ord(i) > ord(last_element) and ord(i) < ord(first_element):
                    operating_list.append(i)
                    #append | between the characters
                    if i != first_element:
                        operating_list.append('|')
            #replace - in regex with the operating list
            regex = regex.replace(last_element + '-' + first_element, ''.join(operating_list))
        #else: Append the character to the postfix list
        else:
            # A normal character => append it to the postfix list
            postfix.append(char)
            if square_brackets_open:
                postfix.append('|') # add an OR operator => '|' between the characters in the square brackets
        # empty the stack
    while stack:
        #error handling : check '(' in the stack
        if stack[-1] == '(':
            raise ValueError('Parentheses mismatch : found "(" in the stack without ")"')
        postfix.append(stack.pop())
    return ''.join(postfix)


# test cases
# ----------
def test (id,regex, expected_postfix):
    assert infix_to_postfix(regex) == expected_postfix
    print(f"Test case #{id} : {regex} expected : {expected_postfix} => Passed")

test(1,'a+b*c', 'a+b*.c.')
test(2,'a+b*c?', 'a+b*.c.?')




print('All test cases passed!')
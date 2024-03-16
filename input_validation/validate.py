#This file is responsible for validating the input regex to the regex engine
#no libraries are used in this file


#The required language for the regex is defined as follows:
#converting to set for faster lookup
regex_language = set([
    #alphabet
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z",
    #numbers
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    #supported special characters:
    # . - any character
    # * - zero or more of the preceding character
    # + - one or more of the preceding character
    # ? - zero or one of the preceding character
    # | - or
    # ( - start of group
    # ) - end of group
    # [ - start of character class
    # ] - end of character class
    ".", "*", "+", "?", "|", "(", ")", "[", "]", "-"
])

some_invalid_combinations = set([
    "**", "++", "??", "||", "--" ,
])

def check_parentheses(regex):
    stack = []
    bracket_flag = False
    for char in regex:
        if char == "[":
            bracket_flag = True
        elif char == "]":
            bracket_flag = False
        if not bracket_flag:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if len(stack) == 0:
                    return False
                stack.pop()
    if len(stack) == 0:
        return True
    else:
        return False
    
def check_brackets(regex):
    stack = []
    for char in regex:
        if char == "[":
            stack.append(char)
        elif char == "]":
            if len(stack) == 0:
                return False
            stack.pop()
    if len(stack) == 0:
        return True
    else:
        return False
    
def check_valid_brackets_parentheses(regex):
    stack = []
    for char in regex:
        if char == "(" or char == "[":
            stack.append(char)
        elif char == ")" or char == "]":
            if len(stack) == 0:
                return False
            if char == ")" and stack[-1] == "[":
                return False
            if char == "]" and stack[-1] == "(":
                return False
            stack.pop()
    if len(stack) == 0:
        return True
    else:
        return False
    

def validate_input(regex):
    """
    
    """
    
    #1. check if the input is not empty
    if regex == "":
        return False
    #2. check if the input contains only the defined language
    for char in regex:
        if char not in regex_language:
            return False
    #3. check if the input is a valid regex
    
    #3.1. check if the input has balanced parentheses
    if not check_parentheses(regex):
        return False
    #3.2. check if the input has balanced brackets
    if not check_brackets(regex):
        return False
    #3.3. corner case: [(a]b) is not a valid regex
    # if not check_valid_brackets_parentheses(regex):
    #     return False
    for i in some_invalid_combinations:
        if i in regex:
            return False
    if regex[0] == '|' or regex[-1] == '|':
        return False
    #3.4 check that or is not the first or last character
    return True




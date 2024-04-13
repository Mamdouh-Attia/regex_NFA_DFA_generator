from validate import validate_input

def test_basic_syntax():
    assert validate_input("") == False  # Empty regex
    assert validate_input("abc123") == True  # Valid regex with alphanumeric characters
    assert validate_input(".") == True  # '.' is a valid regex
    assert validate_input("*") == True  # '*' is a valid regex

def test_parentheses_and_brackets():
    assert validate_input("()") == True  # Balanced parentheses
    assert validate_input("(a(b[c)d]e)f") == False  # Unbalanced brackets
    assert validate_input("[abc]") == True  # Balanced brackets

def test_character_classes():
    assert validate_input("[a-z0-9]") == True  # Valid character class
    assert validate_input("[a-z") == False  # Unbalanced character class
    assert validate_input("[a[bc]d]") == True

def test_quantifiers():
    assert validate_input("a*") == True  # Valid quantifier
    assert validate_input("b+") == True  # Valid quantifier
    assert validate_input("c?") == True  # Valid quantifier
    assert validate_input("**") == False  # Invalid use of quantifier

def test_alternation():
    assert validate_input("a|b") == True  # Valid alternation
    assert validate_input("(a|b)") == True  # Valid alternation with grouping
    assert validate_input("|") == False  # Invalid alternation

def test_grouping():
    assert validate_input("(ab)") == True  # Valid grouping
    assert validate_input("((a|b)c)") == True  # Valid nested grouping
    assert validate_input("()") == True  # Empty grouping

def test_combinations():
    assert validate_input("a|b*") == True  # Combination of alternation and quantifier
    assert validate_input("(a[b])?") == True  # Combination of grouping and quantifier
    assert validate_input("[a(b|c]*d+") == True  # Combination of character class, grouping, and quantifiers

def test_boundaries():
    assert validate_input("a") == True  # Single character
    assert validate_input("(a)") == True  # Single character with grouping
    assert validate_input(".") == True  # Any character
    assert validate_input("(a|)") == True  # Alternation with empty string
    assert validate_input("x" * 10000) == True  # Large string

# Run all test cases
test_basic_syntax()
test_parentheses_and_brackets()
test_character_classes()
test_quantifiers()
test_alternation()
test_grouping()
test_combinations()
test_boundaries()

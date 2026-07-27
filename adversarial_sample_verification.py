"""
Rule checkers for the RQ3 adversarial-transformation study.

Each ``check_rule_N`` decides whether an LLM-produced adversarial sample really
applied transformation rule N to the original snippet (and only that
transformation). The rules correspond one-to-one with the prompts in
``Prompts/{0..27}.txt``; the unit tests in ``adversarial-rule-unit-tests/``
exercise them against hand-written positive and negative examples.

This module holds the checking logic only. The batch driver that applies it to
``adversarial_samples_GPT4_accepted.csv`` lives in
``verify-adversarial-samples.py``.

Splitting the two is what makes the unit tests runnable: they all do
``from adversarial_sample_verification import *``, which previously matched no
importable module (the code lived in a hyphenated filename that also read a CSV
at import time).
"""

import re
from pathlib import Path

import pandas as pd

from tree_sitter_grammars import get_parser

REPO_ROOT = Path(__file__).resolve().parent


def find_identifiers(node):
    identifiers = []

    def traverse(node):
        for child in node.children:
            if child.type == 'identifier':
                # child.text is a byte string, so decode it
                identifiers.append(child.text.decode('utf-8'))

        # Recurse through children
        for child in node.children:
            traverse(child)
    traverse(node)
    return identifiers

# get_parser is imported from tree_sitter_grammars, which resolves compiled
# grammars via TREE_SITTER_SO_DIR and accepts every language spelling used in
# this repo ('cpp'/'c++', 'csharp'/'c#', ...). It is re-exported here because
# the unit tests import this module with `from ... import *`.

def parse_code(code, language):
    """ Parses code into an AST using Tree-sitter. """
    parser = get_parser(language)
    tree = parser.parse(bytes(code, "utf8"))
    return tree.root_node

def traverse(node, types):
    """
    Recursively traverses the AST and collects unique node types.
    Args:
        node: The current node in the AST.
        types: A set to store unique node types.
    """
    if node.type not in ['block_comment', 'line_comment', 'comment']:
        types.add(node.type)
    for child in node.children:
        traverse(child, types)

def find_code_snippet(location):
    """
    Resolve a 'LeetCode_<fold>_<sample_id>' location back to its source snippet.

    Anchored at the repository root rather than the caller's cwd, so the
    verifier works whether it is invoked from the root or from a model
    directory.
    """
    _, fold, sample_id = location.split('_')
    sample_df = pd.read_csv(REPO_ROOT / "LeetCode" / "data" / f"fold_{fold}_test.csv")
    sample_df = sample_df[sample_df['sample_id'] == int(sample_id)]
    return sample_df['code'].values[0]

def extract_python_docstrings(code):
    # Regex pattern for triple-quoted docstrings
    docstring_pattern = r"['\"]{3}([\s\S]*?)['\"]{3}"

    # Find all docstrings
    docstrings = re.findall(docstring_pattern, code)

    return docstrings

def parse_comments(code, language):
    tree = parse_code(code, language)
    comments = []
    
    def traverse(node):
        if node.type in ['block_comment', 'line_comment', 'comment']:
            comments.append(node.text.decode("utf-8", errors="replace"))
        for child in node.children:
            traverse(child)
    traverse(tree)
    
    if language == 'python':
        docstrings = extract_python_docstrings(code)
        comments.extend(docstrings)
    
    return comments

def check_comments(node):
    if node.type in ['block_comment', 'line_comment', 'comment']:
        return True
    for child in node.children:
        if check_comments(child):
            return True
    return False

def contains_comments(code, language):
    if language == 'python':
         comment_pattern = r'(#[^\n]*|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')'
         return bool(re.search(comment_pattern, code))
    else:
        tree = parse_code(code, language)
        
        return check_comments(tree)

def extract_comparisons_as_strings(root) -> list:
    """
    Traverse a Python parse tree (e.g. from tree-sitter) and return
    a list of the text for each individual comparison expression,
    e.g. "None != l1" or "value == x".
    """
    comparisons = []
    
    def traverse(node):
        # If this node is a 'comparison' node, let's capture its text.
        # Tree-sitter often lumps chained comparisons into a single 'comparison' node;
        # e.g. "a < b < c" is one node. You may need to break it up further.
        if node.type in ['comparison_operator', 'conditional', 'unary', 'ternary', 'binary', 'ternary_expression', 'binary_expression', 'unary_expression', 'parenthesized_expression', 'not_operator', 'binary_operator', 'if_statement', 'expression_statement']:
            # In many cases, "a < b < c" is a single node with multiple children.
            # If you want to handle each piece individually, you can look at the
            # child operators. For now, let's just store the entire text:
            node_text = re.sub(r"\s+", "", node.text.decode('utf-8'))
            comparisons.append(node_text)

        # Recurse into children
        for child in node.children:
            traverse(child)

    traverse(root)
    return comparisons

def extract_variable_declarations(root) -> list:
    """
    Extract variable declarations in the order they appear.
    """
    variable_declarations = []

    def traverse(node):
        # Check if node is a variable declaration
        if node.type in ['variable_declaration', 'parameter_declaration', 'variable_declarator', 'init_declarator', 'assignment_expression', 'local_variable_declaration',  'field_declaration', 'local_declaration_statement', 'expression_statement', 'declaration', 'assignment']:
            for child in node.children:
                child_text = re.sub(r"\s+", "", child.text.decode('utf-8'))
                variable_declarations.append(child_text)

        # Recurse
        for child in node.children:
            traverse(child)

    traverse(root)
    return variable_declarations

def extract_assignments_as_strings(root) -> list:
    """
    Traverse a Python parse tree (e.g. from tree-sitter) and return
    a list of the text for each individual assignment expression,
    e.g. "x = 1" or "l1 = None".
    """
    assignments = []
    
    def traverse(node):
        # If this node is an 'assignment' node, let's capture its text.
        if node.type in ('assignment', 'declaration', 'expression_statement', 'assignment_expression', 'update_expression', 'local_variable_declaration', 'field_access', 'parenthesized_expression', 'binary_expression', 'augmented_assignment', 'if_statement', 'integer', 'local_declaration_statement', 'return_statement', 'field_declaration', 'prefix_unary_expression', "++","--", "+=", "-="):
            
            node_text = re.sub(r"\s+", "", node.text.decode('utf-8'))
            assignments.append(node_text)

        # Recurse into children
        for child in node.children:
            traverse(child)
    traverse(root)
    return assignments

def find_all_if_else_statements(root):
    """
    Traverse the AST and return a list of all 'if-else' statements.
    """
    if_else_statements = []

    def traverse(node):
        # Check if this node is an 'if_statement' or 'if'
        if node.type in ['if_statement', 'if', 'conditional_expression', 'conditional', 'ternary_expression']:
            node_text = re.sub(r"\s+", "", node.text.decode('utf-8'))
            if_else_statements.append(node_text)

        # Recurse into children
        for child in node.children:
            traverse(child)

    traverse(root)
    return if_else_statements

def find_all_function_invocations(root):
    """
    Traverse the AST and return a list of all function invocations.
    """
    function_invocations = []

    def traverse(node):
        # Check if this node is a 'function_invocation'
        if node.type in ['function_invocation', 'call_expression', 'method_invocation', 'method_call', 'call', 'method_call_expression', 'function_call', 'function_declaration', 'parameters', 'formal_parameter', 'argument_list','parameter_list', 'method_parameters']:
            node_text = re.sub(r"\s+", "", node.text.decode('utf-8'))
            function_invocations.append(node_text)

        # Recurse into children
        for child in node.children:
            traverse(child)

    traverse(root)
    return function_invocations

def are_comments_equal(original_code, adversarial_code, language):
    original_comments = parse_comments(original_code, language)
    adversarial_comments = parse_comments(adversarial_code, language)
    
    original_comments = [re.sub(r"\s+", "", comment) for comment in original_comments]
    adversarial_comments = [re.sub(r"\s+", "", comment) for comment in adversarial_comments]
    
    return set(original_comments) == set(adversarial_comments)

def check_rule_0(original_code, adversarial_code, language):
    
    """
    Transformation: Remove all comments.
    Verification: Check if the original code has comments and the adversarial code does not.
    """

    original_has_comments = contains_comments(original_code, language)
    
    adversarial_has_comments = contains_comments(adversarial_code, language)

    return original_has_comments and not adversarial_has_comments

def check_rule_1(original_code, adversarial_code, language):
    
    """
    Transformation: Remove unused code including variables, functions, classes.
    Verification: Check if the types of nodes have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_types = set()
    traverse(tree1, original_types)
    
    adversarial_types = set()
    
    traverse(tree2, adversarial_types)
        
    if len(original_types - adversarial_types) > 0 and len(adversarial_types - original_types) == 0:
        return True
    else:
        return False
    
def check_rule_2(original_code, adversarial_code, language):
    """
    Transformation: Add print/log statements at every point where a variable is initialized or its value modified.
    Verification: Check if the number of print/log statements has increased.
    """
    
    keywords = ['print', 'log', 'console\\.log', 'System\\.out\\.println', 'puts', 'echo', 'Console\\.WriteLine', 'std::', 'cout']
    pattern = '|'.join(keywords)
    
    original_code_matches = re.findall(pattern, original_code)
    adversarial_code_matches = re.findall(pattern, adversarial_code)
        
    if len(adversarial_code_matches) > len(original_code_matches):
        return True
    else:
        return False
    
def check_rule_3(original_code, adversarial_code, language) -> bool:
    
    """
    Transformation: Split single line variable declarations into multiple lines.
    Verification: Check if the variable declarations have changed.
    """
    
    root1 = parse_code(original_code, language)
    root2 = parse_code(adversarial_code, language)
    
    original_variable_declarations = extract_variable_declarations(root1)
    adversarial_variable_declarations = extract_variable_declarations(root2)
    
    if not any((',' in item) for item in original_variable_declarations):
        return False
    
    return original_variable_declarations != adversarial_variable_declarations

def check_rule_4(original_code, adversarial_code, language):
    """
    Transformation: Merge multiple variable declarations into a single line.
    Verification: Check if the variable declarations have changed.
    """
    root1 = parse_code(original_code, language)
    root2 = parse_code(adversarial_code, language)
    
    original_variable_declarations = extract_variable_declarations(root1)
    adversarial_variable_declarations = extract_variable_declarations(root2)
    
    if not any((',' in item) for item in adversarial_variable_declarations):
        return False
    
    if len(original_variable_declarations) == len(adversarial_variable_declarations):
        return False
    
    return original_variable_declarations != adversarial_variable_declarations

def check_rule_5(original_code, adversarial_code, language):
    
    """
    Transformation: Change the order of statements.
    Verification: Check if the order of statements has changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_variable_declarations = extract_variable_declarations(tree1)
    adversarial_variable_declarations = extract_variable_declarations(tree2)
    
    original_function_invocations = find_all_function_invocations(tree1)
    adversarial_function_invocations = find_all_function_invocations(tree2)
    
    original_if_statements = find_all_if_else_statements(tree1)
    adversarial_if_statements = find_all_if_else_statements(tree2)
    
    original_comparisons = extract_comparisons_as_strings(tree1)
    adversarial_comparisons = extract_comparisons_as_strings(tree2)
    
    return original_variable_declarations != adversarial_variable_declarations or original_function_invocations != adversarial_function_invocations or original_if_statements != adversarial_if_statements or original_comparisons != adversarial_comparisons
        
def check_rule6_and_7(original_code, adversarial_code, language):
    """
    Transformation: Change variable/function names to a different style.
    Verification: Check if the variable/function names have changed.
    """
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_identifiers = find_identifiers(tree1)
    adversarial_identifiers = find_identifiers(tree2)
    
    return set(original_identifiers) != set(adversarial_identifiers)

def check_rule_8(original_code, adversarial_code, language):
    
    """
    Transformation: Swap relational operators.
    Verification: Check if the relational operators have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_comparisons = extract_comparisons_as_strings(tree1)
    adversarial_comparisons = extract_comparisons_as_strings(tree2)
    if len(original_comparisons) == 0 or len(adversarial_comparisons) == 0:
        return False
    
    return original_comparisons != adversarial_comparisons

def check_rule_9(original_code, adversarial_code, language):
    
    """
    Transformation: Rewrite conditional statements into converse-negative expressions.
    Verification: Check if the conditional statements have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_comparisons = extract_comparisons_as_strings(tree1)
    adversarial_comparisons = extract_comparisons_as_strings(tree2)
    if len(original_comparisons) == 0 or len(adversarial_comparisons) == 0:
        return False
    
    return original_comparisons != adversarial_comparisons

def check_rule_10(original_code, adversarial_code, language):
    
    """
    Transformation: Convert integer literals to expressions.
    Verification: Check if the integer literals have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    original_assignments = extract_assignments_as_strings(tree1)
    adversarial_assignments = extract_assignments_as_strings(tree2)
    
    if len(original_assignments) == 0 or len(adversarial_assignments) == 0:
        return False
    
    return original_assignments != adversarial_assignments
    
def check_rule_11(original_code, adversarial_code, language):
    
    """
    Transformation: Convert increment/decrement operators to assignment operators.
    Verification: Check if the increment/decrement operators have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_types = set()
    traverse(tree1, original_types)
    adversarial_types = set()
    traverse(tree2, adversarial_types)
    
    original_code_assignments = extract_assignments_as_strings(tree1)
    adversarial_code_assignments = extract_assignments_as_strings(tree2)
    
    if original_code_assignments == adversarial_code_assignments:
        return False
    
    original_code_assignments = [assignment for assignment in original_code_assignments if "++" in assignment or "--" in assignment]
    
    if len(original_code_assignments) == 0:
        return False
    
    adversarial_code_assignments = [assignment for assignment in adversarial_code_assignments if "+=" in assignment or "-=" in assignment]
    
    if len(adversarial_code_assignments) == 0:
        return False
    
    return True

def check_rule_12(original_code, adversarial_code, language):
    
    """
    Transformation: Convert increment/decrement operators to assignment operators.
    Verification: Check if the increment/decrement operators have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_code_assignments = extract_assignments_as_strings(tree1)
    adversarial_code_assignments = extract_assignments_as_strings(tree2)
    
    if original_code_assignments == adversarial_code_assignments:
        return False
    
    original_code_assignments = [assignment for assignment in original_code_assignments if "+=" in assignment or "-=" in assignment]
    
    if len(original_code_assignments) == 0:
        return False
    
    pattern = r"(?:\+=|-=)"
    
    if len(re.findall(pattern, original_code)) == len(re.findall(pattern, adversarial_code)):
        return False
    
    adversarial_code_assignments = [assignment for assignment in adversarial_code_assignments if "++" in assignment or "--" in assignment]
    
    if len(adversarial_code_assignments) == 0:
        return False
    
    return True

def check_rule_13(original_code, adversarial_code, language):
    
    """
    Transformation: Convert integer literals to hexadecimal values.
    Verification: Check if the integer literals have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_code_assignments = extract_assignments_as_strings(tree1)
    adversarial_code_assignments = extract_assignments_as_strings(tree2)
    
    if original_code_assignments == adversarial_code_assignments:
        return False
    
    #Regex for identifying hex numbers 0[xX][0-9a-fA-F]+
    hex_pattern = re.compile(r'(0[xX][0-9a-fA-F]+|\\x[0-9a-fA-F]{2})')
    matches = hex_pattern.findall(adversarial_code)
    
    return len(matches) > 0
    
    # # Find all integer numbers (not already hexadecimal)
    # def find_and_convert_integers(code):
    #     def replacer(match):
    #         integer_value = int(match.group())
    #         return hex(integer_value)

    #     # Regex pattern to match integers not part of identifiers or hex numbers
    #     pattern = r'\b(\d+)\b'
    #     modified_code, count = re.subn(pattern, replacer, code)

    #     return modified_code if count > 0 else 'NA'

    # expected_adversarial_code = find_and_convert_integers(original_code)

    # if expected_adversarial_code == 'NA':
    #     return adversarial_code.strip() == 'NA'
    # else:
    #     return expected_adversarial_code.strip() == adversarial_code.strip()

def check_rule_14(original_code, adversarial_code, language):
    
    """
    Transformation: Convert character literals to their corresponding ASCII values.
    Verification: Check if the character literals have changed.
    """
    
    char_literal_pattern = re.compile(r"'(?:\\.|[^\\'])'")
    matches = char_literal_pattern.findall(original_code)
    
    if len(matches) == 0:
        return False
    
    int_literal_pattern = re.compile(r'\b\d+\b')
    int_literal_original_matches = int_literal_pattern.findall(original_code)
    int_literal_adversarial_matches = int_literal_pattern.findall(adversarial_code)
    
    return int_literal_original_matches != int_literal_adversarial_matches

def check_rule_15(original_code, adversarial_code, language):
    
    """
    Transformation: Convert string literals to character arrays.
    Verification: Check if the string literals have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    pattern = r"(?:std::string\s+\w+\s*=\s*[^;]+;|char\s+\w+\[\]\s*=\s*[^;]+;|const\s+char\*\s+\w+\s*=\s*[^;]+;|String\s+\w+\s*=\s*[^;]+;|new\s+String\(\s*[^)]+\s*\)|char\[\]\s+\w+\s*=\s*\{[^}]+\}|string\s+\w+\s*=\s*[^;]+;|string\s+\w+\s*\([^)]*\);|new\s+string\(\s*[^)]+\s*\)|\w+\s*=\s*['\"][^'\"]*['\"]|\w+\s*=\s*%[qQ]\([^)]*\)|<<[A-Z]+\s*[\s\S]+?[A-Z]+|for\s*\(\s*String\s+\w+\s*:\s*\w+\s*\)|\w+(?:\s*,\s*\w+)+\s*=\s*.+)"
    
    original_code_matches = re.findall(pattern, original_code)
    
    if len(original_code_matches) == 0:
        return False
    
    original_code_assignments = extract_assignments_as_strings(tree1)
    adversarial_code_assignments = extract_assignments_as_strings(tree2)
    
    return original_code_assignments != adversarial_code_assignments

def check_rule_16(original_code, adversarial_code, language):
    
    """
    Transformation: Convert boolean literals to integer literals and vice versa.
    Verification: Check if the boolean literals have changed.
    """
    
    bool_pattern = r'\bTrue|False|false|true\b'
    if len(re.findall(bool_pattern, original_code)) == 0:
        return False
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_code_assignments = extract_variable_declarations(tree1)
    adversarial_code_assignments = extract_variable_declarations(tree2)
    
    return original_code_assignments != adversarial_code_assignments

def check_rule_17_and_18(original_code, adversarial_code, language):
    
    """
    Transformation: Convert 'for' statements to 'while' statements or Vice-Versa.
    Verification: Check if the 'for' or while statements have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_types = set()
    traverse(tree1, original_types)
    adversarial_types = set()
    traverse(tree2, adversarial_types)
    
    for_loop_types = {'for_statement', 'for_loop', 'for'}
    while_loop_types = {'while_statement', 'while_loop', 'while'}
    
    if len(original_types & for_loop_types) > 0 and len(adversarial_types & while_loop_types) > 0:
        return True
    
    if len(original_types & while_loop_types) and len(adversarial_types & for_loop_types):
        return True
    return False

def check_rule_19_and_20(original_code, adversarial_code, language):
    
    """
    Transformation: Convert 'if' statements to 'switch' statements or Vice-Versa.
    Verification: Check if the 'if' statements have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    original_types = set()
    traverse(tree1, original_types)
    adversarial_types = set()
    traverse(tree2, adversarial_types)
    
    if_statement_types = {'if_statement', 'if'}
    switch_statement_types = {'switch_statement', 'switch', 'case', 'when'}
    if len(original_types & if_statement_types) > 0 and len(adversarial_types & switch_statement_types) > 0:
        return True
    if len(original_types & switch_statement_types) > 0 and len(adversarial_types & if_statement_types) > 0:
        return True
    
    return False

def check_rule_21(original_code, adversarial_code, language):
    
    """
    Transformation: Convert 'if-else' statements to 'ternary' operators.
    Verification: Check if the 'if-else' statements have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_if_else_statements = find_all_if_else_statements(tree1)
    adversarial_if_else_statements = find_all_if_else_statements(tree2)
    
    if original_if_else_statements == adversarial_if_else_statements:
        return False
    
    if len(original_if_else_statements) == 0:
        return False
    
    if '?' not in adversarial_code and ':' not in adversarial_code:
        return False
    
    if language == 'python':
        # Python does not support the ternary operator in the same way
        return original_if_else_statements != adversarial_if_else_statements
    
    return True

def check_rule_22(original_code, adversarial_code, language):
    
    """
    Transformation: Convert 'ternary' operators to 'if-else' statements.
    Verification: Check if the 'ternary' operators have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_if_else_statements = find_all_if_else_statements(tree1)
    adversarial_if_else_statements = find_all_if_else_statements(tree2)
    
    if language not in ['python', 'ruby']:
        original_assignments = extract_variable_declarations(tree1)
        if not any(('?' in item and ':' in item) for item in original_assignments):
            return False
    
    return original_if_else_statements != adversarial_if_else_statements

def check_rule_23(original_code, adversarial_code, language):
    """
    Transformation: Swap the statements within 'if' and 'else' blocks.
    Verification: Check if the 'if' and 'else' statements have changed.
    """
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
    
    original_if_else_statements = find_all_if_else_statements(tree1)
    adversarial_if_else_statements = find_all_if_else_statements(tree2)
    
    return original_if_else_statements != adversarial_if_else_statements

def check_rule_24(original_code, adversarial_code, language):
    
    """
    Transformation: Swap the order of parameters in function declarations and invocations.
    Verification: Check if the function invocations have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)

    original_function_invocations = find_all_function_invocations(tree1)
    adversarial_function_invocations = find_all_function_invocations(tree2)
    
    return original_function_invocations != adversarial_function_invocations

def check_rule_25(original_code, adversarial_code, language):
    
    """
    Transformation: Add an extra integer parameter with a default value of zero to function declarations and invocations.
    Verification: Check if the function invocations have changed.
    """
    
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)

    original_function_invocations = find_all_function_invocations(tree1)
    adversarial_function_invocations = find_all_function_invocations(tree2)
    
    return original_function_invocations != adversarial_function_invocations

def check_rule_26(original_code, adversarial_code, language):
    """
    Transformation: Identify groups of statements that could be rewritten into a function.
    Verification: Check if the function invocations have changed.
    """
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)

    original_function_invocations = find_all_function_invocations(tree1)
    adversarial_function_invocations = find_all_function_invocations(tree2)
    
    original_identifiers = find_identifiers(tree1)    
    adversarial_identifiers = find_identifiers(tree2)
    
    #All identifiers in the original code should be present in the adversarial code
    if len(set(original_identifiers) - set(adversarial_identifiers)) > 0:
        return False
    
    return original_function_invocations != adversarial_function_invocations

def check_rule_27(original_code, adversarial_code, language) -> bool:
    """
    Transformation: Swap the order of function declarations.
    Verification: Check if the order of function declarations has changed.
    """
    tree1 = parse_code(original_code, language)
    tree2 = parse_code(adversarial_code, language)
            
    original_funcs = find_identifiers(tree1)
    adversarial_funcs = find_identifiers(tree2)
    
    if len(original_funcs) <= 1:
        return False

    if original_funcs != adversarial_funcs:
        return True
    
    #Overloaded
    if all(item == original_funcs[0] for item in original_funcs) and all(item == adversarial_funcs[0] for item in adversarial_funcs):
        return True

    return False

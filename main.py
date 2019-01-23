import string as string_lib
"""
Formal Grammar
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <int>

Todo: -type checking
    
"""

##############################

VAR_CHARS = string_lib.ascii_letters + string_lib.digits + "_"
SPECIAL_CHARS  = "(){;}"
DIGITS = string_lib.digits
WHITESPACE = " \n\t"

class Tkn:
    """Token name class"""
    var = "VARIABLE"
    binop = "BINARY OPERATOR"

    ifx = "IF KEYWORD"
    elsex = "ELSE KEYWORD"
    returnx = "RETURN KEYWORD"
    prog_keywords = (ifx, elsex, returnx)

    intkey = "INT KEYWORD"
    floatkey = "FLOAT KEYWORD"
    charkey = "CHAR KEYWORD"
    voidkey = "VOID KEYWORD"
    type_keys = (intkey, floatkey, charkey, voidkey)

    lparen = "LEFT PAREN"
    rparen = "RIGHT PAREN"
    semicolon = "SEMICOLON"
    rbrack = "RIGHT BRACKET"
    lbrack = "LEFT BRACKET"
    equal = "EQUAL"
    special_chars = (lparen, rparen, semicolon, rbrack, lbrack)
    
    intx = "INT"
    floatx = "FLOAT"
    charx = "CHAR"
    constants = (intx, floatx, charx)

def is_float(token):
    try:
        float(token)
        return True
    except:
        return False

def is_int(token):
    return all([c in DIGITS for c in token])

def is_char(token):
    if len(token) != 3:
        return False
    return token[0] == "'" and token[1] == "'"

def is_var(token):
    return all([c in VAR_CHARS for c in token])

def is_bin_op(token):
    return token in ("*", "+", "-", "/")

def tok_type(token):
    if   token == "if":     return Tkn.ifx
    elif token == "else":   return Tkn.elsex
    elif token == "return": return Tkn.returnx
    elif token == "int":    return Tkn.intkey
    elif token == "float":  return Tkn.floatkey
    elif token == "char":   return Tkn.charkey  
    elif token == "void":   return Tkn.voidkey
    elif token == ";":      return Tkn.semicolon
    elif token == "{":      return Tkn.lbrack
    elif token == "}":      return Tkn.rbrack
    elif token == "(":      return Tkn.lparen
    elif token == ")":      return Tkn.rparen
    elif token == "=":      return Tkn.equal
    elif is_int(token):     return Tkn.intx
    elif is_float(token):   return Tkn.floatx
    elif is_char(token):    return Tkn.charx
    elif is_bin_op(token):  return Tkn.binop
    elif is_var(token):     return Tkn.var
    

##############################


# AST Nodes
class Prog:
    def __init__(self, subtrees):
        self.children = []
        for subtree in subtrees:
            attach(self, subtree)
class If:
    def __init__(self, cond, true_body, else_body):
        self.children = []
        attach(self, cond)
        attach(self, true_body)
        attach(self, else_body)
        self.cond = cond
        self.true_body = true_body
        self.else_body = else_body

class Cond:
    def __init__(self, operator, operand1, operand2):
        self.children = []
        attach(self, operator)
        attach(self, operand1)
        attach(self, operand2)
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

class Func:
    def __init__(self, ret_type, func_name, body):
        self.children = []
        attach(self, body)
        self.ret_type = ret_type
        self.func_name = func_name
        self.body = body

class Body:
    def __init__(self, statements):
        self.statements = statements
        self.children = []
        for statement in statements:
            attach(self, statement)
        
class Assign:
    def __init__(self, var_name, val):
        self.children = []
        attach(self, var_name)
        attach(self, val)
        self.var_name = var_name
        self.val = val

class Const:
    def __init__(self, val, val_type):
        self.val_type = val_type
        self.val = val

class Return:
    def __init__(self, ret_val):
        self.children = []
        self.ret_val = ret_val
        attach(self, ret_val)

class Var:
    def __init__(self, var_name):
        self.var_name = var_name

class Operation:
    def __init__(self, op_name, exp1, exp2):
        self.children = []
        self.exp1 = exp1
        self.exp2 = exp2
        attach(self, exp1)
        attach(self, exp2)
        self.op_name = op_name


##############################


# Functions
def attach(parent, child):
    child.parent = parent
    parent.children.append(child)

def check(val, exp, msg):
    if val != exp:
        raise Exception(msg)

def tokenize(string):
    tokens = []
    token = ""
    for i, c in enumerate(string):
        token += c
        is_final_char = c in SPECIAL_CHARS or i+1 == len(string) or string[i+1] in SPECIAL_CHARS + WHITESPACE
        if is_final_char:
            tokens.append(token)
            token = ""
    if token:
        tokens.append(token)
        token = ""
    return [t.strip() for t in tokens if t.strip()]        

def parse_statements(tokens, ind):
    check(tok_type(tokens[ind]), Tkn.lbrack, "missing opening bracket")
    ind += 1
    statements = []
    while tokens[ind] != "}":
        if ind >= len(tokens):
            print("Syntax Error")
            return
        statement_tokens = []
        while tok_type(tokens[ind]) != Tkn.semicolon:
            statement_tokens.append(tokens[ind])
            ind += 1
        statement, _ = sub_AST(statement_tokens, 0)
        statements.append(statement)
        ind += 1
    ind += 1
    return statements, ind

def expression_AST(tokens, ind):
    final_ind = ind
    tok_list = []
    p_lev = 0
    while tok_type(tokens[final_ind]) is not Tkn.semicolon: 
        """REFACTOR VERY UGLY"""
        curr_type = tok_type(tokens[final_ind])
        if curr_type is Tkn.lparen:
            p_lev -=1
        elif curr_type is Tkn.rparen:
            p_lev += 1
        if  p_lev > 0:
            final_ind += 1
            break
        tok_list.append(tokens[final_ind])
        final_ind += 1

    lst_ind = 0
    first_tkn_type = tok_type(tok_list[lst_ind])
    if first_tkn_type in Tkn.constants:
        constant = Const(tok_list[lst_ind], first_tkn_type)
        lst_ind += 1
        if len(tok_list) == 1:
            return constant, final_ind
        elif tok_type(tok_list[lst_ind]) is Tkn.binop:
            operator = tok_list[lst_ind]
            lst_ind += 1
            second_expression, _ = expression_AST(tokens, ind + lst_ind)
            return Operation(op_name = operator, exp1=constant, exp2=second_expression), final_ind
        else:
            raise Exception("Constant followed by nonterminary token that is not nonbinary operator")

    elif first_tkn_type is Tkn.lparen:
        lst_ind += 1
        p_lev = -1
        while p_lev < 0:
            if tok_type(tok_list[lst_ind]) is Tkn.rparen:
                p_lev += 1
            elif tok_type(tok_list[lst_ind]) is Tkn.lparen:
                p_lev -= 1
            lst_ind += 1
        if len(tok_list) == lst_ind:
            subtree, _ = expression_AST(tokens, ind+1)
            return subtree, final_ind
        elif tok_type(tok_list[lst_ind]) is tkn.binop:
            operator = tok_type(tok_list[lst_ind])
            expression1, _ = expression_AST(tokens, ind+1)
            expression2, _ = expression_AST(tokens, ind+lst_ind)
            return Operation(op_name=Operation, exp1=expression1, exp2=expression2), final_ind
    print(tokens, ind, first_tkn_type)


def sub_AST(tokens, ind):
    root = tokens[ind]
    root_type = tok_type(root)

    if root_type in Tkn.prog_keywords:
        """Special Language Construct"""
        if root_type is Tkn.ifx:
            ind += 1
            check(tok_type(tokens[ind]), Tkn.lparen, "if should be followed by '('")
            ind += 1
            expression, ind = expression_AST(tokens, ind)
            check(tok_type(tokens[ind]), Tkn.rparen, "missing closing parenthesis")
            ind += 1
            true_body, ind = parse_statements(tokens, ind)
            if tokens[ind] == "else":
                ind += 1
                else_body, ind = parse_statements(tokens, ind)
            else:
                else_body = None
            subtree = If(cond=expression, true_body=Body(true_body), else_body=Body(else_body))
        elif root_type is Tkn.returnx:
            ind += 1
            ret_expression, ind = expression_AST(tokens, ind)
            subtree = Return(ret_expression)

    elif root_type in Tkn.type_keys:
        """Function Declaration"""
        ret_type = root
        ind += 1
        func_name = tokens[ind]
        ind += 1
        check(tok_type(tokens[ind]), Tkn.lparen, "function name should be followed by '('")
        ind += 1
        check(tok_type(tokens[ind]), Tkn.rparen, "function name should end with a')'")
        ind += 1
        statements, ind = parse_statements(tokens, ind)
        subtree = Func(ret_type=ret_type, func_name=func_name, body=Body(statements))

    elif root_type is Tkn.var:
        """ Variable Assignment"""
        variable = Var(root)
        ind += 1
        check(tok_type(tokens[ind]), Tkn.equal, "missing = after variable name")
        ind += 1
        expression, ind = expression_AST(tokens, ind)
        subtree = Assign(var_name=variable, val=expression)
    return subtree, ind

def main_AST(program):
    ind = 0
    tokens = tokenize(program)
    subtrees = []
    while ind < len(tokens):
        subtree, ind = sub_AST(tokens, ind)
        subtrees.append(subtree)
    return Prog(subtrees)

def print_tree(tree):
    print("Parent: ", tree.__class__.__name__)
    if hasattr(tree, "children"):
        children = tree.children
        for child in children:
            print("-Child: {}".format(child.__class__.__name__)) 
            if hasattr(child, "val"):
                print("  Val: {}".format(child.val))
            if hasattr(child, "op_name"):
                print("  Operator: {}".format(child.op_name))
        for child in children:
            print_tree(child)

#print(tokenize("5 + (10 + 10);"))
print_tree(expression_AST(tokenize("5 + 10;"), 0)[0])




















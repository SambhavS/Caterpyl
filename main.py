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

# Globals
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

    get_type_keyword = {intx: intkey, floatkey: floatx, charx: charkey}

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
    def __init__(self, var_name, data_type, exp):
        self.children = []
        attach(self, var_name)
        attach(self, exp)
        self.data_type = data_type
        self.var_name = var_name
        self.exp = exp

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

class Expression:
    def __init__(self, op_name, oper1, oper2):
        self.children = []
        self.oper1 = oper1
        self.oper2 = oper2
        attach(self, oper1)
        attach(self, oper2)
        self.op_name = op_name


##############################


# Functions
def attach(parent, child):
    child.parent = parent
    parent.children.append(child)

def check(val, exp, msg):
    if tok_type(val) != exp:
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
    check(tokens[ind], Tkn.lbrack, "missing opening bracket")
    ind += 1
    statements = []
    while tok_type(tokens[ind]) != Tkn.rbrack:
        if ind >= len(tokens):
            raise Exception("Syntax Error")
        statement_tokens = []
        while not statement_tokens or tok_type(tokens[ind-1]) != Tkn.semicolon:
            statement_tokens.append(tokens[ind])
            ind += 1
        statement, _ = sub_AST(statement_tokens, 0, is_statement=True)
        statements.append(statement)
    return statements, ind+1

def expression_AST(tokens, ind):
    final_ind = ind
    tok_list = []
    p_lev = 0
    # Find ending index of overall expression
    while tok_type(tokens[final_ind]) is not Tkn.semicolon: 
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
            return Expression(op_name = operator, oper1=constant, oper2=second_expression), final_ind
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
            return Expression(op_name=operator, oper1=expression1, oper2=expression2), final_ind


def sub_AST(tokens, ind, is_statement=False):
    root = tokens[ind]
    root_type = tok_type(root)

    if root_type in Tkn.prog_keywords:
        """Special Language Construct"""
        if root_type is Tkn.ifx:
            ind += 1
            check(tokens[ind], Tkn.lparen, "if should be followed by '('")
            ind += 1
            expression, ind = expression_AST(tokens, ind)
            check(tokens[ind], Tkn.rparen, "missing closing parenthesis")
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
        type_dec = root
        ind += 1
        if is_statement:
            """ Variable Assignment -- needs type checking"""
            check(tokens[ind], Tkn.var, "Type declaration should be followed by var name")
            variable = Var(root)
            ind += 1
            check(tokens[ind], Tkn.equal, "Missing = after variable name")
            ind += 1
            expression, ind = expression_AST(tokens, ind)
            subtree = Assign(var_name=variable, data_type=type_dec, exp=expression)
        else:
            """Function Declaration -- needs type checking"""
            func_name = tokens[ind]
            ind += 1
            check(tokens[ind], Tkn.lparen, "Function name should be followed by '('")
            ind += 1
            check(tokens[ind], Tkn.rparen, "Function name should end with a')'")
            ind += 1
            statements, ind = parse_statements(tokens, ind)
            subtree = Func(ret_type=type_dec, func_name=func_name, body=Body(statements))

    return subtree, ind

def main_AST(program):
    ind = 0
    tokens = tokenize(program)
    subtrees = []
    while ind < len(tokens):
        subtree, ind = sub_AST(tokens, ind)
        subtrees.append(subtree)
    return Prog(subtrees)

def print_tree(tree, depth=0):
    dt_str = " ({})".format(tree.data_type) if hasattr(tree, "data_type") else ""
    op_str = " ({})".format(tree.op_name) if hasattr(tree, "op_name") else ""
    val_str = " ({})".format(tree.val) if hasattr(tree, "val") else ""
    print("{}{}{}{}{}".format("---"*depth, tree.__class__.__name__, op_str, val_str, dt_str))
    if hasattr(tree, "children"):
        children = tree.children            
        for child in children:
            print_tree(child, depth+1)

print_tree(main_AST("int main(){ int c = 3; return 5 + 5; } int prn() { int x = 10;}"))




















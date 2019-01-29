# Imports
import string as string_lib

# Globals
VAR_CHARS = string_lib.ascii_letters + string_lib.digits + "_"
SPECIAL_CHARS  = "(){;}"
DIGITS = string_lib.digits
WHITESPACE = " \n\t"
ORDERED_BINOPS = ("**", "*", "/", "+", "-", "==", "<=", "!=", ">=", "<", ">")

################# Tkn Types ###################

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

def typ(token):
    """ Return type of token"""
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
    return token in ORDERED_BINOPS


def attach(parent, child):
    child.parent = parent
    parent.children.append(child)

########## AST Node Classes ###########

# High Level Nodes
class Prog:
    def __init__(self, subtrees):
        self.children = []
        for subtree in subtrees:
            attach(self, subtree)

class Func:
    def __init__(self, ret_type, name, body):
        self.children = []
        attach(self, body)
        self.ret_type = ret_type
        self.name = name
        self.body = body

class Body:
    def __init__(self, statements):
        self.statements = statements
        self.children = []
        for statement in statements:
            attach(self, statement)

# Expression
class Expression:
    def __init__(self, op_name, oper1, oper2):
        self.children = []
        self.oper1 = oper1
        self.oper2 = oper2
        attach(self, oper1)
        attach(self, oper2)
        self.op_name = op_name

# Leaves
class Const:
    def __init__(self, val, val_type):
        self.val_type = val_type
        self.val = val

class Var:
    def __init__(self, name=None):
        self.name = name

# Statements     
class If:
    def __init__(self, cond, true_body, else_body):
        self.children = []
        attach(self, cond)
        attach(self, true_body)
        if else_body.children:
            attach(self, else_body)
        self.cond = cond
        self.true_body = true_body
        self.else_body = else_body

class Assign:
    def __init__(self, var_name, exp):
        self.children = []
        attach(self, var_name)
        attach(self, exp)
        self.var_name = var_name
        self.exp = exp

class Decl:
    def __init__(self, type_dec, var):
        self.children = []
        attach(self, var)
        self.type_dec = type_dec
        self.var = var

class Return:
    def __init__(self, ret_val):
        self.children = []
        self.ret_val = ret_val
        attach(self, ret_val)
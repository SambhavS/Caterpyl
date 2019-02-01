# Imports
import string as string_lib

# Globals
VAR_CHARS = string_lib.ascii_letters + string_lib.digits + "_"
DIGITS = string_lib.digits
WHITESPACE = " \n\t"
ORDERED_OPS = ("!", "%", "*", "/", "+", "-", "<=", "!=", 
                  ">=", "<", ">", "==", "!=", "||", "&&")
UNOPS = ("!",)
BINOPS = ("%", "*", "/", "+", "-", "<=", ">=", "<", ">", "==", "!=", "||", "&&")

################# Tkn Types ###################

class Tkn:
    """Token name class"""
    var = "VARIABLE"
    binop = "BINARY OPERATOR"
    unop = "UNARY OPERATOR"

    ifx = "IF KEYWORD"
    elsex = "ELSE KEYWORD"
    whilex = "WHILE KEYWORD"
    returnx = "RETURN KEYWORD"
    prog_keywords = (ifx, elsex, whilex, returnx)

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
    op_eq = "OPERATOR EQUAL"
    special_chars = (lparen, rparen, semicolon, rbrack, lbrack)
    
    intx = "INT"
    floatx = "FLOAT"
    charx = "CHAR"
    constants = (intx, floatx, charx)

    get_type_keyword = {intx: intkey, floatkey: floatx, charx: charkey}

def typ(token):
    """ Return type of token"""
    if   token == "if":     return Tkn.ifx
    elif token == "while":  return Tkn.whilex
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
    elif is_op_eq(token):    return Tkn.op_eq
    elif is_int(token):     return Tkn.intx
    elif is_float(token):   return Tkn.floatx
    elif is_char(token):    return Tkn.charx
    elif is_bin_op(token):  return Tkn.binop
    elif is_un_op(token):   return Tkn.unop
    elif is_var(token):     return Tkn.var

def is_op_eq(token):
    return len(token) == 2 and token[0] in ("+","-","/","*") and token[1] == "="
    
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
    return token in BINOPS

def is_un_op(token):
    return token in UNOPS

def attach(parent, child):
    child.parent = parent
    parent.children.append(child)

########## AST Node Classes ###########
def get_expression_type(exp, lookup):
    if exp.op_name in BINOPS or UNOPS:
        expected_type = "int"
    if exp.op_name in UNOPS:
        oper_type = oper_type_dec(exp.oper, lookup).lower()
        if oper_type == expected_type:
            return expected_type
        raise Exception("Type Error!")
    elif exp.op_name in BINOPS:
        oper_type1 = oper_type_dec(exp.oper1, lookup).lower()
        oper_type2 = oper_type_dec(exp.oper2, lookup).lower()
        if oper_type1 == expected_type and oper_type2 == expected_type:
            return expected_type
        raise Exception("Type Error!")

def oper_type_dec(oper, lookup):
    n_type = node_type(oper).strip()
    if n_type == "expression": return oper.type_dec
    elif n_type == "const":  return oper.val_type
    elif n_type == "var": return lookup[oper.name]


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
    def __init__(self, op_name, oper1, oper2, lookup):
        self.children = []
        self.oper1 = oper1
        self.oper2 = oper2
        attach(self, oper1)
        attach(self, oper2)
        self.op_name = op_name
        self.type_dec = get_expression_type(self, lookup) 

class UnaryExpression:
    def __init__(self, op_name, oper):
        self.children = []
        self.oper = oper
        attach(self, oper)
        self.op_name = op_name
        self.type_dec = get_expression_type(self, lookup) 

# Leaves
class Const:
    def __init__(self, val, val_type):
        self.val = val
        self.val_type = val_type
        

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

class While:
    def __init__(self, cond, true_body):
        self.children = []
        attach(self, cond)
        attach(self, true_body)
        self.cond = cond
        self.true_body = true_body

class Assign:
    def __init__(self, var_name, exp):
        self.children = []
        attach(self, var_name)
        attach(self, exp)
        self.var_name = var_name
        self.exp = exp

class Decl:
    def __init__(self, type_dec, var, lookup):
        self.children = []
        attach(self, var)
        self.type_dec = type_dec
        self.var = var
        if var.name not in lookup:
            lookup[var.name] = type_dec
        else:
            raise Exception("TypeError: `{}` already declared".format(var.name))

class Return:
    def __init__(self, ret_val):
        self.children = []
        self.ret_val = ret_val
        attach(self, ret_val)

############# Misc Utils ##################

def print_IL(lines):
    """Format and print intermediate representation lines"""
    print()
    for l in lines:
        if l[-1] == ":":
            print(l)
        else:
            print("   {}".format(l))

def print_lst(lst):
    """Print all elements in given list"""
    print()
    for i in lst:
        print(i)

def print_tree(tree, depth=0):
    """ Recursively prints an AST"""
    string = "{}{}{}".format("   " * depth, "|", tree.__class__.__name__)
    string += " ({})".format(tree.data_type) if hasattr(tree, "data_type") else ""
    string += " ({})".format(tree.type_dec) if hasattr(tree, "type_dec") else ""
    string += " ({})".format(tree.op_name) if hasattr(tree, "op_name") else ""
    string += " ({})".format(tree.name) if hasattr(tree, "name") else ""
    string += " ({})".format(tree.val) if hasattr(tree, "val") else ""
    print(string)
    if hasattr(tree, "children"):
        children = tree.children
        for child in children:
            print_tree(child, depth + 1)

def node_type(node):
    """Return string correspoonding to type of node"""
    return node.__class__.__name__.lower()        
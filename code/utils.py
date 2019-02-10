# Imports
import string as string_lib

# Globals
VAR_CHARS = string_lib.ascii_letters + string_lib.digits + "_"
DIGITS = string_lib.digits
WHITESPACE = " \n\t"
ORDERED_OPS = ("!", "%", "*", "/", "+", "-", "<=", "!=", 
                  ">=", "<", ">", "==", "!=", "||", "&&")
BOOL_UNOPS = ("!",)
BOTH_BINOPS = ("<=", ">=", "<", ">", "==", "!=")
INT_BINOPS = ("%", "*", "/", "+", "-")
BOOL_BINOPS = ("||", "&&")
BINOPS = ("%", "*", "/", "+", "-", "<=", ">=", "<", ">", "==", "!=", "||", "&&")
################# Tkn Types ###################

class Tkn:
    """Token name class"""
    var = "VARIABLE"
    int_binop = "INTEGER BINARY OPERATOR"
    bool_binop = "BOOLEAN BINARY OPERATOR"
    both_binop = "BOOLEAN & INTEGER BINARY OPERATOR"
    bool_unop = "BOOLEAN UNARY OPERATOR"
    binops = (bool_binop, both_binop, int_binop)

    ifx = "IF KEYWORD"
    elsex = "ELSE KEYWORD"
    whilex = "WHILE KEYWORD"
    returnx = "RETURN KEYWORD"
    prog_keywords = (ifx, elsex, whilex, returnx)

    intkey = "INT KEYWORD"
    boolkey = "BOOL KEYWORD"
    voidkey = "VOID KEYWORD"
    type_keys = (intkey, boolkey, voidkey)

    lparen = "LEFT PAREN"
    rparen = "RIGHT PAREN"
    semicolon = "SEMICOLON"
    rbrack = "RIGHT BRACKET"
    lbrack = "LEFT BRACKET"
    equal = "EQUAL"
    op_eq = "OPERATOR EQUAL"
    comma = "COMMA"
    special_chars = (lparen, rparen, semicolon, rbrack, lbrack, comma)
    
    intx = "INT"
    boolx = "BOOL"
    constants = (intx, boolx)

    get_type_keyword = {intx: intkey, boolkey: boolx}

def typ(token):
    """ Return type of token"""
    if   token == "if":     return Tkn.ifx
    elif token == "while":  return Tkn.whilex
    elif token == "else":   return Tkn.elsex
    elif token == "return": return Tkn.returnx
    elif token == "int":    return Tkn.intkey
    elif token == "bool":   return Tkn.boolkey
    elif token == "void":   return Tkn.voidkey
    elif token == ";":      return Tkn.semicolon
    elif token == "{":      return Tkn.lbrack
    elif token == "}":      return Tkn.rbrack
    elif token == "(":      return Tkn.lparen
    elif token == ")":      return Tkn.rparen
    elif token == "=":      return Tkn.equal
    elif token == ",":      return Tkn.comma
    elif is_op_eq(token):   return Tkn.op_eq
    elif is_int(token):     return Tkn.intx
    elif is_both_bin_op(token):  return Tkn.both_binop
    elif is_int_bin_op(token):   return Tkn.int_binop
    elif is_bool_bin_op(token):  return Tkn.bool_binop
    elif is_bool_un_op(token):   return Tkn.bool_unop
    elif is_bool(token):    return Tkn.boolx
    elif is_var(token):     return Tkn.var

def is_op_eq(token):
    return len(token) == 2 and token[0] in ("+","-","/","*") and token[1] == "="
    
def is_int(token):
    return all([c in DIGITS for c in token])

def is_bool(token):
    return token in ("True", "False")

def is_var(token):
    return all([c in VAR_CHARS for c in token])

def is_both_bin_op(token):
    return token in BOTH_BINOPS

def is_int_bin_op(token):
    return token in INT_BINOPS

def is_bool_bin_op(token):
    return token in BOOL_BINOPS

def is_bool_un_op(token):
    return token in BOOL_UNOPS

def attach(parent, child):
    child.parent = parent
    parent.children.append(child)

########## AST Node Classes ###########
def get_expression_type(exp, lookup):
    if exp.op_name in BOOL_UNOPS:
        oper_type = oper_type_dec(exp.oper, lookup).lower()
        if oper_type == "bool":
            return "BOOL"
        raise Exception("Type Error!")
    elif exp.op_name in BINOPS:
        oper_type1 = oper_type_dec(exp.oper1, lookup).lower()
        oper_type2 = oper_type_dec(exp.oper2, lookup).lower()
        if exp.op_name in INT_BINOPS and oper_type1 == oper_type2 and oper_type1 == "int":
            return "INT"
        if exp.op_name in BOOL_BINOPS and oper_type1 == oper_type2 and oper_type1 == "bool":
            return "BOOL"
        if exp.op_name in BOTH_BINOPS and oper_type1 == oper_type2 and oper_type1 in ["int", "bool"]:
            return "BOOL"
        raise Exception("Type Error!")

def oper_type_dec(oper, lookup):
    n_type = node_type(oper).strip()
    if n_type in ("const", "expression"):  return oper.type_dec
    elif n_type == "var":       return lookup[oper.name]["type_dec"]
    elif n_type == "fnccall":   return oper.master_lookup[oper.called_func]["{}::TYPE_INFO".format(oper.called_func)]


# High Level Nodes
class Prog:
    def __init__(self, subtrees):
        self.children = []
        for subtree in subtrees:
            attach(self, subtree)

class Func:
    def __init__(self, ret_type, name, body, params, lookup):
        self.children = []
        attach(self, body)
        self.params = params
        self.ret_type = ret_type
        self.name = name
        self.body = body
        lookup["{}::TYPE_INFO".format(name)] = {"type_dec": ret_type, "type":"func"}
        if name == "main" and params:
            raise Exception("Main function should not have parameters")

class FncCall:
    def __init__(self, called_func, arguments, master_lookup):
        self.children = []
        self.arguments = arguments
        for arg in arguments:
            attach(self, arg)
        self.called_func = called_func
        self.master_lookup = master_lookup

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
    def __init__(self, op_name, oper, lookup):
        self.children = []
        self.oper = oper
        attach(self, oper)
        self.op_name = op_name
        self.type_dec = get_expression_type(self, lookup) 

# Leaves
class Const:
    def __init__(self, val, type_dec):
        self.val = val
        self.type_dec = type_dec
        

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
    def __init__(self, var, exp, lookup):
        self.children = []
        attach(self, var)
        attach(self, exp)
        self.var = var
        self.exp = exp
        if var.name not in lookup:
            raise Exception("Variable {} not declared".format(var.name))
        var_type, exp_type = lookup[var.name]["type_dec"].lower(), exp.type_dec.lower()
        if var_type != exp_type:
            raise TypeError("Variable type ({}) doesn't match expression type ({})".format(var_type, exp_type))

class Decl:
    def __init__(self, type_dec, var, lookup):
        self.children = []
        attach(self, var)
        self.type_dec = type_dec
        self.var = var
        if var.name not in lookup:
            lookup[var.name] = {"type_dec": type_dec, "type":"var"}
        else:
            raise TypeError("`{}` already declared".format(var.name))

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
    string += " {}".format(tree.params) if hasattr(tree, "params") else ""
    print(string)
    if hasattr(tree, "children"):
        children = tree.children
        for child in children:
            print_tree(child, depth + 1)

def node_type(node):
    """Return string correspoonding to type of node"""
    return node.__class__.__name__.lower()        
from utils import *

"""
TODO:
-add type checking
-namespace for variables vs function?

Program Summary:
We go through the program, checking for independent trees. Each tree is a
return statement, an if/else statement, a variable assignment, or a function declaration.
We should distinguish between a series of statements, a single statement, and an expression.

We skip non-parsable tokens proactively for parse_statements & statement_AST, but not for expression_AST
"""


def test_run(fname):
    """ Load and run program"""
    with open(fname) as f:
        contents = f.read()
        ast = main_AST(contents)
        print_tree(ast)


def print_tree(tree, depth=0):
    dt_str = " ({})".format(tree.data_type) if hasattr(
        tree, "data_type") else ""
    op_str = " ({})".format(tree.op_name) if hasattr(tree, "op_name") else ""
    val_str = " ({})".format(tree.val) if hasattr(tree, "val") else ""
    print("{}{}{}{}{}".format("{}{}".format("   " * depth, "|"),
                              tree.__class__.__name__, op_str, val_str, dt_str))
    if hasattr(tree, "children"):
        children = tree.children
        for child in children:
            print_tree(child, depth + 1)


def main_AST(program):
    tokens = tokenize(program)
    subtrees = parse_statements(tokens, func_dec=True)
    return Prog(subtrees)


def parse_statements(tokens, func_dec=False):
    statements = []
    while len(tokens) and typ(tokens[0]) != Tkn.rbrack:
        statement = statement_AST(tokens, func_dec)
        statements.append(statement)
    # Parse `}`
    if tokens:
        tokens.pop(0)
    return statements


def statement_AST(tokens, func_dec=False):
    root = tokens[0]
    root_type = typ(root)
    if root_type in Tkn.prog_keywords:
        """Special Language Construct"""
        if root_type is Tkn.ifx:
            check_skip(tokens, Tkn.ifx, "Check `if`")
            check_skip(tokens, Tkn.lparen, "Check `(`")
            expression = dropped_exp_AST(tokens)
            check_skip(tokens, Tkn.rparen, "Check `)`")
            check_skip(tokens, Tkn.lbrack, "Check `{`")
            true_statements = parse_statements(tokens)
            if tokens[0] == "else":
                check_skip(tokens, Tkn.elsex, "Check `else`")
                check_skip(tokens, Tkn.lbrack, "Check `{`")
                else_statements = parse_statements(tokens)
            else:
                check_skip(tokens, Tkn.rbrack, "Check `}`")
                else_statements = None
            subtree = If(cond=expression, true_body=Body(
                true_statements), else_body=Body(else_statements))
        elif root_type is Tkn.returnx:
            check_skip(tokens, Tkn.returnx, "Check `return`")
            ret_expression = dropped_exp_AST(tokens)
            check_skip(tokens, Tkn.semicolon, "Check `;`")
            subtree = Return(ret_expression)

    elif root_type in Tkn.type_keys:
        type_dec = root
        check_skip(tokens, Tkn.type_keys, "Check type keyword")
        if func_dec:
            """ Function Declaration -- needs type checking"""
            check_skip(tokens, Tkn.var, "Check function var name")
            func_name = tokens[0]
            check_skip(tokens, Tkn.lparen, "Check `(`")
            check_skip(tokens, Tkn.rparen, "Check `)`")
            check_skip(tokens, Tkn.lbrack, "Check `{`")
            statements = parse_statements(tokens, func_dec=False)
            subtree = Func(ret_type=type_dec,
                           func_name=func_name, body=Body(statements))
        else:
            """ Variable Assignment -- needs type checking"""
            variable = Var(root)
            check_skip(tokens, Tkn.var, "Check var name")
            check_skip(tokens, Tkn.equal, "Check `=`")
            expression = dropped_exp_AST(tokens)
            check_skip(tokens, Tkn.semicolon, "Check `;`")
            subtree = Assign(var_name=variable,
                             data_type=type_dec, exp=expression)
    return subtree

def dropped_exp_AST(tokens):
    exp_ast, drops = expression_AST(tokens)
    for i in range(drops):
        tokens.pop(0)
    return exp_ast

def expression_AST(tokens, ind=0):
    """Returns an AST representing the expression starting at the given index"""
    if typ(tokens[ind]) is Tkn.lparen:
        final_ind = fin_ind(tokens, ind)
        children = []
        i = ind+1
        while i < final_ind:
            tok_type = typ(tokens[i])
            if tok_type in Tkn.constants or tok_type is Tkn.var or tok_type is Tkn.binop:
                if tok_type in Tkn.constants:
                    val = Const(tokens[i], tok_type)
                elif tok_type is Tkn.var:
                    val = Var(tokens[i])
                elif tok_type is Tkn.binop:
                    val = tokens[i]
                children.append(val)
                i += 1
            elif tok_type is Tkn.lparen:
                expression, _ = expression_AST(tokens, i)
                children.append(expression)
                i = fin_ind(tokens, i) + 1
        # Binary operators must alternate
        if len(children) == 1:
            return children[0], i
        if len(children) % 2 == 0:
            raise Exception("Bad expression")
        val = seq_to_tree(children)
        final_ind += 1
        if typ(tokens[final_ind]) is Tkn.binop:
            operator = tokens[final_ind]
            final_ind += 1
            second_exp, final_ind = expression_AST(tokens, final_ind)
            return Expression(op_name=operator, oper1=val, oper2=second_exp), final_ind
        elif typ(tokens[final_ind]) in [Tkn.semicolon, Tkn.rparen]:
            return val, final_ind
        else:
            print(tokens[final_ind])
    elif typ(tokens[ind]) in Tkn.constants or typ(tokens[ind]) is Tkn.var:
        val = Const(tokens[ind], typ(tokens[ind])) if typ(
            tokens[ind]) in Tkn.constants else Var(tokens[ind])
        ind += 1
        if typ(tokens[ind]) is Tkn.binop:
            operator = tokens[ind]
            ind += 1
            second_exp, ind = expression_AST(tokens, ind)
            return Expression(op_name=operator, oper1=val, oper2=second_exp), ind
        elif typ(tokens[ind]) in [Tkn.semicolon, Tkn.rparen]:
            return val, ind
    

def seq_to_tree(sequence):
    """Takes in a sequence of operators and objects and makes an expression tree"""
    if len(sequence) == 3:
        return Expression(op_name=sequence[1], oper1=sequence[0], oper2=sequence[-1])
    return Expression(op_name=sequence[1], oper1=sequence[0], oper2=seq_to_tree(sequence[2:]))


def fin_ind(tokens, start):
    """Returns the index corresponding to the end of an expression"""
    final_ind = start+1
    if typ(tokens[start]) in Tkn.constants or typ(tokens[start]) is Tkn.var:
        return final_ind
    p_lvl = 1
    while True:
        tok_type = typ(tokens[final_ind])
        if tok_type is Tkn.lparen:
            p_lvl += 1
        if tok_type is Tkn.rparen:
            p_lvl -= 1
        if p_lvl == 0 or tok_type is Tkn.semicolon:
            break
        final_ind += 1
    return final_ind


def tokenize(string):
    """ Returns list of tokens given program as a string"""
    tokens = []
    token = ""
    for i, c in enumerate(string):
        token += c
        if (c in SPECIAL_CHARS
            or i+1 == len(string)
                or string[i+1] in SPECIAL_CHARS + WHITESPACE):
            tokens.append(token)
            token = ""
    if token:
        tokens.append(token)
        token = ""
    return [t.strip() for t in tokens if t.strip()]


def check_skip(tokens, exp, msg):
    """Checks that value matches a certain type and skips it"""
    if typ(tokens[0]) not in exp:
        raise Exception("{} but got {}".format(msg, tokens[0]))
    tokens.pop(0)


test_run("ex.c")
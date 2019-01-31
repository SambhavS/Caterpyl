from utils import *

def ast_to_IL(ast):
    """Sets up register counter and initializes lists to hold IL. 
    Calls helper with 'main' to recursively generate IL and process output"""
    def get_count(counter):
        counter[0] += 1
        return counter[0]

    def convert_body(parent_func, body):
        nonlocal lines
        """Recursively traverses tree and generates IL based on node type"""
        for statement in body.statements:
            if node_type(statement) == "return":
                last_reg, sublines = exp_to_IL(r_count, statement.ret_val)
                lines += sublines
                if parent_func == "main":
                    lines.append("retmain {}".format(last_reg))
                else:
                    lines.append("ret {}".format(last_reg))
                break

            elif node_type(statement) == "assign":
                last_reg, sublines = exp_to_IL(r_count, statement.exp)
                r_count[0] -= 1
                lines += sublines
                lines.append("{} = {}".format(statement.var_name.name, last_reg))

            elif node_type(statement) == "if":
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                truth_header = "--> T{}:".format(get_count(counter))
                after_header = "--> A{}:".format(get_count(counter))
                lines.append("ifTrue {} goto {}".format(cond_reg, truth_header[:-1]))
                if statement.else_body.statements:
                    else_header = "--> E{}:".format(get_count(counter))
                    lines.append("ifFalse {} goto {}".format(cond_reg, else_header[:-1]))
                lines.append("goto {}".format(after_header[:-1]))
                lines.append(truth_header)
                convert_body(parent_func, statement.true_body)
                lines.append("goto {}".format(after_header[:-1]))
                if statement.else_body.statements:
                    lines.append(else_header)
                    convert_body(parent_func, statement.else_body)
                    lines.append("goto {}".format(after_header[:-1]))
                lines.append(after_header)
                
            elif node_type(statement) == "while":
                while_header = "--> W{}:".format(get_count(counter))
                lines.append(while_header)
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                after_header = "--> A{}:".format(get_count(counter))
                lines.append("ifFalse {} goto {}".format(cond_reg, after_header[:-1]))
                convert_body(parent_func, statement.true_body)
                lines.append("goto {}".format(while_header[:-1]))
                lines.append(after_header)
                
            elif node_type(statement) == "body":
                convert_body(parent_func, statement)

    counter = [0]
    lines = ["Main:"]
    r_count = [0]
    for function in ast.children:
        if function.name == "main":
            convert_body("main", function.body)
    lines.append("retmain 0")
    return lines

def exp_to_IL(r_count, expression):
    """Returns tuple of generated intermediate-language lines that evaluate
     an expression and name of the register that stores the final value"""
    lines = []
    def helper(exp):
        if node_type(exp) == "expression":
            r1 = helper(exp.oper1)
            r2 = helper(exp.oper2)
            for r in (r1, r2):
                if r[:2] == "_t" and r[2:] and is_int(r[2:]):
                    r_count[0] -= 1
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {} {} {}".format(r_name, r1, exp.op_name, r2))
            return r_name
        elif node_type(exp) == "unaryexpression":
            r = helper(exp.oper)
            if r[:2] == "_t" and r[2:] and is_int(r[2:]):
                r_count[0] -= 1
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {} {}".format(r_name, exp.op_name, r))
            return r_name
        elif node_type(exp) == "const":
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {}".format(r_name, exp.val))
            return r_name
        elif node_type(exp) == "var":
            return exp.name
        else:
            raise Exception("BAD IL")
    last_reg = helper(expression)
    return last_reg, lines

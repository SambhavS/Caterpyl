from astgen import *
import subprocess
"""
-type checking
-how to evaluate expressions
-fix nonspacing for +
-first load functions into namespace
-go through 


"""
def print_IL(lines):
    print()
    for l in lines:
        if l[-1] == ":":
            print(l)
        else:
            print("   {}".format(l))

def print_lst(lst):
    print()
    for i in lst:
        print(i)

def test(): 
    fname = "test.c"
    with open(fname) as f:
        contents = f.read()
    
    ast = main_AST(contents)
    print_tree(ast)
    
    interm_lines = ast_to_IL(ast)   
    print_IL(interm_lines)

    lookup = make_lookup(ast)
    mem_dict = {var:i for i, var in enumerate(lookup.keys())}
    
    assembly = gen_assembly(interm_lines, mem_dict)
    print_lst(assembly)
    write_assembly(fname, assembly)
    run_assembly(fname)


def gen_assembly(interm_lines, mem_dict):
    #deal with need for many vars later
    # use 32bit for everything
    # special registers: rbp (base), rsp (stack), eax (syscall?), edi (return?), r15d(for double memory references)
    # others: ebx, ecx, edx, r8d, r9d, r10d, r11d, r12d, r13d, r14d
    def to_asm(tok):
        if tok in reg_dict:
            return reg_dict[tok]
        elif is_int(tok):
            return "${}".format(tok)
        elif tok in mem_dict:
            return "{}(%rbp)".format(mem_dict[tok] * -8)
        else:
            print(tok)
            raise Exception("Unknown IL token")

    assembly = []
    stack_space = len(mem_dict) * 8
    assembly.append(".global start")
    assembly.append("start:")
    assembly.append("  movq %rsp, %rbp")
    assembly.append("  subq ${}, %rsp".format(stack_space))
    reg_dict = {"_t1": "%ebx",  "_t2": "%ecx",   "_t3": "%edx",  "_t4": "%r8d",
                "_t5": "%r9d",  "_t6": "%r10d",  "_t7": "%r11d", "_t8": "%r12d",
                "_t9": "%r13d", "_t10": "%r14d", "_t11": "%r15d"}
    opers = {"*":"imul", "-":"sub", "+":"add", "/":"div"}

    for line in interm_lines:

        tokens = line.split()
        if len(tokens) == 5:
            if tokens[3] in opers:
                dest, source1, source2 = to_asm(tokens[0]), to_asm(tokens[2]), to_asm(tokens[4])
                instr = opers[tokens[3]]
                assembly.append("  movl {}, %r15d".format(source1))
                assembly.append("  {}  {}, %r15d".format(instr, source2))
                assembly.append("  movl %r15d, {}".format(dest))
            
        elif len(tokens) == 3:
            if tokens[1] == "=":
                source, dest = to_asm(tokens[2]), to_asm(tokens[0])
                if "(" in source and "(" in dest:
                    assembly.append("  movl {}, %r15d".format(source))
                    assembly.append("  movl %r15d, {}".format(dest))
                else:
                    assembly.append("  movl {}, {}".format(source, dest))
        elif len(tokens) == 2:
            if tokens[0] == "retmain":
                source = to_asm(tokens[1])
                assembly.append("  movl {}, %edi".format(source))
                assembly.append("  movl $0x2000001, %eax")
                assembly.append("  syscall")
            elif tokens[0] == "ret":
                # may not work ...
                source = to_asm(tokens[1])
                assembly.append("  movl {}, %edi".format(source))
                assembly.append("  ret")
            else:
                raise Exception("Bad IL Token?")

    assembly.append("  addq ${}, %rsp".format(stack_space))
    return assembly

def ast_to_IL(ast):
    def helper(func_name, body, lines):
        for statement in body.statements:
            if node_type(statement) == "return":
                last_reg, sublines = exp_to_IL(r_count, statement.ret_val)
                lines += sublines
                if func_name == "main":
                    lines += ["retmain {}".format(last_reg)]
                else:
                    lines += ["ret {}".format(last_reg)]
                break
            elif node_type(statement) == "assign":
                last_reg, sublines = exp_to_IL(r_count, statement.exp)
                r_count[0] -= 1
                lines += sublines
                lines += ["{} = {}".format(statement.var_name.name, last_reg)]
            elif node_type(statement) == "if":
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                truth_header = "--> {}:".format(line_counter[0])
                line_counter[0] += 1
                lines += ["ifT {} goto {}".format(cond_reg, truth_header[:-1])]
                truth_lines = [truth_header]
                all_lines.append(truth_lines)
                helper(func_name, statement.true_body, truth_lines)
                if statement.else_body.statements:
                    else_header = "--> {}:".format(line_counter[0])
                    line_counter[0] += 1
                    lines += ["ifF {} goto {}".format(cond_reg, else_header[:-1])]
                    else_lines = [else_header]
                    all_lines.append(else_lines)
                    helper(func_name, statement.else_body, else_lines)
            elif node_type(statement) == "body":
                helper(func_name, statement, lines)

    line_counter = [0]
    main_lines = ["Main:"]
    all_lines = [main_lines]
    r_count = [0]
    for function in ast.children:
        if function.name == "main":
            helper("main", function.body, main_lines)
    main_lines.append("retmain 0")
    interm_lines = [line for lst in all_lines for line in lst]
    return interm_lines

def exp_to_IL(r_count, expression):
    """Generates intermediate-language lines that evaluate an expression 
    and the name of the register that stores the final value"""
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


def make_lookup(ast):
    symb = dict()
    def traverse(tree):
        if hasattr(tree, "children"):
            for child in tree.children:
                traverse(child)
        if node_type(tree) == "decl":
            symb[tree.var.name] = tree.type_dec
    traverse(ast)
    return symb       

def node_type(node):
    return node.__class__.__name__.lower()

def write_assembly(fname, assembly_lines):
    with open("{}.asm".format(fname.split(".")[0]), "w") as f_out:
        for line in assembly_lines:
            f_out.write("{}\n".format(line))

def run_assembly(fname):
    """Run assembly generated by `write_assembly`"""
    f_base = fname.split(".")[0] 
    assemble_link_run = """ as -arch x86_64 -o {0}.o {0}.asm ; 
                            ld -o {0} {0}.o 2> std.err       ; 
                            ./{0} ; echo $?                  ;""".format(f_base)
    return subprocess.call(assemble_link_run, shell=True)  

test()
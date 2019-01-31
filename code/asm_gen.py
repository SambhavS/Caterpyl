from utils import *

def gen_assembly(interm_lines, mem_dict):
    """Converts TAC representation into valid x86_64 assembly. Returns lines of assembly"""

    def to_asm(tok):
        """ Converts individual TAC token to assembly equivelent"""
        if tok in reg_dict:     return reg_dict[tok]
        elif tok in opers:      return opers[tok]
        elif tok in log_ops:    return log_ops[tok]
        elif tok in comps:      return comps[tok]
        elif tok in un_ops:     return un_ops[tok]
        elif is_int(tok):       return "${}".format(tok)
        elif tok in mem_dict:   return "{}(%rbp)".format(mem_dict[tok] * -8)
        else:
            raise Exception("Unknown IL token: {}".format(tok))

    # Define equivalent register names and set up start of assembly file
    assembly = []
    stack_space = len(mem_dict) * 8
    assembly.append("  # Setup stack/base pointer")
    assembly.append(".global start")
    assembly.append("start:")
    assembly.append("  movq %rsp, %rbp")
    assembly.append("  subq ${}, %rsp".format(stack_space))
    reg_dict = {"_t1": "%ebx",  "_t2": "%ecx",   "_t3": "%edx",  "_t4": "%r8d",
                "_t5": "%r9d",  "_t6": "%r10d",  "_t7": "%r11d", "_t8": "%r12d",
                "_t9": "%r13d", "_t10": "%r14d", "_t11": "%r15d"}
    opers = {"*":"imul", "-":"sub", "+":"add", "/":"div"}
    log_ops = {"&&":"and", "||":"or"}
    un_ops = {"!": "not"}
    comps = {"==": "je", "!=": "jne", ">=": "jge", "<=": "jle", "<":  "jl", ">":  "jg"}

    # Convert TAC line by line, by type of statement
    for i, line in enumerate(interm_lines):
        tokens = line.split()
        if len(tokens) == 5:
            if tokens[0] == "ifTrue":
                # Jump iff != 0
                cond_reg, dest = tokens[1], tokens[-1]
                assembly.append("  # IfTrue branch")
                assembly.append("  cmpl $0, {}".format(to_asm(cond_reg)))
                assembly.append("  jne {}".format(dest))
            elif tokens[0] == "ifFalse":
                assembly.append("  # IfFalse branch")
                cond_reg, dest = tokens[1], tokens[-1]
                # Jump iff == 0
                assembly.append("  cmpl $0, {}".format(to_asm(cond_reg)))
                assembly.append("  je {}".format(dest))
            elif tokens[3] in opers:
                assembly.append("  # Arithmetic operation")
                dest, source1, source2 = to_asm(tokens[0]), to_asm(tokens[2]), to_asm(tokens[4])
                instr = to_asm(tokens[3])
                assembly.append("  movl {}, %r15d".format(source1))
                assembly.append("  {}  {}, %r15d".format(instr, source2))
                assembly.append("  movl %r15d, {}".format(dest))
            elif tokens[3] in log_ops:
                assembly.append("  # Logical operation")
                operator = to_asm(tokens[3])
                dest, source1, source2 = to_asm(tokens[0]), to_asm(tokens[2]), to_asm(tokens[4])
                if operator == "and":
                    instr, match, fall_through = "je", 0, 1
                elif operator == "or":
                    instr, match, fall_through = "jne", 1, 0
                assembly.append("  movl {}, %r15d".format(source1))
                assembly.append("  cmp $0, %r15d")
                assembly.append("  {} e{}".format(instr, i))
                assembly.append("  movl {}, %r15d".format(source2))
                assembly.append("  cmp $0, %r15d")
                assembly.append("  {} e{}".format(instr, i))
                assembly.append("  movl ${}, {}".format(fall_through, dest))
                assembly.append("  jmp aft{}".format(i))
                assembly.append("e{}:".format(i))
                assembly.append("  movl ${}, {}".format(match, dest))
                assembly.append("aft{}:".format(i))
                    
            elif tokens[3] in comps:
                assembly.append("  # Checking comparison")
                dest, oper, oper1, oper2 = to_asm(tokens[0]), to_asm(tokens[3]), to_asm(tokens[2]), to_asm(tokens[4])
                assembly.append("  movl {}, %r15d".format(oper1))
                assembly.append("  cmp {}, %r15d".format(oper2))
                assembly.append("  {} e{}".format(oper, i))
                assembly.append("  movl $0, {}".format(dest))
                assembly.append("  jmp aft{}".format(i))
                assembly.append("e{}:".format(i))
                assembly.append("  movl $1, {}".format(dest))
                assembly.append("aft{}:".format(i))
        elif len(tokens) == 4:
            if tokens[2] in un_ops:
                assembly.append("  # Unary operator")
                operator = to_asm(tokens[2])
                dest, operand = to_asm(tokens[0]), to_asm(tokens[3])
                assembly.append("  movl {}, %r15d".format(operand))
                assembly.append("  cmp $0, %r15d")
                assembly.append("  je e{}".format(i))
                assembly.append("  movl $0, {}".format(dest))
                assembly.append("  jmp aft{}".format(i))
                assembly.append("e{}:".format(i))
                assembly.append("  movl $1, {}".format(dest))
                assembly.append("aft{}:".format(i))




        elif len(tokens) == 3:
            if tokens[1] == "=":
                assembly.append("  # Assignment")
                source, dest = to_asm(tokens[2]), to_asm(tokens[0])
                if "(" in source and "(" in dest:
                    assembly.append("  movl {}, %r15d".format(source))
                    assembly.append("  movl %r15d, {}".format(dest))
                else:
                    assembly.append("  movl {}, {}".format(source, dest))
            elif tokens[0] == "goto":
                assembly.append("  # Goto")
                dest = tokens[-1]
                assembly.append("  jmp {}".format(dest))

        elif len(tokens) == 2:
            if tokens[0] == "retmain":
                assembly.append("  # Return out of `main`")
                source = to_asm(tokens[1])
                assembly.append("  movl {}, %edi".format(source))
                assembly.append("  movl $0x2000001, %eax")
                assembly.append("  syscall")
            elif tokens[0] == "ret":
                # needs work for non-main functions
                source = to_asm(tokens[1])
                assembly.append("  movl {}, %edi".format(source))
                assembly.append("  ret")
            elif tokens[0] == "-->":
                label = tokens[-1]
                assembly.append(label)
                

    assembly.append("  addq ${}, %rsp".format(stack_space))
    return assembly

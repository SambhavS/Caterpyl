from utils import *

def gen_assembly(interm_lines, mem_dict):
    """Converts TAC representation into valid x86_64 assembly. Returns lines of assembly"""

    def to_asm(tok):
        """ Converts individual TAC token to assembly equivelent"""
        if tok in reg_dict:
            return reg_dict[tok]
        elif is_int(tok):
            return "${}".format(tok)
        elif tok in mem_dict:
            return "{}(%rbp)".format(mem_dict[tok] * -8)
        else:
            print(tok)
            raise Exception("Unknown IL token")

    # Define equivalent register names and set up start of assembly file
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

    # Convert TAC line by line, by type of statement
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

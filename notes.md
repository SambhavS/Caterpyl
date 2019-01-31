# Todo
-add functions
-add loops
-type checking
-fix nonspacing for +
-namespace for functions? 
-deal with many variables in ASM_gen (insufficient registers)

//We skip non-parsable tokens proactively for parse_statements & statement_AST, but not for expression_AST


# Call assembly
as -arch x86_64 -o test.o test.asm ;
ld -o test test.o 2> std.err ; ./test ; echo $?

# Register allocation
special registers: rbp (base), rsp (stack), eax (syscall?), edi (return?), r15d(for double memory references)
others: ebx, ecx, edx, r8d, r9d, r10d, r11d, r12d, r13d, r14d
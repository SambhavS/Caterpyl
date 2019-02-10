# Todo
- *temp storage*
- lists? 
- break/continue
- void functions
- type checking
- optimization


# Call assembly
as -arch x86_64 -o test1.o test1.asm ;
ld -o test1 test1.o 2> std.err ; ./test1 ; echo $?

# Register allocation
special registers: rbp (base), rsp (stack), eax (syscall?), edi (return?), r15d(for double memory references), rsi ()
others: ebx, ecx, edx, r8d, r9d, r10d, r11d, r12d, r13d, r14d
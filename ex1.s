.section	__TEXT,__text,regular,pure_instructions
.macosx_version_min 10, 13
.global start
#
start:
  movq %rsp, %rbp          # copy stack pointer to base pointer
  subq $64, %rsp 		   # allocate 16 bytes of memory
  movl $10, %r8d		   # store 10 in ebx	
  movl %r8d, -8(%rbp)	   # store ebx (10) on stack
  movl -8(%rbp), %ecx      # get stack value (10) and put in ecx
  addq $64, %rsp
  movl %ecx, %edi	       # load return value
  movl $0x2000001, %eax    # load exit val for syscall
  syscall                  # make syscall to exit

  # Setup stack/base pointer
.global start
start:
  movq %rsp, %rbp
  subq $8, %rsp
  # Assignment
  movl $0, %ebx
  # Unary operator
  movl %ebx, %r15d
  cmp $0, %r15d
  je e2
  movl $0, %ebx
  jmp aft2
e2:
  movl $1, %ebx
aft2:
  # Assignment
  movl %ebx, 0(%rbp)
  # Return out of `main`
  movl 0(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  # Return out of `main`
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
  addq $8, %rsp

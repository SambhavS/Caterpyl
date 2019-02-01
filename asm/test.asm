  # Setup stack/base pointer
.global start
start:
  movq %rsp, %rbp
  subq $24, %rsp
  # Assignment
  movl $1, %r8d
  # Assignment
  movl %r8d, 0(%rbp)
  # Assignment
  movl $2, %r8d
  # Assignment
  movl %r8d, -8(%rbp)
  # Arithmetic operation
  movl 0(%rbp), %r15d
  add  -8(%rbp), %r15d
  movl %r15d, %r8d
  # Assignment
  movl %r8d, -16(%rbp)
  # Return out of `main`
  movl -16(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  # Return out of `main`
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
  addq $24, %rsp

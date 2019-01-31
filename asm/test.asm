  # Setup stack/base pointer
.global start
start:
  movq %rsp, %rbp
  subq $8, %rsp
  # Assignment
  movl $1, %ebx
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

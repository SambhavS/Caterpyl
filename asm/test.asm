  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  subq $52, %rsp
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, 0(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -4(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -8(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -12(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -16(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -20(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -24(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -28(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -32(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -36(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -40(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -44(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -48(%rbp)
  movl 0(%rbp), %r15d
  add  -4(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, %r15d
  add  -8(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, %r15d
  add  -12(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, %r15d
  add  -16(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, %r15d
  add  -20(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, %r15d
  add  -24(%rbp), %r15d
  movl %r15d, %r9d
  # end
  addq $52, %rsp
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  # end
  addq $52, %rsp
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
bar:
  movl $1, %r10d
  movl %r10d, %edi
  ret
  movl $0, %edi
  ret

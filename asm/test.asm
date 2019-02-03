  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  subq $8, %rsp
  movl $3, %r9d
  # popParamSpace
  addq $4, %rsp
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r9d, 0(%rsp)
  call triple
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r10d
  movl %r10d, 0(%rbp)
  movl $4, %r10d
  # popParamSpace
  addq $4, %rsp
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r10d, 0(%rsp)
  call triple
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r11d
  movl %r11d, -4(%rbp)
  # end
  addq $8, %rsp
   
   
  movl 0(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  # end
  addq $8, %rsp
   
   
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
triple:
  subq $4, %rsp
  # end
  addq $4, %rsp
  movl -4(%rbp), %edi
  ret
  # end
  addq $4, %rsp
  movl $0, %edi
  ret

  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $33, %r9d
  #----------
  subq $8, %rsp
  subq $8, %rsp
  movl %r9d, %r15d
  movl %r15d, 0(%rsp)
  movq %rbp, 8(%rsp)
  movq %rsp, %rbp
  call foo
  movq %rbp, %rsp
  movq 8(%rsp), %rbp
  addq $8, %rsp
  addq $8, %rsp
  movl %edi, %r9d
  #----------
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
foo:
  movl $1, %r10d
  movl $4, %r11d
  #----------
  subq $8, %rsp
  subq $8, %rsp
  movl %r11d, %r15d
  movl %r15d, 0(%rsp)
  subq $8, %rsp
  movl %r10d, %r15d
  movl %r15d, 0(%rsp)
  subq $8, %rsp
  movl 0(%rbp), %r15d
  movl %r15d, 0(%rsp)
  movq %rbp, 24(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 24(%rsp), %rbp
  addq $8, %rsp
  addq $24, %rsp
  movl %edi, %r9d
  #----------
  movl %r9d, %edi
  ret
  movl $0, %edi
  ret
bar:
  movl 8(%rbp), %r15d
  add  16(%rbp), %r15d
  movl %r15d, %r10d
  #----------
  subq $8, %rsp
  subq $8, %rsp
  movl %r10d, %r15d
  movl %r15d, 0(%rsp)
  subq $8, %rsp
  movl 0(%rbp), %r15d
  movl %r15d, 0(%rsp)
  movq %rbp, 16(%rsp)
  movq %rsp, %rbp
  call zoo
  movq %rbp, %rsp
  movq 16(%rsp), %rbp
  addq $8, %rsp
  addq $16, %rsp
  movl %edi, %r9d
  #----------
  movl %r9d, %edi
  ret
  movl $0, %edi
  ret
zoo:
  movl $77, %r10d
  movl %r10d, %edi
  ret
  movl $0, %edi
  ret

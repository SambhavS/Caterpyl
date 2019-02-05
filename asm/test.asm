  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call foo
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r9d
  addq $4, %rsp
  #----------
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
foo:
  movl $1, %r10d
  movl $2, %r11d
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r11d, %r15d
  movl %r15d, 0(%rsp)
  subq $4, %rsp
  movl %r10d, %r15d
  movl %r15d, 0(%rsp)
  call max
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r10d
  addq $4, %rsp
  #----------
  addq $8, %rsp
  movl %r10d, %edi
  ret
  movl $0, %edi
  ret
max:
  subq $8, %rsp
  movl -8(%rbp), %r15d
  cmp -4(%rbp), %r15d
  jg e17
  movl $0, %r11d
  jmp aft17
e17:
  movl $1, %r11d
aft17:
  cmpl $0, %r11d
  jne T1
  jmp A2
T1:
  addq $8, %rsp
  movl -8(%rbp), %edi
  ret
  jmp A2
A2:
  addq $8, %rsp
  movl -4(%rbp), %edi
  ret
  addq $8, %rsp
  movl $0, %edi
  ret

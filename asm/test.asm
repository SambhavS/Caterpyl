  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $10, %r9d
  movl $20, %r10d
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r10d, 0(%rsp)
  subq $4, %rsp
  movl %r9d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r9d
  addq $4, %rsp
  #----------
  addq $8, %rsp
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
fact:
  subq $8, %rsp
  movl $1, %r10d
  movl -8(%rbp), %r15d
  cmp %r10d, %r15d
  je e14
  movl $0, %r10d
  jmp aft14
e14:
  movl $1, %r10d
aft14:
  cmpl $0, %r10d
  jne T1
  jmp A2
T1:
  movl $1, %r10d
  movl %r10d, %r15d
  add  -4(%rbp), %r15d
  movl %r15d, %r10d
  addq $8, %rsp
  movl %r10d, %edi
  ret
  jmp A2
A2:
  movl $1, %r11d
  movl -8(%rbp), %r15d
  sub  %r11d, %r15d
  movl %r15d, %r11d
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl -4(%rbp), 0(%rsp)
  subq $4, %rsp
  movl %r11d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r10d
  addq $4, %rsp
  #----------
  addq $8, %rsp
  movl -8(%rbp), %r15d
  imul  %r10d, %r15d
  movl %r15d, %r10d
  addq $8, %rsp
  movl %r10d, %edi
  ret
  addq $8, %rsp
  movl $0, %edi
  ret

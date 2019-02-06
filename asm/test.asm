  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $5, %r9d
  #----------
  subq $4, %rsp
  movq %rbp, -4(%rsp)
  subq $4, %rsp
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r9d, %r15d
  movl %r15d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  addq $4, %rsp
  movq -4(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  subq $4, %rsp
  #----------
  addq $4, %rsp
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
fact:
  subq $4, %rsp
  movl $1, %r10d
  movl -4(%rbp), %r15d
  cmp %r10d, %r15d
  je e11
  movl $0, %r10d
  jmp aft11
e11:
  movl $1, %r10d
aft11:
  cmpl $0, %r10d
  jne T1
  jmp A2
T1:
  movl $1, %r10d
  addq $4, %rsp
  movl %r10d, %edi
  ret
  jmp A2
A2:
  movl $1, %r11d
  movl -4(%rbp), %r15d
  sub  %r11d, %r15d
  movl %r15d, %r11d
  #----------
  subq $4, %rsp
  movq %rbp, -4(%rsp)
  subq $4, %rsp
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r11d, %r15d
  movl %r15d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  addq $4, %rsp
  movq -4(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r11d
  subq $4, %rsp
  #----------
  addq $4, %rsp
  movl $3, %r12d
  movl %r11d, %r15d
  imul  %r12d, %r15d
  movl %r15d, %r11d
  addq $4, %rsp
  movl %r11d, %edi
  ret
  addq $4, %rsp
  movl $0, %edi
  ret

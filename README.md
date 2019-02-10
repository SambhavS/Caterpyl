# Caterpyl

Caterpyl is a compiler I'm writing from scratch to compile a core subset of C into x86_64 assembly.

Currently, it has the following features:
- user defined functions (like `int my_func(){return 123;}`)
- type declaration checking
- two types: `int` and `bool` (modified language slightly to support `True` and `False` instead of `1` and `0` as booleans)
- variables, literals, expressions 
  
  (like `int x = 10;` and `int y = (2 * 10 + 7 * (3 + 1)) - 200;` and `bool broken = False;`)
- boolean operators (`&&`, `||`, `!`)
- arithmetic operators (`+`, `*`, `-`, `/`, `%`)
- comparators (eg. `==`, `<`, `>`, `<=`, `>=`, `!=`)
- control structures (`if`, `else`, `while`)
- comments (start with `//`)

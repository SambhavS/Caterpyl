# Caterpyl

Caterpyl is a compiler I'm writing from scratch to compile Decaf, a C like language, into x86_64 assembly.

Currently, it has the following features:
- user defined functions (like `int my_func(){return 123;}`)
- type declaration checking
- two types: `int` and `bool`
- variables, literals, expressions 
  (like `int x = 10;` and `int y = (2 * 10 + 7 * (3 + 1)) - 200;` and `bool broken = False`)
- boolean operators (`&&`, `||`, `!`)
- arithmetic operators (`+`, `*`, `-`, `/`, `%`)
- comparators (eg. `==`, `<`, `>`, `<=`, `>=`, `!=`)
- control structures (`if`, `else`, `while`)
- comments (start with `//`)

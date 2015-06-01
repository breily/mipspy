# Description: Computes the Fibonacci function using a recursive process.
# Function:         F(n) = 0, if n = 0;
#                          1, if n = 1;
#                          F(n-1) + F(n-2), otherwise.
# Output:           F(n).

# Register usage:
#  $a0 = n (passed directly to fib)
#  $s1 = f(n)
        .data
        .align 2

descr:  .text
    .align 2
    .globl __start

__start:

# Value of N

    ori $v0,$0,0x9
    move $a0, $v0           # $a0 = n
    jal fib             # call fib(n)
    move $s1, $v0           # $s1 = fib(n)

# Print result

    li $v0, 1           # print_int system service ...
    move $a0, $s1           # ... passing argument fib(n)
    syscall

# Call system - exit
    li $v0, 10
    syscall

# Register usage:
#  $a0 = n (argument)
#  $t1 = fib(n-1)
#  $t2 = fib(n-2)
#  $v0 = 1 (for comparison)

# Stack usage:
# 1. push return address, n, before calling fib(n-1)
# 2. pop n
# 3. push n, fib(n-1), before calling fib(n-2)
# 4. pop fib(n-1), n, return address

fib:    bne $a0, $zero, fibne0      # if n == 0 ...
    move $v0, $zero         # ... return 0
    jr $31

fibne0:                 # Assert: n != 0
    li $v0, 1
    bne $a0, $v0, fibne1        # if n == 1 ...
    jr $31              # ... return 1

fibne1:                 # Assert: n > 1
## Compute fib(n-1)
    addi $sp, $sp, -8       # push ...
    sw $ra, 4($sp)          # ... return address
    sw $a0, 0($sp)          # ... and n
    addi $a0, $a0, -1       # pass argument n–1 ...
    jal fib                 # ... to fib
    move $t1, $v0           # $t1 = fib(n–1)
    lw $a0, 0($sp)          # pop n
    addi $sp, $sp, 4        # ... from stack


## Return fib(n-1) + fib(n-2)
    add $v0, $t1, $t2       # $v0 = fib(n) = fib(n–1) + fib(n–2)
    jr $31              # return to caller

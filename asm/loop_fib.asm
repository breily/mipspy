.text
.globl __start

__start:
    addi $a0, $0, 9
    jal fib
    move $s0, $v0
    addi $v0, $0, 10
    syscall

fib:
    bne $a0, $0, not_zero
    add $v0, $0, $0
    jr $ra
not_zero:
    add $t0, $0, $0
    addi $t1, $0, 1
    addi $t2, $0, 2
    addi $a0, $a0, 1
loop:
    beq $a0, $t2, exit_loop
    move $t7, $t1
    add $t1, $t1, $t0
    move $t0, $t7
    addi $t2, $t2, 1
    j loop
exit_loop:
    move $v0, $t1
    jr $ra

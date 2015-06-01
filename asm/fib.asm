    ori $a0, $0, 9  # Call fib(9)
    jal fib
    move $s1, $v0
    li $v0, 1       # Print result
    move $a0, $s1
    syscall
    li $v0, 10      # Exit
    syscall
fib:
    bne $a0, $zero, fibne0
    move $v0, $zero
    jr $31
fibne0:
    li $v0, 1
    bne $a0, $v0, fibne1
    jr $31
fibne1:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
    addi $a0, $a0, -1
    jal fib
    move $t1, $v0
    lw $a0, 0($sp)
    addi $sp, $sp, 4

    add $v0, $t1, $t2
    jr $31

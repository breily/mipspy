.text
.globl __start

__start:
    ori $s7, $0, 0x1000
    sll $s7, $s7, 16

    ori $s0, $0, 0xdead
    sll $s0, $s0, 16
    ori $s0, $s0, 0xbeef

    sw $s0, 0($s7)
    sw $s0, 4($s7)
    sw $s0, 8($s7)
    sw $s0, 12($s7)
    sw $s0, 16($s7)
    sw $s0, 20($s7)
    sw $s0, 24($s7)

    move $a0, $s7
    move $a1, $s7
    addi $a1, $a1, 24

    jal reverse
    move $s1, $v0
    addi $v0, $0, 10
    syscall


reverse:
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    move $t6, $a0
    move $t7, $a1
    #jal aligned
    bne $v0, $0, later
    move $a0, $t7
    #jal aligned
later:
    slt $t5, $t6, $t7
    bne $t5, $0, correct_order
    move $t5, $t6
    move $t6, $t7
    move $t7, $t5
correct_order:
    addi $t7, $t7, 4
loop:
    beq $t6, $t7, x_loop
    lbu $t0, 0($t6)
    lbu $t1, 1($t6)
    lbu $t2, 2($t6)
    lbu $t3, 3($t6)
    sll $t0, $t0, 24
    sll $t1, $t1, 16
    sll $t2, $t2, 8
    or $t0, $t0, $t1
    or $t0, $t0, $t2
    or $t0, $t0, $t3
    sw $t0, 0($t6)
    addi $t6, $t6, 4
    j loop
x_loop:
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra

aligned:
    sll $t0, $a0, 30
    beq $t0, $0, yes_align
    addi $v0, $0, -1
    jr $ra
yes_align:
    add $v0, $0, $0
    jr $ra

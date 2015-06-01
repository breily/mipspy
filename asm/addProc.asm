# test procedure
       .text                   # assembler dir to identify code
                               # can only include instructions or .word

       .globl __start          #

__start:

       addi $a0,$0,1           # load 1 into $a0
       addi $a1,$0,2           # load 2 into $a1
       addi $a2,$0,3           # load 3 into $a2
       addi $a3,$0,4           # load 4 into $a3

       jal add4                # call the procedure

       add $a0,$0,$v0          # display the result
       li $v0, 1
       syscall
       la $a0,newl
       li $v0, 4
       syscall

       addi $a0,$0,1      	#start add4_2
       addi $a1,$0,2
       addi $a2,$0,3
       addi $a3,$0,4

       jal add4_2

       add $a0,$0,$v0
       li $v0, 1
       syscall
       la $a0,newl
       li $v0, 4
       syscall

       li $v0, 10
       syscall

add4:
       move $t0, $s0
       add $s0,$a0,$a1
       add $t1,$a2,$a3
       add $v0,$s0,$t1
       move $s0, $t0
       jr $ra

add4_2:
       addi $sp, $sp, -4       # preserve $s0
       sw $s0, 0($sp)

       add $s0,$a0,$a1
       add $t1,$a2,$a3
       add $v0,$s0,$t1

       lw $s0, 0($sp)
       addi $sp, $sp, 4

       jr $ra                  # return

.data
newl:   .asciiz "\n"

## end of file

#  This c code is what your assembly code should do
#
#  #include <iostream.h>
#
#  main() {
#    int a[] = {36, 20, 27, 15, 1, 62, 41};
#    int n = 7;
#    int max, i;
#
#    for (max = i = 0; i<n; i++)
#      if (a[i] > max)
#        max = a[i];
#
#    cout << max << endl;
#  }


	.text
	.globl __start

__start:
	li $t0, 0		# i in $t0
	li $s0, 0		# max in $s0
	lw $s1, n		# n in $s1

	li $v0, 1		# print the max value
	syscall
	li $v0, 10		# exit
	syscall

	.data
a:	.word 36, 20, 27, 15, 1, 62, 41
n:	.word 7
max:	.word 0

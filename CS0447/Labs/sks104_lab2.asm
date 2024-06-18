# Stephen Skasko
# sks104

# preserves a0, v0

.macro print_str %str
	.data
	print_str_message: .asciiz %str
	.text
	push a0
	push v0
	la a0, print_str_message
	li v0, 4
	syscall
	pop v0
	pop a0	
.end_macro
	
# variables
.data 
	
	display: .word 0
	operation: .byte 0
		
.text
		
			
.globl main
main:
	print_str "Welcome to CALCY THE CALCULATOR!\n"
	
	# while(true) {
	_loop:
	

			lw a0, display

				
			li v0, 1
			syscall
			
			print_str "\nOperation (=,+,-,*,/,c,q): "
			
			# == operation = v0
			li v0, 12
			syscall
			sb v0, operation
		
# switch(operation) {
	lb  t0, operation
	beq t0, 'q', _quit
	beq t0, 'c', _clear
	beq t0, '+', _get_operand
	beq t0, '-', _get_operand
	beq t0, '*', _get_operand
	beq t0, '/', _get_operand
	beq v0, '=', _get_operand
	j   _default

	# indentation is not *required* in asm, but it can be helpful.

	# case 'q':
	_quit:
		print_str "\n"
		
		li v0, 10
		syscall
		
		
		

	# case 'c'
	_clear:
		print_str "\n"
		sw zero, display
		j _break
	
	

	

	# Operands
	_get_operand: 
		
		

		
		
		print_str "\nValue: "
		li v0, 5
		syscall
		
		# Switch Operation
		lb t0, operation
		beq t0, '+', _add
		beq t0, '-', _subtract
		beq t0, '*', _times
		beq t0, '/', _divide

	_add: 
	
		lw t0, display
		sw v0, display
		j _break

	_subtract: 
		
		lw t0, display
		sw v0, display
		j _break
		
	_times: 
	
		lw t0, display
		sw v0, display
		j _break
		
	_divide: 
	
		bne v0, 0, _else
		print_str "Attempting to divide by 0!\n"
		
		j _endif

		_else: 
		
			sw v0, display
			j _break
		
		_endif:
			
			lw t0, display
			j _break
			
		
	# default:
	_default:
		print_str "Huh?\n"
		
		
		
		
		
		# no j _break needed cause it's the next line.
_break:
	# }

	# this "j _loop" is already here!
	j _loop
	

     		

		
			

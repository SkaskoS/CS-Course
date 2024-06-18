# Stephen Skasko
# sks104

# preserves a0, v0
.macro print_str %str
	# DON'T PUT ANYTHING BETWEEN .macro AND .end_macro!!
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

# -------------------------------------------
.eqv ARR_LENGTH 5
.data
	arr: .word 100, 200, 300, 400, 500
	message: .asciiz "testing!"
	message2: .asciiz "argument!"
.text

# -------------------------------------------
.globl main

main:

	jal input_arr
	jal print_arr
	
	#print chars(message)
	la a0, message
	jal print_chars
	
	
	la a0, message2
	jal print_chars
	
	
	
	# exit()
	li v0, 10
	syscall 
	
# -------------------------------------------

input_arr:
    
    	push ra

     	li  t0, 0
 
 _loop:
     
    
    	print_str "enter value: "
	
	move  v0, t0
	li v0, 5
   	syscall
	
		
		
	la  t1, arr
	mul t2, t0, 4
	add t1, t1, t2
	sw  v0, (t1)

   	
	#increments the loop
	add t0, t0, 1
	#is the t< or equal to 0
	blt t0, ARR_LENGTH, _loop
	
	

    	pop ra
    	jr ra

 	  
# -------------------------------------------

print_arr:
	push ra
  	# all the code will go here
  	 
  	  
	li  t0, 0
	
_loop:
	
	print_str "arr["
	
	#moves copies between registers 
	move a0, t0
	li v0, 1
   	syscall

	print_str "] = "
			
	la  t1, arr
	mul a0, t0, 4  
	add t1, t1, a0
	lw  a0, (t1)

	li v0, 1
   	syscall
	
	print_str "\n"
	
	#increments the loop
	add t0, t0, 1
	#is the t< or equal to 0
	blt t0, ARR_LENGTH, _loop

	pop ra
 	jr ra
 	  
 	  
# -------------------------------------------

print_chars:

	push ra
	# all the code will go here
	li  t0, 0
	move t0, a0
	
	

_loop:
   	lb a0, (t0)       # a0 = *t0 (read as "value-at t0")
    	beq a0, 0, _break # if a0 == 0, exit the loop
    
	# 1. now use the print_char syscall to print what's in a0'
	li v0, 11
	syscall
	# 2. and then print a newline
	print_str "\n"
	# 3. finally, increment t0
	add t0, t0, 1
	blt t0, ARR_LENGTH, _loop

    
    j _loop
_break:
  

	
	pop ra
 	jr ra

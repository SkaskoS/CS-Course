# Stephen Skasko
# sks104

.include "lab4_include.asm"

.data
	# variables go here!
	dotX: .word 32
	dotY: .word 32
	curDot: .word 0
	


.text
.globl main
main:
	# when done at the beginning of the program, clears the display
	# because the display RAM is all 0s (black) right now.
	jal display_update

	_loop:
		# code goes here!'
		jal check_input
		jal draw_dot
		jal display_update
		jal sleep



		
	j _loop

_exit:
	# exit()
	li v0, 10
	syscall
	

check_input:
push ra

	lw t0, DISPLAY_KEYS
	and t0, t0, KEY_R
	beq t0, 0, _endif_r
	
	#dot++
	lw t0, dotX
	add t0, t0, 1
	sw t0, dotX
	_endif_r:
	

		
	lw t0, DISPLAY_KEYS
	and t0, t0, KEY_L
	beq t0, 0, _endif_l
	
	#dot--
	lw t0, dotX
	sub t0, t0, 1
	sw t0, dotX
	_endif_l:
	
	#two more times just change the keys
	lw t0, DISPLAY_KEYS
	and t0, t0, KEY_D
	beq t0, 0, _endif_d
	
	#dot++
	lw t0, dotY
	add t0, t0, 1
	sw t0, dotY
	
	
	lw t0, dotY
	and t0, t0, 63
	sw t0, dotY
	
	_endif_d:
	
	
		
	lw t0, DISPLAY_KEYS
	and t0, t0, KEY_U
	beq t0, 0, _endif_u
	
	
	#dot--
	lw t0, dotY
	sub t0, t0, 1
	sw t0, dotY
	
	_endif_u:
	
		
		lw t0, dotY
		and t0, t0, 63
		sw t0, dotY
		
		lw t0, dotX
		and t0, t0, 63
		sw t0, dotX
		
pop ra 
jr ra


draw_dot:

push ra


	lw t0, dotY
	mul t0, t0, 64
	lw t1, dotX
	add t0, t0, t1
	add t0, t0, DISPLAY_BASE
	
	#T1 = COLOR purple
	li t1, COLOR_BLUE #CONSTANTS
	
	#store purple into Display
	sb t1, (t0)
	
	


	lw t0, dotY
	mul t0, t0, 64
	lw t1, dotX
	add t0, t0, t1
	add t0, t0, DISPLAY_BASE
	
	#T1 = COLOR purple
	li t1, COLOR_BLUE #CONSTANTS
	
	#store purple into Display
	sb t1, (t0)
	
#step#4
        li  t2, 0
        
        

_loop:


	    lw t2, curDot
	    bne t3, t2, _else

	
	
	        
	    lw t0, dotY
	    mul t0, t0, 64
	    lw t1, dotX
	    add t0, t0, t1
	    add t0, t0, DISPLAY_BASE
	        
	    #T1 = COLOR 
	    li t1, COLOR_WHITE #CONSTANTS
	    
	    #store  color into Display
	    sb t1, (t0) 
	    
	    
j _endif

_else:
	    lw t7, dotY
	    mul t7, t7, 64
	    lw t8, dotX
	    add t7, t7, t8
	    add t7, t7, DISPLAY_BASE
	        
	    #T1 = COLOR 
	    li t8, COLOR_WHITE #CONSTANTS
	    
	    #store  color into Display
	    sb t8, (t7) 
	    
_endif:
	
	      add t1, t1, 1
	      blt t1, 3, _loop
	     
	    
	    
pop ra
jr ra


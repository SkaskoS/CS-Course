#Stephen Skakso
#sks104
#if use t registers with jr, it would be unreconizable 

.include "display_2211_0822.asm"
.include "math.asm"

# Player constants
.eqv PLAYER_X_START 0x1D00 # 30.0
.eqv PLAYER_Y_START 0x3200 # 50.0
.eqv PLAYER_X_MIN   0x0200 # 2.0
.eqv PLAYER_X_MAX   0x3900 # 57.0
.eqv PLAYER_Y_MIN   0x2E00 # 46.0
.eqv PLAYER_Y_MAX   0x3900 # 57.0
.eqv PLAYER_W       0x0500 # 5.0
.eqv PLAYER_H       0x0500 # 5.0
.eqv PLAYER_VEL     0x0100 # 1.0

# Bullet constants
.eqv BULLET_COLOR   COLOR_WHITE
.eqv MAX_BULLETS    10 # size of the bullet arrays
.eqv BULLET_DELAY   25 # frames
.eqv BULLET_VEL     0x0180 # 1.5

# Rock constants
.eqv ROCKS_TO_DESTROY 10
.eqv MAX_ROCKS        10
.eqv ROCK_VEL         0x0080 # 0.5 pixels/frame
.eqv ROCK_W           0x0500 # 5.00
.eqv ROCK_H           0x0500 # 5.00
.eqv ROCK_MAX_X       0x4000 # 64.0
.eqv ROCK_MAX_Y       0x4000 # 64.0
.eqv ROCK_DELAY       45 # frames
.eqv ROCK_MIN_ANGLE   115
.eqv ROCK_ANGLE_RANGE 110

.data

# Player variables
player_x:         .word PLAYER_X_START
player_y:         .word PLAYER_Y_START
player_next_shot: .word 0
player_lives:     .word 3
rocks_left:       .word ROCKS_TO_DESTROY

# Bullet variables
bullet_x:         .word 0:MAX_BULLETS
bullet_y:         .word 0:MAX_BULLETS
bullet_active:    .byte 0:MAX_BULLETS

# Rock variables
rock_x:           .word 0:MAX_ROCKS
rock_y:           .word 0:MAX_ROCKS
rock_vx:          .word 0:MAX_ROCKS
rock_vy:          .word 0:MAX_ROCKS
rock_active:      .byte 0:MAX_ROCKS
rock_next_spawn:  .word 0

# Sprites
player_sprite: .byte
-1 -1  4 -1 -1
-1  4  7  4 -1
 4  7  7  7  4
 4  4  4  4  4
 4 -1  2 -1  4

rock_sprite: .byte
-1 11 11 11 -1
11 11 11 11 11
11 11 11 11 11
11 11 11 11 11
-1 -1 11 11 11

.text

# -------------------------------------------------------------------------------------------------

.globl main
main:
	jal wait_for_start

	_loop:
		# TODO: uncomment these and implement them
		jal check_input
		jal update_all
		jal draw_all
		jal display_update_and_clear
		jal wait_for_next_frame
	jal check_game_over
	beq v0, 0, _loop
syscall_exit

# -------------------------------------------------------------------------------------------------

wait_for_start:
enter
	_loop:
		jal draw_all
		jal display_update_and_clear
		jal wait_for_next_frame
	jal input_get_keys_pressed
	beq v0, 0, _loop
_return:
leave

# -------------------------------------------------------------------------------------------------

check_game_over:
enter
	li  v0, 1
	lw  t0, player_lives
	beq t0, 0, _return
	lw  t0, rocks_left
	beq t0, 0, _return
	li  v0, 0
_return:
leave

# -------------------------------------------------------------------------------------------------

draw_all:
enter
	# TODO: uncomment and implement these
	jal draw_rocks
	jal draw_bullets
	jal draw_player
	jal draw_hud
leave

# -------------------------------------------------------------------------------------------------

draw_hud:
enter
	# hide our shame :^)
	li a0, 0
	li a1, 0
	li a2, 64
	li a3, 7
	li v1, COLOR_DARK_GREY
	jal display_fill_rect

	# display rocks left
	li a0, 1
	li a1, 1
	lw a2, rocks_left
	jal display_draw_int

	# display lives left
	li a0, 45
	li a1, 1
	la a2, player_sprite
	jal display_blit_5x5_trans

	li a0, 51
	li a1, 1
	li a2, '='
	jal display_draw_char

	li a0, 57
	li a1, 1
	lw a2, player_lives
	jal display_draw_int
leave

#------------------------------------------------------------

draw_player:
enter
	lw a0, player_x
	sra a0, a0, 8
	lw a1, player_y
	srl a1, a1, 8
	la a2, player_sprite
	jal display_blit_5x5_trans
		

leave
# -----------------------------------------------------------

check_input:
enter
	jal input_get_keys_held
	
	# if(v0 & key_l) left
	and t0, v0, KEY_L
	beq t0, 0, _endif_l
	
		#player_x -= PLater_vel
		lw t0 player_x
		sub t0, t0, PLAYER_VEL
		maxi t0, t0, PLAYER_X_MIN
		sw t0, player_x
		
	_endif_l:
	
	
	# if(v0 & key_r)
	and t0, v0, KEY_R
	beq t0, 0, _endif_r
	
		#player_x += PLater_vel
		lw t0 player_x
		add t0, t0, PLAYER_VEL
		mini t0, t0, PLAYER_X_MAX
		sw t0, player_x
	_endif_r:
	
	
	# if(v0 & key_D)
	and t0, v0, KEY_D
	beq t0, 0, _endif_d
	
		#player_x += PLater_vel
		lw t0 player_y
		add t0, t0, PLAYER_VEL
		mini t0, t0, PLAYER_Y_MAX
		sw t0, player_y
	_endif_d:
	# if(v0 & key_U)
	and t0, v0, KEY_U
	beq t0, 0, _endif_u
	
		#player_x -= PLater_vel
		lw t0 player_y
		sub t0, t0, PLAYER_VEL
		maxi t0, t0, PLAYER_Y_MIN
		sw t0, player_y
	_endif_u:

	# fire_bullet
	and t0, v0, KEY_Z
	beq t0, 0, _endif_z
	
		
		jal fire_bullet
		
_endif_z:
leave

# ----------------------------------------------

fire_bullet:
enter
	
	
		
	lw t0 frame_counter
	lw t1, player_next_shot
	
	blt t0, t1, _break
	add t0, t0, BULLET_DELAY
	
	sw t0, player_next_shot
	
		
	        jal find_free_bullet
	        blt v0, zero, _break
	        li t1, 1
	        sb t1, bullet_active(v0) # bullet_active[v0] = 1
	        
	        mul t4, v0, 4 # t4 = v0 * 4
	    
	        lw  t2, player_x
	        add t5, t2, 0x200    
	        sw  t5, bullet_x(t4) 
	    
	        lw  t3, player_y
	        sub t6, t3, 0x100    
	        sw  t6, bullet_y(t4) 
		        
_break:	
leave
	

#-------------------------------------------------

find_free_bullet:		
enter
        li t0, 0
_loop:
        # if bullet_active[t0] == 0
        lb t1, bullet_active(t0)
        bne t1, 0, _endif
        
            # return t0
            move v0, t0
            j _return
        
	_endif: 
    
   	add t0, t0, 1
    	blt t0, MAX_BULLETS, _loop

    # here, we got out of the loop without finding a free slot,
    # so we return -1.
    li v0, -1

_return:
leave
#-------------------------------------------------

draw_bullets:
enter s0 # if you want to use s0, you have to declare it on the enter and leave.

    # for s0 = 0 to MAX_BULLETS
    	li s0, 0
_loop:
        # here is where you check if bullet_active(s0), and then set the pixel if so
	lb t2, bullet_active(s0)
	beq t2, 0, _inactive # if t2 == 0, go to _inactive
		
		#println_str "drawing a bullet"
   		mul t0, s0, 4 # t0 = s0 * 4, have to do this because bullet_x/y are word arrays
                lw  a0, bullet_x(t0)
                lw  a1, bullet_y(t0)
                sra a0, a0, 8
                sra a1, a1, 8
                li a2, BULLET_COLOR    
                jal display_set_pixel
    
	_inactive:
    
	add s0, s0, 1
	blt s0, MAX_BULLETS, _loop
  
leave s0

# ----------------------------------------

update_all:
enter
	
	jal spawn_rocks
	jal move_bullets
	jal move_rocks
	jal collide_rocks_with_bullets
	jal collide_rocks_with_player

leave

# ----------------------------------------

move_bullets:
enter
	li  t0, 0
_loop:
   	bge t0, MAX_BULLETS, _break
	#code
	mul t4, t0, 4 # t4 = index * 4
    	lw t1, bullet_y(t4)    # use t4 as the index; t1 = y coordinate
   	sub t1, t1, BULLET_VEL # subtract BULLET_VEL from its y coordinate
    	sw t1, bullet_y(t4)    # put the value back where it came from

    # now here, you have to check if t1 < 0, and if so, make bullet_active(t0) zero

    	
   	 # code   
   	 bge t1, 0, _endif # notice it's bge - the INVERSE of <
         sb zero, bullet_active(t0)
    
	_endif:

	    add t0, t0, 1
	    j _loop
    
_break:

leave

# ----------------------------------------

find_free_rock:		
enter
       li t0, 0
_loop:
        # if bullet_active[t0] == 0
        lb t1, rock_active(t0)
        bne t1, 0, _endif
        
            # return t0
            move v0, t0
            j _return
        
	_endif: 
    
    	add t0, t0, 1
    	blt t0, MAX_ROCKS, _loop

	    # here, we got out of the loop without finding a free slot,
	    # so we return -1.
	    li v0, -1

_return:
leave

# ----------------------------------------

spawn_rocks:
enter s0

	lw t0 frame_counter
	lw t1, rock_next_spawn
	
	bge t1, t0, _break
	add t0, t1, ROCK_DELAY
	
	sw t0, rock_next_spawn
		
	        jal find_free_rock
	        blt v0, zero, _break
	        

	        li t1, 1
	  	li t2, ROCK_MAX_X
	        sb t1, rock_active(v0) # bullet_active[v0] = 1
	        
	    	mul v0, v0, 4
	        sw zero, rock_y(v0) # rock_y[i] = 0
	        move s0, v0
	        li a0, ROCK_MAX_X
	        jal random
	        sw v0, rock_x(s0) # rock_x[x] = random(ROCK_MAX_X)
	    	
	    	
	    	li a0, ROCK_ANGLE_RANGE
	    	jal random
	    	add a1, v0, ROCK_MIN_ANGLE
	    	
	    	li a0, ROCK_VEL
	    	jal to_cartesian
	    	sw v0, rock_vx(s0)
	    	sw v1, rock_vy(s0)
	    	    
_break:
leave s0

# ----------------------------------------------------


draw_rocks:
enter s0 # if you want to use s0, you have to declare it on the enter and leave.

    # for s0 = 0 to MAX_BULLETS
    li s0, 0
_loop:
        # here is where you check if bullet_active(s0), and then set the pixel if so
	lb t2, rock_active(s0)
	beq t2, 0, _inactive # if t2 == 0, go to _inactive
		
		#println_str "drawing a bullet"
   		mul t0, s0, 4 # t0 = s0 * 4, have to do this because bullet_x/y are word arrays
                lw  a0, rock_x(t0)
                lw  a1, rock_y(t0)
                sra a0, a0, 8
                sra a1, a1, 8
                la a2, rock_sprite    
                jal display_blit_5x5_trans
    
	_inactive:
    
	add s0, s0, 1
	blt s0, MAX_ROCKS, _loop
  
leave s0

# ----------------------------------------------------

move_rocks:
enter s0
    
     #rock_x[i] = (rock_x[i] + rock_vx[i]) & 0x3FFF
        li t7, 0
_loop:
         
       # t0
       mul s0, t7, 4 
       lw t0, rock_x(s0)
       lw t1, rock_vx(s0)
       add t0, t0, t1
       and t0, t0, 0x3FFF
       sw t0, rock_x(s0)
       
	       lw t0, rock_y(s0) # rock_y[i]
	       lw t1, rock_vy(s0) #rock_vy[i]
	       add t0, t0, t1 # rock_y[i] + rock_vy[i]
	       sw t0, rock_y(s0)
       
       # in here is where you will check if t0 >= ROCK_MAX_Y
	       		blt t0, ROCK_MAX_Y, _endif
	       		# deactivate the rock!
	       		sb zero, rock_active(t7)
       _endif:
       
       		add t7, t7, 1
		blt t7, MAX_ROCKS, _loop
  
leave s0

# ------------------------------------

 # rock in a0, bullet in a1
collide_rocks_with_bullets:
enter s0, s1
   # li s0, 0 # s0 = rock counter
    _rock_loop:
         li s1, 0 # s1 = bullet counter 
        _bullet_loop:
            # this is inside the inner loop

	  
        move a0, s0
        move a1, s1
        jal rock_collides_with_bullet
        # the return value is in v0, and you want to check if it's 0, not equal to itself.
        # and if it is 0, you want to skip this bullet, not exit the 
        beq a0, 0, _skip

        sb zero, rock_active(a0)
        sb zero, bullet_active(a1)


        lw a0, rocks_left(a0)
        sub zero, a0, -1 # rock--
	sw a0, rocks_left(a1)

            
        add s1, s1, 1
        blt s1, MAX_BULLETS, _bullet_loop
        
   _break_bullet_loop: # you'll need to come here in one circumstance
   
        add s0, s0, 1
        blt s0, MAX_ROCKS, _rock_loop
   _skip:
leave s0, s1
# ---------------------------------

rock_collides_with_bullet:
enter
	# set v0 to 0 (false) to indicate no collision.
	li v0, 0

	# now, we check all the conditions detailed above.
	# if a condition is NOT met, branch to _return.
	#lb  t0, rock_active(a0)
	beq t0, 0, _return # inactive? return.
	lb  t0, bullet_active(a1)
	beq t0, 0, _return # inactive? return.

	li a0, ROCK_W
	li a1, ROCK_H
	sw t1, bullet_y
	sw t2, rock_x
	sw t3, bullet_x
	sw t4, rock_y
	
	bge t1, t2, _return
	add t3, t2, a0
	ble t3, t3, _return 
	bge t1, t4, _return
	add t6, t4, a1
	ble t1, t6, _return 


	# if we make it through all the conditions above, return 1 (true).
	li v0, 1
_return:
leave


# ---------------------------------
collide_rocks_with_player:
enter
       li t0, 0
_loop:
        add t0, t0, 1
    	blt t0, MAX_ROCKS, _endif

        
            # return t0
            move v0, t0
            j _return
        
	_endif: 
    
    	add t0, t0, 1
    	blt t0, MAX_ROCKS, _loop

	    # here, we got out of the loop without finding a free slot,
	    # so we return -1.
	    li v0, -1

_return:
	
leave

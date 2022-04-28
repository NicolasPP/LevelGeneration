from bisect import insort_right
import pygame
from config import FULLSCREEN, DELAY
from screen import Screen
from cell import *
from instruction import Instructions
from time_wait import regular_interval_tick_wait

"""
------------- RESTRUCTURING -------------
TODO add event parser class if game loop gets too long
TODO intructions have to be their own class
     move perform_instruction function to new class
TODO Implement a queue for the instruction
     --get rid of hardcoding instructions--
------------- ------------- -------------
------------- MENU -------------
TODO Make menu
TODO Be able show key bindings
TODO Be able to create instructions in the menu
TODO Be able to save instructions
TODO Be able to load instructions
TODO Be able to delete instructions
------------- ---- -------------
"""

show_board_info = False
done = False
screen = Screen(1600,900, FULLSCREEN)
screen.display()
instruction_manager = Instructions()

generate_cells(screen)
draw(screen.surface)


show_commands_uses = False

# UI functions 
# def perform_instructions(instruction):
#     size = len(instruction) - 1
#     index = 0
#     count = 0
#     total = instruction[index][1]
#     while True:
#         if index >= size:
#             return 
#         if regular_interval_tick_wait(DELAY):
#             count += 1
#             if count == total:
#                 index+=1
#                 total += instruction[index][1]
#             instruction[index][0](screen.surface)
#             display_current_board_information('trip', show_board_info)
#             pygame.display.update()

                    
        
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                add_walls(screen.surface)
            if event.key == pygame.K_c:
                clean_up_bigger(screen.surface)
            if event.key == pygame.K_i:
                iterate(screen.surface)
            if event.key == pygame.K_n:
                iterate_new(screen.surface)
            if event.key == pygame.K_r:
                randomise(screen.surface)
            if event.key == pygame.K_TAB:
                instruction_manager.perform(screen)
                # perform_instructions(instructions_35)
            if event.key == pygame.K_UP:
                handle_cell_size_increase(5, screen)
                generate_cells(screen)
            if event.key == pygame.K_DOWN:
                handle_cell_size_decrease(5)
                generate_cells(screen)
            if event.key == pygame.K_LEFT:
                instruction_manager.decrease_index()
                draw(screen.surface)
            if event.key == pygame.K_RIGHT:
                instruction_manager.increase_index()
                draw(screen.surface)
            if event.key == pygame.K_s:
                show_board_info = not show_board_info
                draw(screen.surface)
    display_current_board_information(Instructions.current_instruction, show_board_info)
    pygame.display.update()
    

    
from time_wait import regular_interval_tick_wait
import pygame
from config import FULLSCREEN, DELAY
from screen import Screen
from cell import *
from instruction import Instructions

"""
------------- RESTRUCTURING -------------
TODO add event parser class if game loop gets too long
TODO make checking for event.key == --- into a switch statement
------------- ------------- -------------
------------- MENU -------------
TODO Make menu
TODO Be able show key bindings
TODO Be able to create instructions in the menu
TODO Be able to save instructions
TODO Be able to delete instructions
------------- ---- -------------
"""

show_board_info = False
show_key_binds = False
done = False
perform = False
perform_index = 0
screen = Screen(1600,900, FULLSCREEN)
screen.display()
instruction_manager = Instructions()

generate_cells(screen)
draw(screen.surface)   
                    
        
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
            if event.key == pygame.K_TAB and not perform:
                perform = not perform
                perform_index = 0
                instruction_manager.handle_optional_resize(screen)
                # instruction_manager.perform(screen, show_board_info)
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
            if event.key == pygame.K_k:
                show_board_info = not show_board_info
                draw(screen.surface)
    if perform:
        if regular_interval_tick_wait(DELAY):
            perform = instruction_manager.perform(perform_index, screen)
            perform_index += 1
            
    display_current_board_information(show_board_info)
    display_current_instruction_info(instruction_manager.get_current_instruction(), screen, show_board_info)
    display_key_binds()
    pygame.display.update()
    

        
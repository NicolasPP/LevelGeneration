import pygame
from config import FULLSCREEN, DELAY
from screen import Screen
from cell import * 
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
cell_size = 20

generate_cells(screen, 20)
draw(screen.surface)


show_commands_uses = False
###### Instructions for different tilesize ###### 


# good for tile size 30 to 40
instructions_35 = [
    [randomise, 1],
    [clean_up, 1],
    [iterate, 16],
    [clean_up_bigger, 1],
    [add_walls, 1]
]
#good for large open spaces
instructions_10 = [
    [randomise, 1],
    [clean_up_huge, 1],
    [iterate, 20],
    [clean_up_bigger, 2],
    [clean_up , 7],
    [add_walls, 1]
]

# good for islands and more coast
instructions_10 = [
    [randomise, 1],
    [clean_up_bigger, 1],
    [iterate, 20],
    [clean_up_bigger, 2],
    [clean_up , 5],
    [add_walls, 1]
]

instructions_5 = [
    [randomise, 1],
    [clean_up_bigger, 1],
    [iterate, 25],
    [clean_up_huge, 1],
    [clean_up, 2],
    [add_walls, 1]
]
# FIXME this stops in the last instruction
instructions_trip = [
    [randomise, 1],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25]
]

instructions_trip = [
    [iterate_new, 100]
]

# UI functions 
def perform_instructions(instruction):
    size = len(instruction) - 1
    index = 0
    count = 0
    total = instruction[index][1]
    while index <= size:
        if regular_interval_tick_wait(DELAY):
            count += 1
            if count == total:
                index+=1
                print(index, size)
                total += instruction[index][1]
            instruction[index][0](screen.surface)
            display_current_board_information(cell_size, 'trip', show_board_info)
            pygame.display.update()
def handle_cell_size_increase(change, cell_size):
    new_size = cell_size + change
    if new_size <= screen.current_height // 10 and new_size <= screen.current_width // 10:
        return new_size
    return cell_size
def handle_cell_size_decrease(change, cell_size):
    new_size = cell_size - change
    if new_size > 0:
        return new_size   
    return cell_size                               
            
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
                perform_instructions(instructions_trip)
            if event.key == pygame.K_UP:
                cell_size = handle_cell_size_increase(5, cell_size)
                generate_cells(screen, cell_size)
                draw(screen.surface)
            if event.key == pygame.K_DOWN:
                cell_size = handle_cell_size_decrease(5, cell_size)
                generate_cells(screen, cell_size)
                draw(screen.surface)
            if event.key == pygame.K_s:
                show_board_info = not show_board_info
                draw(screen.surface)
    display_current_board_information(cell_size, 'trip', show_board_info)           
    pygame.display.update()
    

    
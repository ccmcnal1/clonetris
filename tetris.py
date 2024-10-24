# Tetris-Like Game Based on the NES Version
# Created by Connor McNally
# ESOF-2571 Project
# February 20th, 2022

import pygame
import random
from pygame.locals import *
from time import *
from os import path

############# GENERAL FUNCTIONS ###############

# Creates a new surface and sets it as the background
def initialize_surface():    
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption("Clonetris")
    surface.fill((0, 0, 0)) 
    return surface

# Runs once per Frame at 60fps
def update():
    global game_state
    
    # Splash Screen
    if game_state == 0:
        process_inputs_splash()
        draw_splash()
    
    # Main Menu
    if game_state == 1:
        process_inputs_menu()
        draw_menu()
    
    # Main Game
    if game_state == 2:
        process_inputs_game()
        modify_piece_matrix()
        auto_shift()
        draw_game()
        
        # Delay at the start of the game
        global start_delay
    
        if (start_delay <= 0):
            piece_fall()
        else:
            start_delay -= 1
    
    # Score Screen
    if game_state == 3:
        process_inputs_score()
        draw_score_screen()
    
    # Limits the game to 60fps
    clock.tick(60)

# Returns the fall speed for a given level
def get_level_speed(level):
    global fall_speeds
    
    if level >= 29:
        return level_speeds[29]
    else:
        return level_speeds[level]

# Returns the amount of start lines for a given level
def get_start_lines():
    global start_lines
    global level
     
    if level >= 29:
        return start_lines[29]
    else:
        return start_lines[level]

# Plays a specific sound
def play_sound(sound):
    global sound_dictionary
    
    if sfx_enabled:
        pygame.mixer.Sound.play(sound_dictionary[sound])

# plays specific music
def play_music(music):
    if music_enabled:
        pygame.mixer.music.stop()
        
        if music != "stop":
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            
# Creates a text object
def create_text_object(text, color):
    renderedText = font.render(str(text), True, color)
    return renderedText, renderedText.get_rect()

# Displays a text object center-aligned
def display_text_centered(text, color, pos):
    textSurface, textRect = create_text_object(text, color)
    textRect.center = pos
    windowSurface.blit(textSurface, textRect)
    
def set_font_size(size):
    global font
    font = pygame.font.Font("textures/8_bit_fortress.ttf", size)
    
def update_high_score():
    global score
    global high_score
    global is_new_high_score
    
    if score > high_score:
        high_score = score
        is_new_high_score = True
        play_sound("tetris")
        save_high_score()
        return True
    return False

# Saves the high schore to a file
def save_high_score():
    global high_score

    dir = path.dirname(__file__) # defines a file directory
    with open(path.join(dir, "saved/highscore.txt"), "w") as file: # opens file for writing
        file.write(str(high_score)) # writes the high score to the file
    
def load_high_score():
    global high_score

    dir = path.dirname(__file__) # defines a file directory
    try: # opens a file for reading
        with open(path.join(dir, "saved/highscore.txt"), "r") as file:
            high_score = int(file.read()) # fetches the high score from the file
    except:
        high_score = 0 # occurs if the file doesn't exist or is corrupted

########## SPLASH SCREEN FUNCTIONS #############

def draw_splash():
    # Background
    windowSurface.fill((0, 0, 0))
    windowSurface.blit(splash_background, (0, 0))
    
    # Updates the display
    pygame.display.update()

def process_inputs_splash():
    global game_state
    
    # Checks for all specific events
    for event in pygame.event.get():
        
        # Quits if this event happens
        if event.type == QUIT:
            running = False
            
        ### INPUTS FOR KEYBOARD ###
        if event.type == pygame.KEYDOWN:
            game_state = 1
            play_sound("level_up")
        
        ### INPUTS FOR CONTROLLER ###
        if event.type == pygame.JOYBUTTONDOWN:
            game_state = 1
            play_sound("level_up")

############ MAIN MENU FUNCTIONS ###############

# Draws the textures of the main menu
def draw_menu():
    global high_school
    global added_levels
    global music_enabled
    global sfx_enabled
    
    # Background
    windowSurface.fill((0, 0, 0))
    windowSurface.blit(menu_background, (0, 0))

    # Level adder
    if added_levels == 0:
        windowSurface.blit(ui_plus_zero, (780, 124))
    elif added_levels == 10:
        windowSurface.blit(ui_plus_ten, (780, 124))
    else:
        windowSurface.blit(ui_plus_twenty, (780, 124))
        
    # Music/SFX X icons
    if not sfx_enabled:
        windowSurface.blit(ui_x, (780, 252))
    if not music_enabled:
        windowSurface.blit(ui_x, (908, 252))

    # UI Selector
    draw_menu_selection()
    
    # High score
    set_font_size(64)
    display_text_centered(high_score, (255, 255, 255), (576, 600))
    
    # Updates the display
    pygame.display.update()

# Processes inputs for the main menu
def process_inputs_menu():
    global isPushingUp
    global isPushingDown
    global isPushingLeft
    global isPushingRight
    
    # Checks for all specific events
    for event in pygame.event.get():
        
        # Quits if this event happens
        if event.type == QUIT:
            running = False
            
        ### INPUTS FOR KEYBOARD ###
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                navigate_menu(0, 1) # move up
            if event.key == pygame.K_DOWN:
                navigate_menu(0, -1) # move down
            if event.key == pygame.K_LEFT:
                navigate_menu(-1, 0) # move left
            if event.key == pygame.K_RIGHT:
                navigate_menu(1, 0) # move right
            if event.key == pygame.K_RETURN:
                select_ui() # select ui element
        
        ### INPUTS FOR CONTROLLER ###
        if event.type == pygame.JOYHATMOTION:
            # D-Pad Used for Navigation
            if event.value[1] == 1 and isPushingUp == False:
                isPushingUp = True
                navigate_menu(0, 1) # move up
            if event.value[1] == -1 and isPushingDown == False:
                isPushingDown = True
                navigate_menu(0, -1) # move down
            if event.value[0] == 1 and isPushingRight == False:
                isPushingRight = True
                navigate_menu(1, 0) # move left
            if event.value[0] == -1 and isPushingLeft == False:
                isPushingLeft = True
                navigate_menu(-1, 0) # move right
                
            # resets input variables if the joyhat is in the neutral position
            # for the respective axis
            if event.value[1] == 0:
                isPushingUp = False
                isPushingDown = False
            if event.value[0] == 0:
                isPushingLeft = False
                isPushingRight = False
        
        # A button to select UI
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                select_ui()

# Determines menu position
# h - horizontal, v - vertical
def navigate_menu(h, v):
    global menu_position
    
    # Left and Right Movement
    if (v == 0):
        # Stops from moving too far left or right
        if menu_position == 0 and h == -1:
            menu_position = 0
        elif menu_position == 12 and h == 1:
            menu_position = 12
        # Moves based on h value
        else:
            menu_position += h
            play_sound("ui_move")
    
    # Up and Down Movement
    if (h == 0):
        # Bottom to Top Case
        if menu_position > 5 and v == 1:
            if menu_position > 10:
                menu_position = 5
                play_sound("ui_move")
            else:
                menu_position -= 6
                play_sound("ui_move")
        # Top to Bottom Case
        if menu_position <= 5 and v == -1:
            menu_position += 6
            play_sound("ui_move")

# Draws the green rectangle over the selected menu position
def draw_menu_selection():
    global menu_position
    global ui_select
    global ui_select_big
    
    if menu_position >= 0 and menu_position <= 4:
        windowSurface.blit(ui_select, (128*menu_position + 140, 124))
    elif menu_position == 5:
        windowSurface.blit(ui_select_big, (780, 124))
    else:
        windowSurface.blit(ui_select, (128*(menu_position - 6) + 140, 252))

# Does specified action upon selection of certain ui elements
def select_ui():
    global menu_position
    global added_levels
    global sfx_enabled
    global music_enabled
    
    # Start game (levels 0-4 + added levels)
    if menu_position >= 0 and menu_position <= 4:
        start_game(menu_position + added_levels)
        play_sound("level_up")
    # Add levels
    elif menu_position == 5:
        add_levels()
        play_sound("piece_rotate")
    # Toggle Sound Effects
    elif menu_position == 11:
        sfx_enabled = not sfx_enabled
        play_sound("piece_rotate")
    # Toggle Music
    elif menu_position == 12:
        music_enabled = not music_enabled
        play_sound("piece_rotate")
    # Start game (levels 5-9 + added levels)
    else:
        start_game(menu_position - 1 + added_levels)
        play_sound("level_up")

# Toggles through different amounts of added levels
def add_levels():
    global added_levels
    
    if added_levels == 20:
        added_levels = 0
    else:
        added_levels += 10

# Resets all game variables to defaults and starts game
def start_game(start_level):
    global game_state
    global level
    global lines_to_next_level
    
    reset_all_game_variables()
    
    # sets starting level and lines
    level = start_level
    lines_to_next_level = get_start_lines()
    
    # starts the game scene
    game_state = 2
    play_music("audio/music.wav")

# Resets all game variables to their defaults
def reset_all_game_variables():
    global level
    global score
    global lines
    global lines_to_next_level
    global current_rotation
    global current_piece
    global next_piece
    global das
    global fall_timer
    global center
    global start_delay
    global is_new_high_score
    global isPushingUp
    global isPushingDown
    global isPushingLeft
    global isPushingRight
    
    # Default values
    level = 0
    score = 0
    lines = 0
    lines_to_next_level = 0
    current_rotation = 3
    current_piece = get_next_piece()
    next_piece = get_next_piece()
    clear_block_matrix()
    clear_piece_matrix()
    das = 0
    fall_timer = 0
    center = [5, 0]
    start_delay = 90
    is_new_high_score = False
    isPushingUp = False
    isPushingDown = False
    isPushingLeft = False
    isPushingRight = False

############ MAIN GAME FUNCTIONS ###############

# Responsible for drawing the graphics of the game screen
def draw_game():    
    global score
    global lines
    global level
    
    # Background
    windowSurface.fill((0, 0, 0))
    windowSurface.blit(game_background, (0, 0))
    
    # Draws Score, Lines, and Level Text to the Screen
    set_font_size(32)
    display_text_centered(score, (255, 255, 255), (228, 180))
    display_text_centered(lines, (255, 255, 255), (228, 436))
    display_text_centered(level, (255, 255, 255), (932, 436))
    
    # Grid and next piece
    drawGrid()
    display_next_piece()
    
    # Updates the display
    pygame.display.update()

# Processes inputs for the game
def process_inputs_game():
    global fall_timer
    global isPushingDown
    global isPushingRight
    global isPushingLeft
    global start_delay
    global center
    global das
    global level
    
    # Checks for all specific events
    for event in pygame.event.get():
        
        # Quits if this event happens
        if event.type == QUIT:
            running = False
        
        ### INPUTS FOR KEYBOARD ###
        if event.type == pygame.KEYDOWN:        
            # Right movement
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                isPushingRight = True
                isPushingLeft = False
                
                # to stop the piece from moving right and down at the same time
                isPushingDown = False
                
                # This check is here to simulate the ability
                # for a direction key to not reset das
                # during a line-clear or entry delay
                if center[1] != 0 or fall_timer != get_level_speed(level):
                    das = -10
                    move_right()
            # Left movement
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                isPushingLeft = True
                isPushingRight = False
                
                # to stop the piece from moving left and down at the same time
                isPushingDown = False
                
                if center[1] != 0 or fall_timer != get_level_speed(level):
                    das = -10
                    move_left()
                
            isPushingDown = False
            # Down    This is here to prevent the piece from moving down and to the side at the same time since this behaviour is impossible in the original game
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not (isPushingLeft or isPushingRight): # <<<V
                isPushingDown = True
                if level < 29:
                    fall_timer = 2
                start_delay = 0 # skips start delay if down pressed
            
            # Up (used as a rotation key)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                rotate_right()
            
            # Rotation
            if event.key == pygame.K_x or event.key == pygame.K_SLASH:
                rotate_right()
            if event.key == pygame.K_z or event.key == pygame.K_PERIOD:
                rotate_left()
        
        # Resets fall speed to default
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and isPushingDown == True:
                isPushingDown = False
                fall_timer = get_level_speed(level)
                
            # Resets left and right movement when released
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                isPushingRight = False
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                isPushingLeft = False
                
        ### INPUTS FOR CONTROLLER ###
        if event.type == pygame.JOYHATMOTION:
            # Right movement
            if event.value[0] == 1 and isPushingRight == False:
                isPushingRight = True
                
                # to stop the piece from moving right and down at the same time
                isPushingDown = False
  
                if center[1] != 0 or fall_timer != get_level_speed(level):
                    das = -10
                    move_right()
            # Left movement
            if event.value[0] == -1 and isPushingLeft == False:
                isPushingLeft = True
                
                # to stop the piece from moving left and down at the same time
                isPushingDown = False
                
                if center[1] != 0 or fall_timer != get_level_speed(level):
                    das = -10
                    move_left()
            
            # Down movement  Prevents diagonal inputs from doing two actions at once V
            if event.value[1] == -1 and event.value[0] == 0 and isPushingDown == False:
                isPushingDown = True
                if level < 29:
                    fall_timer = 2
                start_delay = 0
            if event.value[1] == 0 and isPushingDown == True:
                isPushingDown = False
                fall_timer = get_level_speed(level)
                
            # reset left and right movement if the joyhat is in the
            # neutral position
            if event.value[0] == 0:
                isPushingLeft = False
                isPushingRight = False
          
        # Rotation
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1: # B button
                rotate_right()
            if event.button == 0: # A button
                rotate_left()

# Draws the block matrix contents on screen
def drawGrid():
    global block_matrix
    global piece_matrix
    
    # Loops through each block in both the block and piece matrices and draws the specified
    # block at each location
    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[x])):
            if block_matrix[x][y] != 0:
                windowSurface.blit(blocks[block_matrix[x][y] - 1], (416 + (32 * x), 112 + (32 * y)))
            if piece_matrix[x][y] != 0:
                windowSurface.blit(blocks[piece_matrix[x][y] - 1], (416 + (32 * x), 112 + (32 * y)))

# Deals with positioning the piece in the piece matrix
def modify_piece_matrix():
    global tetrominoes
    global piece_matrix
    global current_piece
    global center
    global current_rotation
    
    # Modifies the values of the piece matrix to add the piece into it around the center point
    for i in range(6):
        for j in range(6):
            if (center[0] + i - 3) >= 0 and (center[1] + j - 3) >= 0 and (center[0] + i - 3) < 10 and (center[1] + j - 3) < 20:
                piece_matrix[center[0] + i - 3][center[1] + j - 3] = tetrominoes[current_piece][current_rotation][i][j]
    
# Determines if the current piece's position is within the allowable playspace
def check_valid_position():
    global center
    global tetrominoes
    global block_matrix
    global current_piece
    global current_rotation
    
    for i in range(6):
        for j in range(6):
            if tetrominoes[current_piece][current_rotation][i][j] != 0:
                # Checks if any part of the piece is outside the grid (except for the top which is intended
                # to allow for play at the top of the screen)
                if (center[0] + i - 3) < 0 or (center[0] + i - 3) >= 10 or (center[1] + j - 3) >= 20:
                    return False
                # Checks if any part of the piece is colliding with the block grid
                if not (center[1] + j - 3) < 0:
                    if block_matrix[center[0] + i - 3][center[1] + j - 3] != 0:
                        return False
    return True

# Controls how fast a piece falls depending on the level and if
# the down key is pressed
def piece_fall():
    global fall_timer
    global isPushingDown
    global push_down_pts
    global level_speeds
    global level
      
    if fall_timer > 1:
        fall_timer -= 1
    else:
        if isPushingDown:
            if get_level_speed(level) != 1:
                fall_timer = 2
            push_down_pts += 1
            push_down_pts = push_down_pts % 16 # to emulate a bug in the original game
        else:
            fall_timer = get_level_speed(level)
            push_down_pts = 0
            
        drop_piece()

# Drops the piece by 1 unit
def drop_piece():
    global center
    global isPushingDown

    center[1] += 1
    
    # If it collides with other blocks or the bottom,
    # Lock the piece to the grid
    if not check_valid_position():
        center[1] -= 1
        isPushingDown = False
        lock_piece()

# Auto-shifts the piece left or right if a direction
# key is held for long enough (long delay at first,
# short delay afterward
def auto_shift():
    global das
    global isPushingLeft
    global isPushingRight
    
    if isPushingLeft:
        das += 1
        if das >= 6:
            das = 0
            move_left()
    if isPushingRight:
        das += 1
        if das >= 6:
            das = 0
            move_right()

# Moves piece left
def move_left():
    global das
    
    center[0] -= 1
    if not check_valid_position():
        center[0] += 1
        das = 6 # allows for piece tucking and "wall charges"
    else:
        play_sound("piece_move")

# Moves piece right
def move_right():
    global das
    
    center[0] += 1
    if not check_valid_position():
        center[0] -= 1
        das = 6 # allows for piece tucking and "wall charges"
    else:
        play_sound("piece_move")

# Rotates current piece left
def rotate_left():
    global current_rotation
    
    if (current_rotation < 3):
        current_rotation += 1
        if not check_valid_position():
            current_rotation -= 1
        else:
            play_sound("piece_rotate")
    else:
        current_rotation = 0
        if not check_valid_position():
            current_rotation = 3
        else:
            play_sound("piece_rotate") 
     
# Rotates current piece right
def rotate_right():
    global current_rotation
    
    if (current_rotation > 0):
        current_rotation -= 1
        if not check_valid_position():
            current_rotation += 1
        else:
            play_sound("piece_rotate")
    else:
        current_rotation = 3
        if not check_valid_position():
            current_rotation = 0
        else:
            play_sound("piece_rotate")

# Returns a random number corrosponding to a specific piece
def get_next_piece():
    return random.randint(0, 6)

# Displays the next piece in the next box
def display_next_piece():
    global next_piece
        
    for x in range(6):
        for y in range(6):
            if (tetrominoes[next_piece][3][x][y]) != 0:
                windowSurface.blit(blocks[tetrominoes[next_piece][3][x][y] - 1], (816 + (32 * x), 80 + (32 * y)))

# Locks the piece to the grid
def lock_piece():
    global block_matrix
    global piece_matrix
    global next_piece
    global current_piece
    global current_rotation
    global center
    
    # Transfers the squares from the piece matrix
    # To the block matrix
    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[x])):
            if piece_matrix[x][y] != 0:
                block_matrix[x][y] = piece_matrix[x][y]
    start_next_piece()

# Prepares the next piece
def start_next_piece():
    global current_piece
    global next_piece
    global current_rotation
    global center
    
    clear_piece_matrix()
       
    if not clear_lines():
        draw_game()
        pygame.time.delay(217) # 13 frames equivalent delay
        play_sound("piece_lock")
    
    current_piece = next_piece
    next_piece = get_next_piece()
    center = [5, 0]
    current_rotation = 3
    calculate_pushdown_points()
    control_music()
    modify_piece_matrix()
    draw_game()
    
    # Checks for game over condition (if the block collides with
    # any block at the top of the board)
    if not check_valid_position():
        game_end()

# Determines when to play the fast music versus the normal music
def control_music():
    global block_matrix
    global is_fast_music
    
    has_changed_value = False
    
    # Checks if any of the middle squares in the top 6 rows are filled
    if is_fast_music == False:
        for x in range(6):
            for y in range(6):
                if block_matrix[x+2][y] != 0:
                    is_fast_music = True
                    has_changed_value = True
                    break
    else:
        is_fast_music = False
        has_changed_value = True
        for x in range(6):
            for y in range(6):
                if block_matrix[x+2][y] != 0:
                    is_fast_music = True
                    has_changed_value = False
    
    if (has_changed_value):
        if is_fast_music:
            play_music("audio/music_fast.wav")
        else:
            play_music("audio/music.wav")
    
# Sets all values in the piece matrix to 0
def clear_piece_matrix():
    global piece_matrix
    
    for x in range(len(piece_matrix)):
        for y in range(len(piece_matrix[x])):
            piece_matrix[x][y] = 0

# Sets all values in the block matrix to 0
def clear_block_matrix():
    global block_matrix
    
    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[x])):
            block_matrix[x][y] = 0

# Clears any horizontal lines that are filled up and moves
# any remaining lines down the grid
def clear_lines():
    global block_matrix
    global lines
    
    # Matrix that contains a list of rows (compared to a list of columns)
    converted_matrix = [[0 for i in range(10)] for j in range(20)]
    
    # Will contain the specific lines that need to be cleared
    lines_to_clear = []
    
    # Converts the [columns][rows] block matrix to the
    # [rows][columns] converted matrix (to make the line
    # clearing algorithm easier
    for x in range(len(block_matrix)):
        for y in range(len(block_matrix[x])):
            converted_matrix[y][x] = block_matrix[x][y]
    
    # Checks all rows to see if any of them are filled and places
    # the indices of the filled rows in the lines_to_clear list
    for i in range(len(converted_matrix)):
        if 0 not in converted_matrix[i]:
            lines_to_clear.append(i)  
    
    # Plays line clear sound
    if len(lines_to_clear) == 4:
        play_sound("tetris")
    elif len(lines_to_clear) > 0:
        play_sound("line_clear")
         
    # Plays a line clear animation
    if (len(lines_to_clear) > 0):
        line_clear_animation(lines_to_clear)
    
    # Moves all remaining rows above each cleared line down to fill
    # the gap using a top-down approach (note that lower numbers
    # Represent higher blocks in the grid)
    for i in lines_to_clear:
        for j in range(i, 0, -1):        
            converted_matrix[j] = converted_matrix[j-1]
                
    # Clears top rows if there were any pieces in the top row
    for i in range(len(lines_to_clear)):
        converted_matrix[i] = [0 for x in range(10)]
    
    # Converts the converted matrix back to the regular
    # block matrix format
    for x in range(len(converted_matrix)):
        for y in range(len(converted_matrix[x])):
            block_matrix[y][x] = converted_matrix[x][y]
    
    # Updates lines, level, and score accordingly
    lines += len(lines_to_clear)
    calculate_level(len(lines_to_clear))
    calculate_line_score(len(lines_to_clear))
    
    return len(lines_to_clear) > 0

# Line-clear animation
def line_clear_animation(lines_to_clear):
    global block_matrix
    
    pygame.time.delay(167) # 10 frames equivalent
    
    for i in lines_to_clear:
        block_matrix[4][i] = 0
        block_matrix[5][i] = 0
      
    draw_game()
    pygame.time.delay(67) # 4 frames equivalent
        
    for i in lines_to_clear:
        block_matrix[3][i] = 0
        block_matrix[6][i] = 0
       
    draw_game()
    pygame.time.delay(67) # 4 frames equivalent
        
    for i in lines_to_clear:
        block_matrix[2][i] = 0
        block_matrix[7][i] = 0
    
    draw_game()
    pygame.time.delay(67) # 4 frames equivalent
        
    for i in lines_to_clear:
        block_matrix[1][i] = 0
        block_matrix[8][i] = 0
    
    draw_game()
    pygame.time.delay(67) # 4 frames equivalent
        
    for i in lines_to_clear:
        block_matrix[0][i] = 0
        block_matrix[9][i] = 0
        
    draw_game()
    pygame.time.delay(100) # 6 frames equivalent
    

# Adds push-down points to the current score
def calculate_pushdown_points():
    global score
    global push_down_pts
    
    score += push_down_pts
    push_down_pts = 0

# Adds line-clear points to score (higher levels
# and high-line clear counts add more to the score
def calculate_line_score(lines_cleared):
    global score
    global level
    
    if lines_cleared == 1:
        score += 40 * (level + 1)
    if lines_cleared == 2:
        score += 120 * (level + 1)
    if lines_cleared == 3:
        score += 300 * (level + 1)
    if lines_cleared == 4:
        score += 1200 * (level + 1)

# Updates the level based on the number of lines
# cleared
def calculate_level(lines_cleared):
    global level
    global level_speeds
    global lines_to_next_level
    
    lines_to_next_level -= lines_cleared
    
    if lines_to_next_level <= 0:
        level += 1
        lines_to_next_level += 10
        
        # Audio
        if get_level_speed(level-1) != get_level_speed(level):
            play_sound("speed_up")
        else:
            play_sound("level_up")
        
# Returns to the menu when the player reaches the top of the screen
def game_end():
    play_music("stop")
    play_sound("game_over")
    
    # Waits 5 seconds until it gets to the menu
    pygame.time.delay(5000)
    setup_score_screen()

############# SCORE SCREEN FUNCTIONS ##############
    
def setup_score_screen():
    global game_state
    
    game_state = 3
    play_music("audio/music_end.wav")
    
    clear_block_matrix()
    clear_piece_matrix()
    
    update_high_score()
    
def draw_score_screen():
    global is_new_high_score
    
    # Background
    windowSurface.fill((0, 0, 0))
    windowSurface.blit(score_background, (0, 0))
    
    # Draws Score and Level Text to the Screen
    set_font_size(64)
    display_text_centered(score, (255, 255, 255), (312, 340))
    display_text_centered(level, (255, 255, 255), (840, 340))
    
    # High score text
    if (is_new_high_score):
        display_text_centered("NEW HIGH SCORE!", (255, 255, 255), (576, 560))
    
    # Updates the display
    pygame.display.update()
    

def process_inputs_score():
    global game_state
    
     # Checks for all specific events
    for event in pygame.event.get():
        
        # Quits if this event happens
        if event.type == QUIT:
            running = False
            
        ### INPUTS FOR KEYBOARD ###
        if event.type == pygame.KEYDOWN:
            game_state = 1 # return to the menu
            play_music("stop")
            play_sound("level_up")
        
        ### INPUTS FOR CONTROLLER ###
        if event.type == pygame.JOYBUTTONDOWN:
            game_state = 1 # return to the menu
            play_music("stop")
            play_sound("level_up")

################# INIT PYGAME #####################

# Starts Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

# Initializes all Joysticks
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

# Window resolution
WINDOWWIDTH = 1152
WINDOWHEIGHT = 864

# Initializes a surface and the pygame clock
windowSurface = initialize_surface()
clock = pygame.time.Clock()

################## TEXTURES #######################

# Menu Screen
menu_background = pygame.image.load("textures/menu_screen.png")
menu_background = pygame.transform.scale(menu_background, (WINDOWWIDTH, WINDOWHEIGHT))

score_background = pygame.image.load("textures/score_screen.png")
score_background = pygame.transform.scale(score_background, (WINDOWWIDTH, WINDOWHEIGHT))

splash_background = pygame.image.load("textures/splash_screen.png")
splash_background = pygame.transform.scale(splash_background, (WINDOWWIDTH, WINDOWHEIGHT))

# Menu UI Elements
ui_select = pygame.image.load("textures/ui_selection.png")
ui_select = pygame.transform.scale(ui_select, (104, 104)) # 4x upscale from original image

ui_select_big = pygame.image.load("textures/ui_selection_big.png")
ui_select_big = pygame.transform.scale(ui_select_big, (232, 104))

ui_x = pygame.image.load("textures/ui_x.png")
ui_x = pygame.transform.scale(ui_x, (104, 104))

ui_plus_zero = pygame.image.load("textures/ui_plus_zero.png")
ui_plus_zero = pygame.transform.scale(ui_plus_zero, (232, 104))

ui_plus_ten = pygame.image.load("textures/ui_plus_ten.png")
ui_plus_ten = pygame.transform.scale(ui_plus_ten, (232, 104))

ui_plus_twenty = pygame.image.load("textures/ui_plus_twenty.png")
ui_plus_twenty = pygame.transform.scale(ui_plus_twenty, (232, 104))

# Background screen
game_background = pygame.image.load("textures/game_screen.png")
game_background = pygame.transform.scale(game_background, (WINDOWWIDTH, WINDOWHEIGHT))

# Piece blocks
i_block = pygame.image.load("textures/I_block.png")
i_block = pygame.transform.scale(i_block, (32, 32))
j_block = pygame.image.load("textures/J_block.png")
j_block = pygame.transform.scale(j_block, (32, 32))
l_block = pygame.image.load("textures/L_block.png")
l_block = pygame.transform.scale(l_block, (32, 32))
o_block = pygame.image.load("textures/O_block.png")
o_block = pygame.transform.scale(o_block, (32, 32))
s_block = pygame.image.load("textures/S_block.png")
s_block = pygame.transform.scale(s_block, (32, 32))
t_block = pygame.image.load("textures/T_block.png")
t_block = pygame.transform.scale(t_block, (32, 32))
z_block = pygame.image.load("textures/Z_block.png")
z_block = pygame.transform.scale(z_block, (32, 32))

# Piece array
blocks = [i_block, j_block, l_block, o_block, s_block, t_block, z_block]

# Text
font = pygame.font.Font("textures/8_bit_fortress.ttf", 32)

################## AUDIO/MUSIC ####################

piece_move = pygame.mixer.Sound("audio/piece_move.wav")
piece_rotate = pygame.mixer.Sound("audio/piece_rotate.wav")
piece_lock = pygame.mixer.Sound("audio/piece_lock.wav")
game_over = pygame.mixer.Sound("audio/game_over.wav")
line_clear = pygame.mixer.Sound("audio/line_clear.wav")
tetris = pygame.mixer.Sound("audio/tetris.wav")
level_up = pygame.mixer.Sound("audio/level_up.wav")
speed_up = pygame.mixer.Sound("audio/speed_up.wav")
ui_move = pygame.mixer.Sound("audio/ui_move.wav")

# Sound Dictionary
sound_dictionary = {
    "piece_move" : piece_move,
    "piece_rotate" : piece_rotate,
    "piece_lock" : piece_lock,
    "game_over" : game_over,
    "line_clear" : line_clear,
    "tetris" : tetris,
    "level_up" : level_up,
    "speed_up" : speed_up,
    "ui_move" : ui_move
}
   
################ GENERAL VARIABLES ################

# Game runs as long as this is true
running = True

# Is a new high score
is_new_high_score = False

# Game State (0 = splash, 1 = menu, 2 = game, 3 = score)
game_state = 0

# Menu Position
menu_position = 0

# Music is fast or not
is_fast_music = False

# Audio settings
music_enabled = True
sfx_enabled = True

################# INPUT VARIABLES #################

isPushingUp = False
isPushingDown = False
isPushingLeft = False
isPushingRight = False

################## GAME VARIABLES #################

# Look-up table for level fall speeds (0-29)
level_speeds = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3,
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]

# Start lines until next level for each starting level (0-29)
start_lines = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 100, 100, 100, 100,
               100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 200, 200,
               200, 200]

# Lines to next level
lines_to_next_level = 0

# Delayed Auto-Shift for left/right movement
das = 0

# Start delay (in frames)
start_delay = 90

# Block center (default value)
center = [5, 0]

# Current piece
current_piece = 0

# Next piece
next_piece = 0

# Current rotation
current_rotation = 3

# Score counter
score = 0
high_score = 0
load_high_score()

# Lines counter
lines = 0

# Level counter
level = 0

# Push-down points
push_down_pts = 0

# Added levels
added_levels = 0

# Lines to next level
lines_to_next_level = 0

# Fall timer
fall_timer = 0

# 10x20 block matrix (stores locked pieces)
block_matrix = [[0 for x in range(20)] for y in range(10)]

# 10x20 piece matrix (stores moving pieces)
piece_matrix = [[0 for x in range(20)] for y in range(10)]

################# TETROMINOES #################

# I Piece
i_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,0 ,0, 0],
                [0, 1 ,1 ,1 ,1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0 ,0 ,1 ,0, 0],
                [0, 0 ,0 ,1 ,0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,0 ,0, 0],
                [0, 1 ,1 ,1 ,1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0 ,0 ,1 ,0, 0],
                [0, 0 ,0 ,1 ,0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0]]]

# J Piece
j_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0],
                [0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 0, 0],
                [0, 0, 0, 2, 0, 0],
                [0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0],
                [0, 0, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0],
                [0, 0, 0, 2, 0, 0],
                [0, 0, 0, 2, 2, 0],
                [0, 0, 0, 0, 0, 0]]]

# L Piece
l_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,0 ,0, 0],
                [0, 0 ,3 ,3 ,3, 0],
                [0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,3 ,0, 0],
                [0, 0 ,0 ,3 ,0, 0],
                [0, 0, 3, 3, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,3 ,0 ,0, 0],
                [0, 0 ,3 ,3 ,3, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,3 ,3, 0],
                [0, 0 ,0 ,3 ,0, 0],
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0]]]

# O Piece
o_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0 ,4 ,4, 0],
                [0, 0, 0 ,4 ,4, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0 ,0 ,4 ,4, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]]

# S Piece
s_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0 ,0 ,0, 0],
                [0, 0, 0 ,5 ,5, 0],
                [0, 0, 5, 5, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,5 ,0, 0],
                [0, 0 ,0 ,5 ,5, 0],
                [0, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,0 ,0, 0],
                [0, 0 ,0 ,5 ,5, 0],
                [0, 0, 5, 5, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,5 ,0, 0],
                [0, 0 ,0 ,5 ,5, 0],
                [0, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0]]]

# T Piece
t_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0 ,0 ,0, 0],
                [0, 0, 6 ,6 ,6, 0],
                [0, 0, 0, 6, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,6 ,0, 0],
                [0, 0 ,6 ,6 ,0, 0],
                [0, 0, 0, 6, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,6 ,0, 0],
                [0, 0 ,6 ,6 ,6, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0 ,0 ,6 ,0, 0],
                [0, 0 ,0 ,6 ,6, 0],
                [0, 0, 0, 6, 0, 0],
                [0, 0, 0, 0, 0, 0]]]

# Z Piece
z_tetromino = [[[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0 ,0, 0],
                [0, 0, 7, 7 ,0, 0],
                [0, 0, 0, 7, 7, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0 ,0, 7, 0],
                [0, 0, 0 ,7, 7, 0],
                [0, 0, 0, 7, 0, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 7, 7, 0, 0],
                [0, 0, 0, 7, 7, 0],
                [0, 0, 0, 0, 0, 0]],
               [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 7, 0],
                [0, 0, 0, 7, 7, 0],
                [0, 0, 0, 7, 0, 0],
                [0, 0, 0, 0, 0, 0]]]

# Tetromino List (stored as a 6x6x4x7 matrix (6x6 blocks, 4 rotations, 7 pieces)
tetrominoes = [i_tetromino, j_tetromino, l_tetromino, o_tetromino, s_tetromino, t_tetromino, z_tetromino]

################## MAIN GAME LOOP #################

# Runs the game
while running:
    update()

# Quits pygame once done
pygame.quit()
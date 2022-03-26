import pygame
import sys
import easygui
import random
import os
import json
from button import Button
from mastermind import MastermindGame

pygame.init()  # Initialize pygame to work with it

WIDTH, HEIGHT = 720, 800  # Width and height of display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create screen
pygame.display.set_caption("Mastermind")  # Set screen title

FONT = pygame.font.SysFont('Comic Sans MS', 22)

''' Load background imgs '''
bg1 = pygame.image.load(os.path.join("Assets", "bg1.jpg"))
bg2 = pygame.image.load(os.path.join("Assets", "bg2.jpg"))
bgs = [bg1, bg2]
bg = random.choice(bgs)  # Choose random background on start

''' Load img's color knobs '''
red = pygame.image.load(os.path.join("Assets", "red.png"))
yellow = pygame.image.load(os.path.join("Assets", "yellow.png"))
green = pygame.image.load(os.path.join("Assets", "green.png"))
blue = pygame.image.load(os.path.join("Assets", "blue.png"))
black = pygame.image.load(os.path.join("Assets", "black.png"))
white = pygame.image.load(os.path.join("Assets", "white.png"))
purple = pygame.image.load(os.path.join("Assets", "purple.png"))
blank = pygame.image.load(os.path.join("Assets", "blank.png"))
''' Load img's for scores '''
blank_score = pygame.image.load(os.path.join("Assets", "blank_score.png"))
black_score = pygame.image.load(os.path.join("Assets", "black_score.png"))
white_score = pygame.image.load(os.path.join("Assets", "white_score.png"))
cursor = pygame.image.load(os.path.join("Assets", "target.png"))

''' Load img's for buttons '''
blue_button_img = pygame.image.load(
    os.path.join("Assets", "blue_bt_inactive.png"))
blue_button_img = pygame.transform.scale(blue_button_img, (150, 70))
blue_button_active_img = pygame.image.load(
    os.path.join("Assets", "blue_bt_active.png"))
blue_button_active_img = pygame.transform.scale(
    blue_button_active_img, (150, 70))

yellow_button_img = pygame.image.load(
    os.path.join("Assets", "yellow_bt_inactive.png"))
yellow_button_img = pygame.transform.scale(yellow_button_img, (150, 70))
yellow_button_active_img = pygame.image.load(
    os.path.join("Assets", "yellow_bt_active.png"))
yellow_button_active_img = pygame.transform.scale(
    yellow_button_active_img, (150, 70))

exit_button_img = pygame.image.load(
    os.path.join("Assets", "exit_bt_inactive.png"))
exit_button_img = pygame.transform.scale(exit_button_img, (116, 76))
exit_button_active_img = pygame.image.load(
    os.path.join("Assets", "exit_bt_active.png"))
exit_button_active_img = pygame.transform.scale(
    exit_button_active_img, (116, 76))

# Load board img
board = pygame.image.load(os.path.join("Assets", "board.png"))

# Declare global variables
SELECTED_ROW = 0  # Currently selected row
SELECTED_COLUMN = 0  # Currently selected column

# Store player answers and scores respectively
PLAYER_GRID = [["blank"] * 4 for rows in range(8)]
SCORE_GRID = [["blank"] * 4 for rows in range(8)]

# Store player colors and possible scores respectively
PLAYER_COLORS = {"red": red, "yellow": yellow, "green": green, "blue": blue,
                 "black": black, "white": white, "purple": purple, "blank": blank}
SCORE_COLORS = {"black": black_score,
                "white": white_score, "blank": blank_score}

# Create game instance!
GAME = MastermindGame(list(PLAYER_COLORS.keys()))

SET_CODE = False  # True if creating own code


def draw_board():
    screen.blit(board, (0, 0))


def exit_game():
    ''' Exit game outside while loop '''
    pygame.quit()
    sys.exit()


def check_answer():
    ''' Get score and store to display later on '''
    global SELECTED_ROW, update_screen, GAME, SET_CODE
    if (SET_CODE == True):
        code = PLAYER_GRID[SELECTED_ROW]
        restart_game()
        GAME.set_code(code)
        SET_CODE = False
        update_screen = True
        return
    score = GAME.check_answer(PLAYER_GRID[SELECTED_ROW], GAME.get_code())
    if (score.count("black") == 4):  # WIN!!!
        easygui.msgbox("Congrats! You won!!!")
        exit_game()
    if SELECTED_ROW == 7:   # LOSE :(
        correct_code = " ".join(GAME.get_code())
        easygui.msgbox("You Lost! Correct code is: " + str(correct_code))
        exit_game()
    index = 0
    for result in score:
        SCORE_GRID[SELECTED_ROW][index] = result
        index += 1

    SELECTED_ROW += 1
    update_screen = True


def set_code():
    ''' Clear grid to allow player to set custom code '''
    global SET_CODE
    restart_game()
    SET_CODE = True


def ai_turn():
    ''' Smart AI answer '''
    global update_screen, PLAYER_GRID
    colors = random.sample(GAME.possibilities, 1)[0]
    PLAYER_GRID[SELECTED_ROW] = colors
    update_screen = True


def random_turn():
    ''' Dumb AI answer '''
    global update_screen, PLAYER_GRID
    for column in range(4):
        color = random.sample(list(PLAYER_COLORS.keys()), 1)
        PLAYER_GRID[SELECTED_ROW][column] = color[0]
    update_screen = True


def save_game():
    ''' Save game session to data.json file '''
    dictionary = {
        "selected_column": SELECTED_COLUMN,
        "selected_row": SELECTED_ROW,
        "code": GAME.get_code(),
        "player_grid": PLAYER_GRID,
        "score_grid": SCORE_GRID,
        "possibilities": GAME.possibilities
    }
    data = json.dumps(dictionary, indent=4)
    with open("data.json", "w") as file:
        file.write(data)


def load_game():
    ''' Loads game session from data.json and assign data to global variables '''
    global SELECTED_ROW, SELECTED_COLUMN, PLAYER_GRID, SCORE_GRID, update_screen
    with open("data.json", "r") as file:
        data = json.load(file)
        index = 0
        # Clear current AI information about game session
        GAME.clear_history()
        GAME.set_code(data['code'])
        GAME.possibilities = data['possibilities']
        for row in data['player_grid']:
            PLAYER_GRID[index] = row
            index += 1
        index = 0
        for row in data['score_grid']:
            SCORE_GRID[index] = row
            index += 1
        SELECTED_COLUMN = data['selected_column']
        SELECTED_ROW = data['selected_row']
        update_screen = True


def restart_game():
    ''' Restart game by clearing grids data and updating the screen '''
    global update_screen, PLAYER_GRID, SCORE_GRID, GAME, SELECTED_COLUMN, SELECTED_ROW
    PLAYER_GRID = [["blank"] * 4 for rows in range(8)]
    SCORE_GRID = [["blank"] * 4 for rows in range(8)]
    GAME = MastermindGame(list(PLAYER_COLORS.keys()))
    SELECTED_COLUMN = SELECTED_ROW = 0
    update_screen = True


def go_to_next_position():
    ''' Automatically place cursor to next position for faster answering! '''
    global update_screen
    global SELECTED_COLUMN
    SELECTED_COLUMN += 1
    if (SELECTED_COLUMN >= 4):
        SELECTED_COLUMN = 0
    update_screen = True


def place_color(color):
    ''' Store choosed by player color '''
    global PLAYER_GRID
    PLAYER_GRID[SELECTED_ROW][SELECTED_COLUMN] = color
    go_to_next_position()


white_color = (255, 255, 255)  # create white color (RGB)
''' Create buttons on left pannel '''
check_button = Button(screen, "Check!", (560, 50), 30, yellow_button_img,
                      yellow_button_active_img, (150, 255, 255), check_answer)
SET_CODE_button = Button(screen, "Set code", (560, 115), 28, blue_button_img,
                         blue_button_active_img, white_color, set_code)
ai_button = Button(screen, "AI turn", (560, 180), 30, blue_button_img,
                   blue_button_active_img, (220, 110, 255), ai_turn)
dumb_ai_button = Button(screen, "dumb AI", (560, 245), 30, blue_button_img,
                        blue_button_active_img, (170, 140, 255), random_turn)
save_button = Button(screen, "Save", (560, 310), 32, blue_button_img,
                     blue_button_active_img, (180, 255, 180), save_game)
load_button = Button(screen, "Load", (560, 375), 32, blue_button_img,
                     blue_button_active_img, (180, 180, 255), load_game)
restart_button = Button(screen, "Restart", (560, 440), 30, blue_button_img,
                        blue_button_active_img, (255, 180, 180), restart_game)
exit_button = Button(screen, "", (630, -24), 0, exit_button_img,
                     exit_button_active_img, white_color, exit_game)

''' Create knobs buttons on left bottom pannel '''
red_color_bt = Button(screen, "", (575, 520), 20, red,
                      red, white_color, place_color, "red")
yellow_color_bt = Button(screen, "", (575, 585), 20, yellow,
                         yellow, white_color, place_color, "yellow")
green_color_bt = Button(screen, "", (575, 650), 20, green,
                        green, white_color, place_color, "green")
purple_color_bt = Button(screen, "", (575, 715), 20, purple,
                         purple, white_color, place_color, "purple")
blue_color_bt = Button(screen, "", (640, 520), 20, blue,
                       blue, white_color, place_color, "blue")
white_color_bt = Button(screen, "", (640, 585), 20, white,
                        white, white_color, place_color, "white")
black_color_bt = Button(screen, "", (640, 650), 20, black,
                        black, white_color, place_color, "black")
blank_color_bt = Button(screen, "", (646, 721), 20, blank,
                        blank, white_color, place_color, "blank")

# Store buttons for easier access when updating each of them
buttons = [check_button, SET_CODE_button, ai_button, dumb_ai_button, save_button, load_button,
           restart_button, exit_button, red_color_bt, yellow_color_bt,
           green_color_bt, blue_color_bt, white_color_bt, black_color_bt, purple_color_bt, blank_color_bt]


def draw_buttons():
    for button in buttons:
        button.render()


# Rectangular panel to update only a portion of screen
# Better for perfomance!
update_rect = pygame.Rect(WIDTH - 160, 0, 160, HEIGHT)

#
field_start_y = 89
space_btw_columns = 88.5
space_btw_answers_x = 40
space_btw_player_colors_x = 65

# Store positions of player grid and score grid respectively on which answers are placed
player_board_positions = [[(290 + space_btw_player_colors_x * columns, field_start_y + space_btw_columns * rows)
                           for columns in range(4)] for rows in range(8)]
score_board_positions = [[(68 + space_btw_answers_x * columns, field_start_y + space_btw_columns * rows)
                          for columns in range(4)] for rows in range(8)]


def draw_selection():
    ''' render selector on currebtly selected position on player's grid '''
    x = player_board_positions[SELECTED_ROW][SELECTED_COLUMN][0] - \
        cursor.get_width() / 2
    y = player_board_positions[SELECTED_ROW][SELECTED_COLUMN][1] - \
        cursor.get_height() / 2
    screen.blit(cursor, (x, y))


def draw_grid(positions, imgs, grid):
    ''' render player and score grids '''
    for row in range(len(positions)):  # 8 rows
        for column in range(len(positions[row])):  # 4 columns
            answer = grid[row][column]  # SCORE_GRID or PLAYER_GRID
            img = imgs[answer]
            x = positions[row][column][0] - \
                img.get_width() / 2
            y = positions[row][column][1] - \
                img.get_height() / 2
            screen.blit(img, (x, y))


def select_field(pos):
    ''' select position on player's grid '''
    global PLAYER_GRID, SELECTED_COLUMN, update_screen
    x = pos[0]
    x_positions = [coords[0]
                   for coords in player_board_positions[SELECTED_ROW]]
    distaces = [abs(x - x2) for x2 in x_positions]
    if (min(distaces) > 50):
        return
    if (SELECTED_COLUMN == distaces.index(min(distaces))):
        return
    SELECTED_COLUMN = distaces.index(min(distaces))
    update_screen = True


def draw_possibilities_text():
    ''' Display how many possibilities remain '''
    text = f"Possibilities remain: {GAME.possibilities_remain()}"
    text_surface = FONT.render(text, False, white_color)
    screen.blit(text_surface, (250, 16))  # render text


def draw_game():
    ''' draw all elements in game layer by layer '''
    screen.blit(bg, (0, 0))
    draw_board()
    draw_grid(player_board_positions, PLAYER_COLORS, PLAYER_GRID)
    draw_grid(score_board_positions, SCORE_COLORS, SCORE_GRID)
    draw_buttons()
    draw_possibilities_text()
    draw_selection()
    pygame.display.update()  # Update screen to display changes


def main():
    ''' Main loop of the game. Here Magic happens !'''
    global PLAYER_GRID, SELECTED_COLUMN, update_screen
    PLAYER_GRID = [["blank"] * 4 for i in range(8)]
    # compute how many milliseconds have passed since the previous call
    clock = pygame.time.Clock()
    run = True
    update_buttons_panel = True
    update_screen = True
    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        for button in buttons:
            # Update current state for each button
            button.on_hover_over((mouse_x, mouse_y))
            if (button.check_for_update() == True):  # If button state has changed
                update_buttons_panel = True  # Then update buttons
        for event in pygame.event.get():  # loop for each event in game
            if event.type == pygame.QUIT:  # Escape button or cross pressed
                run = False  # Quit main loop
                break  # Break main loop
            elif event.type == pygame.KEYDOWN:  # If button pressed
                if event.key == pygame.K_RIGHT and SELECTED_COLUMN < 3:  # Move right
                    SELECTED_COLUMN += 1
                    update_screen = True  # Update screen to display cursor on new position
                elif event.key == pygame.K_LEFT and SELECTED_COLUMN > 0:  # Move left
                    SELECTED_COLUMN -= 1
                    update_screen = True  # Update screen to display cursor on new position
                elif event.key == pygame.K_r:  # r for red
                    place_color("red")
                elif event.key == pygame.K_y:  # y for yellow
                    place_color("yellow")
                elif event.key == pygame.K_g:  # g for green
                    place_color("green")
                elif event.key == pygame.K_b:  # b for blue
                    place_color("blue")
                elif event.key == pygame.K_p:  # p for purple
                    place_color("purple")
                elif event.key == pygame.K_w:  # w for white
                    place_color("white")
                elif event.key == pygame.K_k:  # k for black
                    place_color("black")
                elif event.key == pygame.K_SPACE:  # Spacebar is pressed
                    go_to_next_position()  # Automatically move cursor
                elif event.key == pygame.K_RETURN:  # Enter button  for  check answer
                    check_answer()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button is pressed
                for button in buttons:
                    button.on_click(event)  # Check if pressed on button
                # Set current position on grid with mouse
                select_field(event.pos)

        if (update_buttons_panel):
            if (update_screen == False):
                screen.blit(bg, (0, 0))
                # Update only buttons for better perfomance
                draw_buttons()
                pygame.display.update(update_rect)  # Update the screen
            update_buttons_panel = False

        if (update_screen):
            # Update the screen when needed
            draw_game()
            update_screen = False

        # Set target FPS to 30
        clock.tick(30)
    # Quit if game doesn't run (run = False)
    pygame.quit()


if __name__ == "__main__":
    # run game only from this script
    main()

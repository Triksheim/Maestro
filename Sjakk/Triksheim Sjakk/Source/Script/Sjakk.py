import numpy
import pygame
import sys
import math
import time

ROW_COUNT = 8
COL_COUNT = 8
SQUARESIZE = 100

# Functions ----------------------------------------------------------------------------------------------------------
# Create matrix of zeroes for board data
def create_board():
    board = numpy.zeros((ROW_COUNT, COL_COUNT))
    return board

# Draws chessboard squares
def draw_board():

    outer_tile_rect = 0, 0
    screen.blit(outer_tile, outer_tile_rect)

    outer_tile2_rect = SQUARESIZE-37, SQUARESIZE-39
    screen.blit(outer_tile2, outer_tile2_rect)

    for c in range(1, COL_COUNT+1, 2):
        for r in range(1, ROW_COUNT+1 , 2):
            light_tile_rect = r * SQUARESIZE, c * SQUARESIZE
            screen.blit(light_tile,light_tile_rect)
    for c in range(2, COL_COUNT+1, 2):
        for r in range(2, ROW_COUNT+1, 2):
            light_tile_rect = r * SQUARESIZE, c * SQUARESIZE
            screen.blit(light_tile, light_tile_rect)
    for c in range(1, COL_COUNT+1, 2):
         for r in range(2, ROW_COUNT+1, 2):
            dark_tile_rect = r * SQUARESIZE, c * SQUARESIZE
            screen.blit(dark_tile, dark_tile_rect)
    for c in range(2, COL_COUNT+1, 2):
        for r in range(1, ROW_COUNT+1, 2):
            dark_tile_rect = r * SQUARESIZE, c * SQUARESIZE
            screen.blit(dark_tile, dark_tile_rect)

# Place starting pieces. White is positive and black is negative values
# 1 = pawn, 2 = rook, 3 = knight, 4 = bishop, 5 = queen, 6 = king
def place_starting_pieces(board):
    for c in range(COL_COUNT):
        board[1][c] = -1
        board[6][c] = 1
    board[0][0] = -2
    board[0][7] = -2
    board[0][1] = -3
    board[0][6] = -3
    board[0][2] = -4
    board[0][5] = -4
    board[0][3] = -5
    board[0][4] = -6
    board[7][0] = 2
    board[7][7] = 2
    board[7][1] = 3
    board[7][6] = 3
    board[7][2] = 4
    board[7][5] = 4
    board[7][3] = 5
    board[7][4] = 6

# Moves pieces in board data
def move_piece(board, col, row, pick_or_place, turn):
    # 0 = white turn, 1 = black turn
    if turn == 0:
        if pick_or_place == 0:
            picked_piece = int(board[row][col])     # Picks piece from board data
            if picked_piece >= 1:                   # Checks for correct piece color
                board[row][col] = 0                 # Clears piece from picked square
                pick_or_place += 1
                print("Picked white piece")
                return picked_piece, col, row, pick_or_place, turn
            elif pick_or_place == 0:
                print("Invalid white pick")
                return picked_piece, col, row, pick_or_place, turn
        else:
            # Checks if picked place is a new position and no piece of same color on square
            game_over = False
            if board[row][col] <= 0 and not (row == row_store and col == col_store):
                if validate_piece_placement(board,picked_piece_store, row_store, col_store, row, col):
                    if picked_piece_store == 1 and row == 0:    # Promoting pawn
                        board[row][col] = 5
                        pick_or_place -= 1
                        print(board)
                        print("Placed white piece")
                        print("White pawn promoted")
                        turn += 1
                        return pick_or_place, turn, game_over
                    else:
                        board[row][col] = picked_piece_store    # Placing the piece in board data
                        pick_or_place -= 1
                        print(board)
                        print("Placed white piece")
                        turn += 1                               # Switches turn
                        if white_king_check(board) or black_king_check(board):
                            game_over = True
                        return pick_or_place, turn, game_over
                else:
                    board[row_store][col_store] = picked_piece_store
                    pick_or_place -= 1
                    print("Move validation failed")
                    return pick_or_place, turn, game_over
            else:
                board[row_store][col_store] = picked_piece_store
                pick_or_place -= 1
                print("Invalid white placement")
                return pick_or_place, turn, game_over

    if turn == 1:
        if pick_or_place == 0:
            picked_piece = int(board[row][col])
            if picked_piece <= -1:
                board[row][col] = 0
                pick_or_place += 1
                print("Picked black piece")
                return picked_piece, col, row, pick_or_place, turn
            elif pick_or_place == 0:
                print("Invalid black pick")
                return picked_piece, col, row, pick_or_place, turn
        else:
            game_over = False
            if board[row][col] >= 0 and not (row == row_store and col == col_store):
                if validate_piece_placement(board, picked_piece_store, row_store, col_store, row, col):
                    if picked_piece_store == -1 and row == 7:
                        board[row][col] = -5
                        pick_or_place -= 1
                        print(board)
                        print("Placed black piece")
                        print("Black pawn promoted")
                        turn -= 1
                        return pick_or_place, turn, game_over
                    else:
                        board[row][col] = picked_piece_store
                        pick_or_place -= 1
                        print(board)
                        print("Placed black piece")
                        turn -= 1
                        if white_king_check(board) or black_king_check(board):
                            game_over = True
                        return pick_or_place, turn, game_over
                else:
                    board[row_store][col_store] = picked_piece_store
                    pick_or_place -= 1
                    print("Move validation failed")
                    return pick_or_place, turn, game_over
            else:
                board[row_store][col_store] = picked_piece_store
                pick_or_place -= 1
                print("Invalid black placement")
                return pick_or_place, turn, game_over

def validate_piece_placement(board,picked_piece, picked_row, picked_col, place_row, place_col):

    # Validate pawn move
    if picked_piece == 1:
        if picked_row == place_row + 1 and picked_col == place_col and board[place_row][place_col] == 0:
            return True
        elif picked_row == 6 and picked_row == place_row + 2 and picked_col == place_col:
            return True
        elif picked_row == place_row + 1 and abs(picked_col - place_col) == 1 and board[place_row][place_col] < 0:
            return True
        else:
            return False
    elif picked_piece == -1:
        if picked_row == place_row - 1 and picked_col == place_col and board[place_row][place_col] == 0:
            return True
        elif picked_row == 1 and picked_row == place_row - 2 and picked_col == place_col:
            return True
        elif picked_row == place_row - 1 and abs(picked_col - place_col) == 1 and board[place_row][place_col] > 0:
            return True
        else:
            return False

    # Validate knight move
    elif picked_piece == 3 or picked_piece == -3:
        if picked_row == place_row + 2 and (picked_col == place_col + 1 or picked_col == place_col - 1):
            return True
        elif picked_row == place_row + 1 and (picked_col == place_col + 2 or picked_col == place_col - 2):
            return True
        elif picked_row == place_row - 2 and (picked_col == place_col + 1 or picked_col == place_col - 1):
            return True
        elif picked_row == place_row - 1 and (picked_col == place_col + 2 or picked_col == place_col - 2):
            return True
        else:
            return False

    # Validate rook move
    elif picked_piece == 2 or picked_piece == -2:
        if picked_col == place_col:
            for r in range(abs(picked_row - place_row)):
                if picked_row > place_row:
                    if board[picked_row - r][picked_col] != 0:
                        return False
                elif picked_row < place_row:
                    if board[picked_row + r][picked_col] != 0:
                        return False
            return True
        elif picked_row == place_row:
            for r in range(abs(picked_col - place_col)):
                if picked_col > place_col:
                    if board[picked_row][picked_col - r] != 0:
                        return False
                elif picked_col < place_col:
                    if board[picked_row][picked_col + r] != 0:
                        return False
            return True

    # Validate bishop move
    elif picked_piece == 4 or picked_piece == -4:
        if picked_col != place_col and picked_row != place_row and (abs(picked_row - place_row) - abs(picked_col - place_col)) == 0:
            check = (place_row + place_col) % 2
            print(check)
            for r in range(abs(picked_row - place_row)):
                if picked_row > place_row and picked_col > place_col:
                    if board[picked_row - r][picked_col - r] != 0:
                        return False
                elif picked_row > place_row and picked_col < place_col:
                    if board[picked_row - r][picked_col + r] != 0:
                        return False
                elif picked_row < place_row and picked_col > place_col:
                    if board[picked_row + r][picked_col - r] != 0:
                        return False
                elif picked_row < place_row and picked_col < place_col:
                    if board[picked_row + r][picked_col + r] != 0:
                        return False
            return True
        else:
            return False

    # Validate queen move
    elif picked_piece == 5 or picked_piece == -5:
        if picked_col == place_col:
            for r in range(abs(picked_row - place_row)):
                if picked_row > place_row:
                    if board[picked_row - r][picked_col] != 0:
                        return False
                elif picked_row < place_row:
                    if board[picked_row + r][picked_col] != 0:
                        return False
            return True
        elif picked_row == place_row:
            for r in range(abs(picked_col - place_col)):
                if picked_col > place_col:

                    if board[picked_row][picked_col - r] != 0:
                        return False
                elif picked_col < place_col:
                    if board[picked_row][picked_col + r] != 0:
                        return False
            return True
        elif picked_col != place_col and picked_row != place_row and (abs(picked_row - place_row) - abs(picked_col - place_col)) == 0:
            for r in range(abs(picked_row - place_row)):
                if picked_row > place_row and picked_col > place_col:
                    if board[picked_row - r][picked_col - r] != 0:
                        return False
                elif picked_row > place_row and picked_col < place_col:
                    if board[picked_row - r][picked_col + r] != 0:
                        return False
                elif picked_row < place_row and picked_col > place_col:
                    if board[picked_row + r][picked_col - r] != 0:
                        return False
                elif picked_row < place_row and picked_col < place_col:
                    if board[picked_row + r][picked_col + r] != 0:
                        return False
            return True
        else:
            return False

    # Validate king move
    elif picked_piece == 6 or picked_piece == -6:
        if (picked_row == place_row + 1 and picked_col == place_col) or (
                picked_row == place_row - 1 and picked_col == place_col):
            return True
        elif (picked_row == place_row and picked_col == place_col + 1) or (
                picked_row == place_row and picked_col == place_col - 1):
            return True
        elif (picked_col == place_col + 1 or picked_col == place_col + -1) and (picked_row == place_row + 1 or picked_row == place_row + -1):
            return True
        else:
            return False
    else:
        return False

# Draws pieces on board based on board data
def draw_pieces(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):                      # Runs through board data
            # White
            if board[c][r] == 1:                        # Checks for piece type
                pawn_rect = (r+1)*SQUARESIZE, (c+1)*SQUARESIZE  # Calculates square location
                screen.blit(pawn, pawn_rect)            # Draws piece from corresponding image at square location
            elif board[c][r] == 2:
                rook_rect = (r+1) * SQUARESIZE, (c+1) * SQUARESIZE
                screen.blit(rook, rook_rect)
            elif board[c][r] == 3:
                knight_rect = ((r+1) * SQUARESIZE) + 5, ((c+1) * SQUARESIZE) + 10
                screen.blit(knight, knight_rect)
            elif board[c][r] == 4:
                bishop_rect = (r+1) * SQUARESIZE, (c+1) * SQUARESIZE
                screen.blit(bishop, bishop_rect)
            elif board[c][r] == 5:
                queen_rect = (r+1) * SQUARESIZE, (c+1) * SQUARESIZE
                screen.blit(queen, queen_rect)
            elif board[c][r] == 6:
                king_rect = (r+1) * SQUARESIZE+2, (c+1) * SQUARESIZE
                screen.blit(king, king_rect)

            # Black
            elif board[c][r] == -1:
                pawn_rect_b = (r+1)*SQUARESIZE, (c+1)*SQUARESIZE
                screen.blit(pawn_b, pawn_rect_b)
            elif board[c][r] == -2:
                rook_rect_b = (r+1) * SQUARESIZE, (c+1) * SQUARESIZE
                screen.blit(rook_b, rook_rect_b)
            elif board[c][r] == -3:
                knight_rect_b = (r+1) * SQUARESIZE, (c+1) * SQUARESIZE
                screen.blit(knight_b, knight_rect_b)
            elif board[c][r] == -4:
                bishop_rect_b = ((r+1) * SQUARESIZE) +15, ((c+1) * SQUARESIZE) + 15
                screen.blit(bishop_b, bishop_rect_b)
            elif board[c][r] == -5:
                queen_rect_b = ((r+1) * SQUARESIZE) +5, ((c+1) * SQUARESIZE) +5
                screen.blit(queen_b, queen_rect_b)
            elif board[c][r] == -6:
                king_rect_b = (r+1) * SQUARESIZE+2, (c+1) * SQUARESIZE
                screen.blit(king_b, king_rect_b)

# Drags a picked piece at mouse location until placed
def drag_piece(picked_piece_store, turn, board):
    if picked_piece_store == 1 and turn == 0:           # Checks piece and color
        mouse_x, mouse_y = pygame.mouse.get_pos()       # Get current mouse position
        pawn_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(pawn, pawn_drag)                    # Draws image on mouse position
    elif picked_piece_store == 2 and turn == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rook_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(rook, rook_drag)
    elif picked_piece_store == 3 and turn == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        knight_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(knight, knight_drag)
    elif picked_piece_store == 4 and turn == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bishop_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(bishop, bishop_drag)
    elif picked_piece_store == 5 and turn == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        queen_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(queen, queen_drag)
    elif picked_piece_store == 6 and turn == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        king_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(king, king_drag)

    # Black pieces
    elif picked_piece_store == -1 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pawn_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(pawn_b, pawn_b_drag)
    elif picked_piece_store == -2 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rook_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(rook_b, rook_b_drag)
    elif picked_piece_store == -3 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        knight_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(knight_b, knight_b_drag)
    elif picked_piece_store == -4 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bishop_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(bishop_b, bishop_b_drag)
    elif picked_piece_store == -5 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        queen_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(queen_b, queen_b_drag)
    elif picked_piece_store == -6 and turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        king_b_drag = int(mouse_x-50), int(mouse_y-50)
        screen.blit(king_b, king_b_drag)
    # pygame.display.update()
    # draw_board()

#   Gets mouse position at event trigger
def get_event_mouse_pos(event):
    posx = event.pos[0]
    posy = event.pos[1]
    col = int(math.floor(posx / SQUARESIZE)) -1
    row = int(math.floor(posy / SQUARESIZE)) -1
    # Outside board check, picks nearest square instead
    if col == -1 and row == -1:
        col += 1
        row += 1
        return col, row
    elif col == 8 and row == 8:
        col -= 1
        row -= 1
        return col, row
    elif col == 8 and row == -1:
        col -= 1
        row += 1
        return col, row
    elif col == -1 and row == 8:
        col += 1
        row -= 1
        return col, row
    elif col == -1:
        col += 1
        return col, row
    elif col == 8:
        col -= 1
        return col, row
    elif row == -1:
        row += 1
        return col, row
    elif row == 8:
        row -= 1
        return col, row
    else:
        return col, row

def calc_score(board):
    white_score = 0
    black_score = 0
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] > 0:
                if board[r][c] == 1:
                    white_score += 1
                elif board[r][c] == 2:
                    white_score += 5
                elif board[r][c] == 3 or board[r][c] == 4:
                    white_score += 3
                elif board[r][c] == 5:
                    white_score += 10
            elif board[r][c] < 0:
                if board[r][c] == -1:
                    black_score += 1
                elif board[r][c] == -2:
                    black_score += 5
                elif board[r][c] == -3 or board[r][c] == -4:
                    black_score += 3
                elif board[r][c] == -5:
                    black_score += 10
    white_score_diff = white_score - black_score
    black_score_diff = black_score - white_score
    return white_score_diff, black_score_diff

def timer_white(time_start, white_time_limit, used_black_time):
    time_now = time.time()
    time_elapsed =int(math.floor(time_now - time_start))
    white_time = white_time_limit - time_elapsed + used_black_time
    if white_time <= 0:
        game_over = True
    else:
        game_over = False
    return white_time, game_over

def timer_black(time_start,black_time_limit, used_white_time):
    time_now = time.time()
    time_elapsed =int(math.floor(time_now - time_start))
    black_time = black_time_limit - time_elapsed + used_white_time
    if black_time <= 0:
        game_over = True
    else:
        game_over = False
    return black_time, game_over

def format_time(time):
    mins, secs = divmod(time,60)
    timeformat = "{:02d}:{:02d}".format(mins,secs)
    return timeformat

def white_king_check(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 6:
                return False
    return True

def black_king_check(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == -6:
                return False
    return True

# ---------------------------------------------------------------------------------------------------------------------

# Setup ---
pygame.init()
pygame.display.set_caption("Triksheim Chess")

# Resize game window
width = (COL_COUNT + 2) * SQUARESIZE
height = (ROW_COUNT + 2) * SQUARESIZE
size = width, height
screen = pygame.display.set_mode(size)

# # Load and resize board image
light_tile = pygame.image.load("light_wood.png")
light_tile = pygame.transform.scale(light_tile,(int(SQUARESIZE),int(SQUARESIZE)))
dark_tile = pygame.image.load("dark_wood.png")
dark_tile = pygame.transform.scale(dark_tile,(int(SQUARESIZE),int(SQUARESIZE)))
outer_tile = pygame.image.load("outer_wood.jpg")
outer_tile = pygame.transform.scale(outer_tile,(1000,1000))
outer_tile2 = pygame.image.load("outer_wood2.jpg")
outer_tile2 = pygame.transform.scale(outer_tile2,(875,875))

# Load and resize image of white pieces
pawn = pygame.image.load("pawn.png")
pawn = pygame.transform.scale(pawn,(int(SQUARESIZE),int(SQUARESIZE)))
rook = pygame.image.load("rook.png")
rook = pygame.transform.scale(rook,(int(SQUARESIZE),int(SQUARESIZE)))
knight = pygame.image.load("knight.png")
knight = pygame.transform.scale(knight,(int(SQUARESIZE-20),int(SQUARESIZE-20)))
bishop = pygame.image.load("bishop.png")
bishop = pygame.transform.scale(bishop,(int(SQUARESIZE),int(SQUARESIZE)))
queen = pygame.image.load("queen.png")
queen = pygame.transform.scale(queen,(int(SQUARESIZE),int(SQUARESIZE)))
king = pygame.image.load("king.png")
king = pygame.transform.scale(king,(int(SQUARESIZE-5),int(SQUARESIZE-5)))

# Load and resize image of black pieces
pawn_b = pygame.image.load("pawn_b.png")
pawn_b = pygame.transform.scale(pawn_b,(int(SQUARESIZE),int(SQUARESIZE)))
rook_b = pygame.image.load("rook_b.png")
rook_b = pygame.transform.scale(rook_b,(int(SQUARESIZE),int(SQUARESIZE)))
knight_b = pygame.image.load("knight_b.png")
knight_b = pygame.transform.scale(knight_b,(int(SQUARESIZE),int(SQUARESIZE)))
bishop_b = pygame.image.load("bishop_b.png")
bishop_b = pygame.transform.scale(bishop_b,(int(SQUARESIZE-25),int(SQUARESIZE-25)))
queen_b = pygame.image.load("queen_b.png")
queen_b = pygame.transform.scale(queen_b,(int(SQUARESIZE-11),int(SQUARESIZE-11)))
king_b = pygame.image.load("king_b.png")
king_b = pygame.transform.scale(king_b,(int(SQUARESIZE-5),int(SQUARESIZE-5)))

game_over = False
turn = 0
picked_piece = 0
picked_piece_store = 0
pick_or_place = 0
white_score = 0
black_score = 0
white_time_limit = 900
black_time_limit = 900
white_time = white_time_limit
black_time = black_time_limit
used_white_time = 0
used_black_time = 0
time_start = time.time()
board = create_board()
place_starting_pieces(board)
draw_board()
draw_pieces(board)
print(board)
print("Starting pieces placed")
font = pygame.font.SysFont("Cambria", 50)
font_win = pygame.font.SysFont("Cambria", 250)
text_white_score = font.render("", 0, (255, 255, 255))
text_black_score = font.render("", 0, (125, 125, 125))
text_white_time = font.render(str(white_time_limit), 0, (255, 255, 255))
text_black_time = font.render(str("15:00"), 0, (200, 200, 200))
text_white_turn = font.render(str(">             <"), 0, (255, 255, 255))
text_black_turn = font.render(str(">             <"), 0, (200, 200, 200))
# Setup end ---

# Main game loop
while not game_over:
    if turn == 0:
        used_black_time = black_time_limit - black_time
        white_time, game_over = timer_white(time_start, white_time_limit, used_black_time)
        white_time_formatted = format_time(white_time)
        text_white_time = font.render(str(white_time_formatted), 0, (255, 255, 255))
    elif turn == 1:
        used_white_time = white_time_limit - white_time
        black_time, game_over = timer_black(time_start, black_time_limit, used_white_time)
        black_time_formatted = format_time(black_time)
        text_black_time = font.render(str(black_time_formatted), 0, (200, 200, 200))
    for event in pygame.event.get():                                # Checks for events and clears
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:                          # Quit when ESC pressed
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:                  # True when a mousebutton is pressed
            col, row = get_event_mouse_pos(event)                   # Get mouse position at event trigger
            if pick_or_place == 0:                                  # 0 = Picking and 1 = already picked piece
                picked_piece_store, col_store, row_store,pick_or_place, turn, \
                = move_piece(board, col, row, pick_or_place, turn)  # Picks piece
            else:
                pick_or_place, turn, game_over = move_piece(board, col, row, pick_or_place, turn)  # Places piece
                white_score, black_score = calc_score(board)                            # Calc score
                if white_score > 0:
                    text_white_score = font.render("+" + str(white_score), 0, (255, 255, 255))
                    text_black_score = font.render("", 0, (200, 200, 200))
                elif white_score < 0:
                    text_white_score = font.render("", 0, (255, 255, 255))
                    text_black_score = font.render("+" + str(black_score), 0, (200, 200, 200))
                else:
                    text_white_score = font.render("" , 0, (255, 255, 255))
                    text_black_score = font.render("", 0, (200, 200, 200))

    draw_pieces(board)  # Draws chess pieces based on board data
    if turn == 0:
        screen.blit(text_white_turn, (769, 940))
    else:
        screen.blit(text_black_turn, (769, 0))
    screen.blit(text_white_score, (62, 940))
    screen.blit(text_black_score, (62, 0))
    screen.blit(text_white_time, (800, 940))
    screen.blit(text_black_time, (800, 0))
    if pick_or_place == 1:
        drag_piece(picked_piece_store, turn, board)  # Drag picked piece at mouse position
    pygame.display.update()
    draw_board()

while game_over:
    for event in pygame.event.get():
        draw_pieces(board)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif white_time <= 0 or turn == 0:
            text_black_win = font_win.render(str("WINNER"), 0, (0, 0, 0))
            screen.blit(text_black_win, (5, 350))
        elif black_time <= 0 or turn == 1:
            text_white_win = font_win.render(str("WINNER"), 0, (255, 255, 255))
            screen.blit(text_white_win, (5, 350))
        screen.blit(text_white_score, (62, 940))
        screen.blit(text_black_score, (62, 0))
        screen.blit(text_white_time, (800, 940))
        screen.blit(text_black_time, (800, 0))
        pygame.display.update()
        draw_board()

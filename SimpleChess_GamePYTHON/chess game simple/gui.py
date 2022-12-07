'''
Developed by: Frederico Jordan

@author: fvj
'''
import pygame, chessgame
from pygame.locals import *
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

SQUARE_SIDE = 55
CLOCK_SIDE = 250
AI_SEARCH_DEPTH = 2

CLOCK_BACKGROUND = (0,0,0)
RED_CHECK          = (240, 150, 150)
WHITE              = (255, 255, 255)
BLUE_LIGHT         = (140, 184, 219)
BLUE_DARK          = (91,  131, 159)
GRAY_LIGHT         = (240, 240, 240)
GRAY_DARK          = (200, 200, 200)
CHESSWEBSITE_LIGHT = (212, 202, 190)
CHESSWEBSITE_DARK  = (100,  92,  89)
LICHESS_LIGHT      = (240, 217, 181)
LICHESS_DARK       = (181, 136,  99)
LICHESS_GRAY_LIGHT = (164, 164, 164)
LICHESS_GRAY_DARK  = (136, 136, 136)

BOARD_COLORS = [(GRAY_LIGHT, GRAY_DARK),
                (BLUE_LIGHT, BLUE_DARK),
                (WHITE, BLUE_LIGHT),
                (CHESSWEBSITE_LIGHT, CHESSWEBSITE_DARK),
                (LICHESS_LIGHT, LICHESS_DARK),
                (LICHESS_GRAY_LIGHT, LICHESS_GRAY_DARK)]
BOARD_COLOR = choice(BOARD_COLORS)

BLACK_KING   = pygame.image.load('images/black_king.png')
BLACK_QUEEN  = pygame.image.load('images/black_queen.png')
BLACK_ROOK   = pygame.image.load('images/black_rook.png')
BLACK_BISHOP = pygame.image.load('images/black_bishop.png')
BLACK_KNIGHT = pygame.image.load('images/black_knight.png')
BLACK_PAWN   = pygame.image.load('images/black_pawn.png')
BLACK_JOKER  = pygame.image.load('images/black_joker.png')

WHITE_KING   = pygame.image.load('images/white_king.png')
WHITE_QUEEN  = pygame.image.load('images/white_queen.png')
WHITE_ROOK   = pygame.image.load('images/white_rook.png')
WHITE_BISHOP = pygame.image.load('images/white_bishop.png')
WHITE_KNIGHT = pygame.image.load('images/white_knight.png')
WHITE_PAWN   = pygame.image.load('images/white_pawn.png')
WHITE_JOKER  = pygame.image.load('images/white_joker.png')

CLOCK = pygame.time.Clock()
CLOCK_TICK = 30

SCREEN = pygame.display.set_mode((8*SQUARE_SIDE, 8*SQUARE_SIDE + CLOCK_SIDE), pygame.RESIZABLE)
SCREEN_TITLE = 'Chess Game'

# -----------clock setting-----------

font = pygame.font.Font("fonts/BowlbyOneSC.ttf", 34)
# -----------------------------------
pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))
clock_image = pygame.image.load("images/clock.png")
clock_image = pygame.transform.scale(clock_image, (440, CLOCK_SIDE))
pygame.display.set_caption(SCREEN_TITLE)

def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode((8*square_side_len, 8*square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len

def print_empty_board():
    SCREEN.fill(BOARD_COLOR[0])
    paint_dark_squares(BOARD_COLOR[1])
    
def paint_square(square, square_color):
    col = chessgame.FILES.index(square[0])
    row = 7-chessgame.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 0)
    pygame.draw.rect(SCREEN, CLOCK_BACKGROUND, (0, SQUARE_SIDE*8, SQUARE_SIDE*8 , SQUARE_SIDE+CLOCK_SIDE),0)

def paint_dark_squares(square_color):
    for position in chessgame.single_gen(chessgame.DARK_SQUARES):
        paint_square(chessgame.bb2str(position), square_color)
            
def get_square_rect(square):
    col = chessgame.FILES.index(square[0])
    row = 7-chessgame.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE,SQUARE_SIDE))

def coord2str(position, color=chessgame.WHITE):
    if color == chessgame.WHITE:
        file_index = int(position[0]/SQUARE_SIDE)
        rank_index = 7 - int(position[1]/SQUARE_SIDE)
        return chessgame.FILES[file_index] + chessgame.RANKS[rank_index]
    if color == chessgame.BLACK:
        file_index = 7 - int(position[0]/SQUARE_SIDE)
        rank_index = int(position[1]/SQUARE_SIDE)
        return chessgame.FILES[file_index] + chessgame.RANKS[rank_index]
    
def print_board(board, color=chessgame.WHITE):

    if color == chessgame.WHITE:
        printed_board = board
    if color == chessgame.BLACK:
        printed_board = chessgame.rotate_board(board)
    
    print_empty_board()
    
    if chessgame.is_check(board, chessgame.WHITE):
        paint_square(chessgame.bb2str(chessgame.get_king(printed_board, chessgame.WHITE)), RED_CHECK)
    if chessgame.is_check(board, chessgame.BLACK):
        paint_square(chessgame.bb2str(chessgame.get_king(printed_board, chessgame.BLACK)), RED_CHECK)
    
    SCREEN.blit(clock_image, (0,440))

    for position in chessgame.colored_piece_gen(printed_board, chessgame.KING, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KING,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.QUEEN, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_QUEEN,  (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.ROOK, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_ROOK,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.BISHOP, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_BISHOP, (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.KNIGHT, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KNIGHT, (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.PAWN, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_PAWN,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.JOKER, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_JOKER,  (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
        
    for position in chessgame.colored_piece_gen(printed_board, chessgame.KING, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KING,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.QUEEN, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_QUEEN,  (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.ROOK, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_ROOK,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.BISHOP, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_BISHOP, (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.KNIGHT, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KNIGHT, (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.PAWN, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_PAWN,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.JOKER, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_JOKER,  (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
        
    pygame.display.flip()
    
def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()
    
def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chessgame.make_move(game, chessgame.get_AI_move(game, AI_SEARCH_DEPTH))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, color)
    return new_game

def try_move(game, attempted_move):
    for move in chessgame.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chessgame.make_move(game, move)
    return game

def play_as(game, color):
    run = True
    ongoing = True
    joker = 0

    time_a = 300
    time_b = 300
    a_on = False
    b_on = True
    
    try:
        while run:
            CLOCK.tick(CLOCK_TICK)
            print_board(game.board, color)
            
            if chessgame.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chessgame.get_outcome(game))
                ongoing = False
            
            if ongoing and game.to_move == chessgame.opposing_color(color):
                game = make_AI_move(game, color)
            
            if chessgame.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chessgame.get_outcome(game))
                ongoing = False
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == USEREVENT:
                    if time_a > 0:
                        time_a -= 1
                    else:
                        pygame.time.set_timer(USEREVENT, 0)

                elif event.type == (USEREVENT + 1):
                    if time_b > 0:
                        time_b -= 1
                    else:
                        pygame.time.set_timer(USEREVENT, 0)
                
                #--------------------
                if event.type == pygame.MOUSEBUTTONDOWN:
                    leaving_square = coord2str(event.pos, color)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, color)
                    
                    if ongoing and game.to_move == color:
                        move = (chessgame.str2bb(leaving_square), chessgame.str2bb(arriving_square))
                        game = try_move(game, move)
                        print_board(game.board, color)
                    
                    if not a_on:
                        # Set for 1 second (1000 milliseconds)
                        pygame.time.set_timer(USEREVENT, 1000)
                        pygame.time.set_timer(USEREVENT + 1, 0)
                        b_on = False
                        a_on = True
                        print("A turned On")
                        print("B turned Off")
                    else:
                        # The other one should turn on immediately
                        pygame.time.set_timer(USEREVENT, 0)
                        pygame.time.set_timer(USEREVENT + 1, 1000)
                        b_on = True
                        a_on = False
                        print("B turned On")
                        print("A turned Off")

                #----------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing: # H key
                        game = make_AI_move(game, color)
                    if event.key == 117: # U key
                        game = chessgame.unmake_move(game)
                        game = chessgame.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        print_board(game.board, color)
                        ongoing = True
                    if event.key == 99: # C key
                        global BOARD_COLOR
                        new_colors = deepcopy(BOARD_COLORS)
                        new_colors.remove(BOARD_COLOR)
                        BOARD_COLOR = choice(new_colors)
                        print_board(game.board, color)
                    if event.key == 112 or event.key == 100: # P or D key
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101: # E key
                        print('eval = ' + str(chessgame.evaluate_game(game)/100))
                    if event.key == 106: # J key
                        joker += 1
                        if joker == 13 and chessgame.get_queen(game.board, color):
                            queen_index = chessgame.bb2index(chessgame.get_queen(game.board, color))
                            game.board[queen_index] = color|chessgame.JOKER
                            print_board(game.board, color)
                
                if event.type == pygame.VIDEORESIZE:
                    if SCREEN.get_height() != event.h:
                        resize_screen(int(event.h/8.0))
                    elif SCREEN.get_width() != event.w:
                        resize_screen(int(event.w/8.0))
                    print_board(game.board, color)

            # Format time into minutes:seconds
            time_a_str = "%d:%02d" % (int(time_a/60),int(time_a%60))
            time_b_str = "%d:%02d" % (int(time_b/60),int(time_b%60))

            print(time_a)
            print(time_b)

            time_a_txt = font.render(time_a_str, 1, (255, 255, 255))
            time_b_txt = font.render(time_b_str, 1, (255, 255, 255))

            time_a_rect = time_a_txt.get_rect()
            time_a_rect.center = (120, 580)
            time_b_rect = time_b_txt.get_rect()
            time_b_rect.center = (330, 580)
            
            SCREEN.blit(time_a_txt, time_a_rect)
            SCREEN.blit(time_b_txt, time_b_rect)
            
            pygame.display.update()
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as WHITE:\n\t' if color == chessgame.WHITE else '\nPlaying as BLACK:\n\t')
        bug_file.write(game.get_move_list() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()

def play_as_white(game=chessgame.blitz()):
    return play_as(game, chessgame.WHITE)

def play_as_black(game=chessgame.blitz()):
    return play_as(game, chessgame.BLACK)

def play_random_color(game=chessgame.blitz()):
    color = choice([chessgame.WHITE, chessgame.BLACK])
    play_as(game, color)

# chessgame.verbose = True
play_random_color()

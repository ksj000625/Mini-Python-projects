'''공개 SW 실무'''
'''김성진 권상훈 김하랑 채연우 홍수민'''

import pygame
import chessgame
from pygame.locals import *
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
import os
import sys
import tkinter as tk

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

SQUARE_SIDE = 95
CLOCK_SIDE = 280

CLOCK_BACKGROUND = (0, 0, 0)
RED_CHECK = (240, 150, 150)

LICHESS_LIGHT = (240, 217, 181)
LICHESS_DARK = (181, 136,  99)


BOARD_COLORS = [(LICHESS_LIGHT, LICHESS_DARK)]
BOARD_COLOR = choice(BOARD_COLORS)

BLACK_KING = pygame.image.load('images/black_king.png')
BLACK_QUEEN = pygame.image.load('images/black_queen.png')
BLACK_ROOK = pygame.image.load('images/black_rook.png')
BLACK_BISHOP = pygame.image.load('images/black_bishop.png')
BLACK_KNIGHT = pygame.image.load('images/black_knight.png')
BLACK_PAWN = pygame.image.load('images/black_pawn.png')
BLACK_JOKER = pygame.image.load('images/black_joker.png')

WHITE_KING = pygame.image.load('images/white_king.png')
WHITE_QUEEN = pygame.image.load('images/white_queen.png')
WHITE_ROOK = pygame.image.load('images/white_rook.png')
WHITE_BISHOP = pygame.image.load('images/white_bishop.png')
WHITE_KNIGHT = pygame.image.load('images/white_knight.png')
WHITE_PAWN = pygame.image.load('images/white_pawn.png')
WHITE_JOKER = pygame.image.load('images/white_joker.png')

CLOCK = pygame.time.Clock()
CLOCK_TICK = 30

SCREEN = pygame.display.set_mode(
    (8*SQUARE_SIDE, 8*SQUARE_SIDE), pygame.RESIZABLE)
SCREEN_TITLE = 'Chess Game'

# -----------clock setting-----------
font = pygame.font.Font("fonts/BowlbyOneSC.ttf", 34)
# -----------------------------------
pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))
clock_image = pygame.image.load("images/clock.png")
clock_image = pygame.transform.scale(clock_image, (500, CLOCK_SIDE))
pygame.display.set_caption(SCREEN_TITLE)
pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))

global play_mode   # 0은 시작하기 전, 1은 classic, 2는 blitz
play_mode = 0
global ai_depth    # easy: 1, normal: 2, hard: 3
ai_depth = 1

global time_a
time_a = 300
global time_b
time_b = 300

# -----------image setting-----------
ai_easy = pygame.image.load("images/ai-easy.png")
ai_easy = pygame.transform.scale(ai_easy, (300, 2.5 * SQUARE_SIDE))
ai_normal = pygame.image.load("images/ai-middle.jpeg")
ai_normal = pygame.transform.scale(ai_normal, (300, 2.5 * SQUARE_SIDE))
ai_hard = pygame.image.load("images/ai-hard.png")
ai_hard = pygame.transform.scale(ai_hard, (300, 2.5 * SQUARE_SIDE))
player_pic = pygame.image.load("images/player.png")
player_pic = pygame.transform.scale(player_pic, (300, 2.5 * SQUARE_SIDE))
# -----------------------------------


def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode(
        (8*square_side_len, 8*square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len


def print_empty_board():
    SCREEN.fill(BOARD_COLOR[0])
    paint_dark_squares(BOARD_COLOR[1])


def paint_square(square, square_color):
    col = chessgame.FILES.index(square[0])
    row = 7-chessgame.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE*col,
                     SQUARE_SIDE*row, SQUARE_SIDE, SQUARE_SIDE), 0)
    pygame.draw.rect(SCREEN, CLOCK_BACKGROUND, (8 * SQUARE_SIDE,
                     0, 8 * SQUARE_SIDE + 500, 8 * SQUARE_SIDE), 0)


def paint_dark_squares(square_color):
    for position in chessgame.single_gen(chessgame.DARK_SQUARES):
        paint_square(chessgame.bb2str(position), square_color)


def get_square_rect(square):
    col = chessgame.FILES.index(square[0])
    row = 7-chessgame.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE, SQUARE_SIDE))


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
    global play_mode
    global ai_depth

    if color == chessgame.WHITE:
        printed_board = board
    if color == chessgame.BLACK:
        printed_board = chessgame.rotate_board(board)

    print_empty_board()

    if chessgame.is_check(board, chessgame.WHITE):
        paint_square(chessgame.bb2str(chessgame.get_king(
            printed_board, chessgame.WHITE)), RED_CHECK)
    if chessgame.is_check(board, chessgame.BLACK):
        paint_square(chessgame.bb2str(chessgame.get_king(
            printed_board, chessgame.BLACK)), RED_CHECK)

    if play_mode == 2:
        SCREEN.blit(clock_image, (8*SQUARE_SIDE, 2.5*SQUARE_SIDE))
        if ai_depth == 1:
            SCREEN.blit(ai_easy, (8*SQUARE_SIDE + 100, 0))
        elif ai_depth == 2:
            SCREEN.blit(ai_normal, (8*SQUARE_SIDE + 100, 0))
        elif ai_depth == 3:
            SCREEN.blit(ai_hard, (8*SQUARE_SIDE + 100, 0))
        SCREEN.blit(player_pic, (8*SQUARE_SIDE + 100, 5.5 * SQUARE_SIDE))

    for position in chessgame.colored_piece_gen(printed_board, chessgame.KING, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KING,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.QUEEN, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_QUEEN,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.ROOK, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_ROOK,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.BISHOP, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_BISHOP, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.KNIGHT, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KNIGHT, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.PAWN, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_PAWN,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.JOKER, chessgame.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_JOKER,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))

    for position in chessgame.colored_piece_gen(printed_board, chessgame.KING, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KING,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.QUEEN, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_QUEEN,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.ROOK, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_ROOK,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.BISHOP, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_BISHOP, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.KNIGHT, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KNIGHT, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.PAWN, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_PAWN,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))
    for position in chessgame.colored_piece_gen(printed_board, chessgame.JOKER, chessgame.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_JOKER,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chessgame.bb2str(position)))

    pygame.display.flip()


def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()


def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chessgame.make_move(
        game, chessgame.get_AI_move(game, ai_depth))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, color)
    return new_game


def try_move(game, attempted_move):
    for move in chessgame.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chessgame.make_move(game, move)
    return game


def play_as(game, color):
    global play_mode
    global ai_depth
    global time_a
    global time_b

    run = True
    ongoing = True
    joker = 0

    if play_mode == 2:
        SCREEN = pygame.display.set_mode(
            (8*SQUARE_SIDE + 500, 8*SQUARE_SIDE), pygame.RESIZABLE)

    for_check = 0

    try:
        while run:

            CLOCK.tick(CLOCK_TICK)
            print_board(game.board, color)

            if chessgame.game_ended(game, time_a, time_b):
                set_title(SCREEN_TITLE + ' - ' +
                          chessgame.get_outcome(game, time_a, time_b))
                ongoing = False

            if ongoing and game.to_move == chessgame.opposing_color(color):
                print("AI Turn")
                for_check = 0
                game = make_AI_move(game, color)
                continue
            else:
                print(for_check)
                if for_check == 0:
                    if play_mode == 2:
                        print("for_check is 0")
                        # Set for 1 second (1000 milliseconds)
                        pygame.time.set_timer(USEREVENT, 1000)
                        pygame.time.set_timer(USEREVENT + 1, 0)

            if chessgame.game_ended(game, time_a, time_b):
                set_title(SCREEN_TITLE + ' - ' +
                          chessgame.get_outcome(game, time_a, time_b))
                ongoing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

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

                # --------------------
                if event.type == pygame.MOUSEBUTTONDOWN:
                    leaving_square = coord2str(event.pos, color)

                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, color)

                    if ongoing and game.to_move == color:
                        move = (chessgame.str2bb(leaving_square),
                                chessgame.str2bb(arriving_square))
                        game = try_move(game, move)
                        print_board(game.board, color)
                        break

                    if play_mode == 1 | play_mode == 2:
                        for_check = 0
                    # if not a_on:
                    #     # Set for 1 second (1000 milliseconds)
                    #     pygame.time.set_timer(USEREVENT, 1000)
                    #     pygame.time.set_timer(USEREVENT + 1, 0)
                    #     b_on = False
                    #     a_on = True
                    #     print("A turned On")
                    #     print("B turned Off")
                    # else:
                    #     # The other one should turn on immediately
                    #     pygame.time.set_timer(USEREVENT, 0)
                    #     pygame.time.set_timer(USEREVENT + 1, 1000)
                    #     b_on = True
                    #     a_on = False
                    #     print("B turned On")
                    #     print("A turned Off")

                # ----------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing:  # H key
                        game = make_AI_move(game, color)
                    if event.key == 117:  # U key
                        game = chessgame.unmake_move(game)
                        game = chessgame.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        print_board(game.board, color)
                        ongoing = True
                    if event.key == 99:  # C key
                        global BOARD_COLOR
                        new_colors = deepcopy(BOARD_COLORS)
                        new_colors.remove(BOARD_COLOR)
                        BOARD_COLOR = choice(new_colors)
                        print_board(game.board, color)
                    if event.key == 112 or event.key == 100:  # P or D key
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101:  # E key
                        print('eval = ' + str(chessgame.evaluate_game(game)/100))
                    if event.key == 106:  # J key
                        joker += 1
                        if joker == 13 and chessgame.get_queen(game.board, color):
                            queen_index = chessgame.bb2index(
                                chessgame.get_queen(game.board, color))
                            game.board[queen_index] = color | chessgame.JOKER
                            print_board(game.board, color)

                if event.type == pygame.VIDEORESIZE:
                    if SCREEN.get_height() != event.h:
                        resize_screen(int(event.h/8.0))
                    elif SCREEN.get_width() != event.w:
                        resize_screen(int(event.w/8.0))
                    print_board(game.board, color)

            for_check = for_check + 1
            for i in range(100):
                update_timer(time_a, time_b)
                pygame.display.flip()
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as WHITE:\n\t' if color ==
                       chessgame.WHITE else '\nPlaying as BLACK:\n\t')
        bug_file.write(game.get_move_list() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()


def update_timer(time_a, time_b):
    # Format time into minutes:seconds
    time_a_str = "%d:%02d" % (int(time_a/60), int(time_a % 60))
    time_b_str = "%d:%02d" % (int(time_b/60), int(time_b % 60))

    time_a_txt = font.render(time_a_str, 1, (255, 255, 255))
    time_b_txt = font.render(time_b_str, 1, (255, 255, 255))

    time_a_rect = time_a_txt.get_rect()
    time_a_rect.center = (760 + 140, 4.1*SQUARE_SIDE)
    time_b_rect = time_b_txt.get_rect()
    time_b_rect.center = (760 + 380, 4.1*SQUARE_SIDE)

    SCREEN.blit(time_a_txt, time_a_rect)
    SCREEN.blit(time_b_txt, time_b_rect)


def play_as_white(game=chessgame.Game()):
    return play_as(game, chessgame.WHITE)


def play_as_black(game=chessgame.Game()):
    return play_as(game, chessgame.BLACK)


def play_random_color(game=chessgame.Game()):
    color = choice([chessgame.WHITE, chessgame.BLACK])
    play_as(game, color)

# play_as_white()


def get_font(size):
    return pygame.font.SysFont("arial", size, True, True)


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


def blitz():
    global play_mode
    global ai_depth
    play_mode = 2
    while True:
        BLITZ_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        BLITZ_TEXT = get_font(100).render("BLITZ", True, "#b68f40")
        BLITZ_RECT = BLITZ_TEXT.get_rect(center=(380, 110))
        SCREEN.blit(BLITZ_TEXT, BLITZ_RECT)

        TEXT = get_font(40).render(
            "Blitz chessgame simply refers to a game of", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(40).render(
            "chessgame that has a fast time control.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 260
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(40).render(
            "Each player is given 10 minutes or less.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 320
        SCREEN.blit(TEXT, TEXT_RECT)

        BLITZ_START = Button(image=None, pos=(260, 500),
                             text_input="START", font=get_font(50), base_color="White", hovering_color="Green")
        BLITZ_BACK = Button(image=None, pos=(500, 500),
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

        for button in [BLITZ_START, BLITZ_BACK]:
            button.changeColor(BLITZ_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if BLITZ_BACK.checkForInput(BLITZ_MOUSE_POS):
                    main_menu()
                if BLITZ_START.checkForInput(BLITZ_MOUSE_POS):
                    blitz_level()
        pygame.display.update()


def blitz_level():
    global play_mode
    global ai_depth
    play_mode = 2
    while True:
        BLITZ_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        BLITZ_TEXT = get_font(100).render("BLITZ", True, "#b68f40")
        BLITZ_RECT = BLITZ_TEXT.get_rect(center=(380, 110))
        SCREEN.blit(BLITZ_TEXT, BLITZ_RECT)

        BLITZ_EASY = Button(image=None, pos=(380, 250),
                            text_input="EASY", font=get_font(75), base_color="White", hovering_color="Green")
        BLITZ_NORMAL = Button(image=None, pos=(380, 400),
                              text_input="NORMAL", font=get_font(75), base_color="White", hovering_color="Green")
        BLITZ_HARD = Button(image=None, pos=(380, 550),
                            text_input="HARD", font=get_font(75), base_color="White", hovering_color="Green")

        BLITZ_BACK = Button(image=None, pos=(680, 700),
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        for button in [BLITZ_EASY, BLITZ_NORMAL, BLITZ_HARD, BLITZ_BACK]:
            button.changeColor(BLITZ_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if BLITZ_BACK.checkForInput(BLITZ_MOUSE_POS):
                    blitz()
                if BLITZ_EASY.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 1
                    setting_time()
                if BLITZ_NORMAL.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 2
                    setting_time()
                if BLITZ_HARD.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 3
                    setting_time()
        pygame.display.update()

# Setting BLITZ Time


def setting_time():
    global time_a
    global time_b
    play_key = False
    while True:
        TIME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        BLITZ_TEXT = get_font(100).render("BLITZ", True, "#b68f40")
        BLITZ_RECT = BLITZ_TEXT.get_rect(center=(380, 110))
        SCREEN.blit(BLITZ_TEXT, BLITZ_RECT)

        # TEXT
        TEXT = get_font(25).render(
            "SETTING BLITZ TIME", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x = 280
        TEXT_RECT.y = 220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "PLAYER", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = 180
        TEXT_RECT.y = 280
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "COM", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = 600
        TEXT_RECT.y = 280
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "Q : +1 MINUTE", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x = 100
        TEXT_RECT.y = 340
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "A : -1 MINUTE", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x = 100
        TEXT_RECT.y = 370
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "P : +1 MINUTE", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x = 520
        TEXT_RECT.y = 340
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "L : -1 MINUTE", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x = 520
        TEXT_RECT.y = 370
        SCREEN.blit(TEXT, TEXT_RECT)

        # Button
        START_BUTTON = Button(image=None, pos=(380, 720),
                                text_input="START",font=get_font(75), base_color="#dcfcd4", hovering_color="White")
        SCREEN.blit(clock_image, (130, 400))

        for button in [START_BUTTON]:
            button.changeColor(TIME_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if START_BUTTON.checkForInput(TIME_MOUSE_POS):
                    # Starting Game
                    play_key = True
                    break

            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    time_a += 60 # add a minute from alloted time

                if event.key == K_a:
                    time_a -= 60 # subtract a minute

                if event.key == K_p:
                    time_b += 60

                if event.key == K_l:
                    time_b -= 60
        
        # Format time into minutes:seconds
        time_a_str = "%d:%02d" % (int(time_a/60),int(time_a%60))
        time_b_str = "%d:%02d" % (int(time_b/60),int(time_b%60) )

        time_a_txt = font.render(time_a_str, True, (255, 255, 255))
        time_b_txt = font.render(time_b_str, True, (255, 255, 255))

        time_a_rect = time_a_txt.get_rect()
        time_a_rect.center = (270, 550)
        time_b_rect = time_b_txt.get_rect()
        time_b_rect.center = (510, 550)

        SCREEN.blit(time_a_txt, time_a_rect)
        SCREEN.blit(time_b_txt, time_b_rect)
            
        if play_key:
            play_random_color()

        pygame.display.update()


def classic():
    global play_mode
    global ai_depth
    play_mode = 1
    play_key = False
    while True:
        BLITZ_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        CLASSIC_TEXT = get_font(100).render("CLASSIC", True, "#b68f40")
        CLASSIC_RECT = CLASSIC_TEXT.get_rect(center=(380, 110))
        SCREEN.blit(CLASSIC_TEXT, CLASSIC_RECT)

        CLASSIC_EASY = Button(image=None, pos=(380, 250),
                              text_input="EASY", font=get_font(75), base_color="White", hovering_color="Green")
        CLASSIC_NORMAL = Button(image=None, pos=(380, 400),
                                text_input="NORMAL", font=get_font(75), base_color="White", hovering_color="Green")
        CLASSIC_HARD = Button(image=None, pos=(380, 550),
                              text_input="HARD", font=get_font(75), base_color="White", hovering_color="Green")

        CLASSIC_BACK = Button(image=None, pos=(680, 700),
                              text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        for button in [CLASSIC_EASY, CLASSIC_NORMAL, CLASSIC_HARD, CLASSIC_BACK]:
            button.changeColor(BLITZ_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if CLASSIC_BACK.checkForInput(BLITZ_MOUSE_POS):
                    main_menu()
                if CLASSIC_EASY.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 1
                    play_key = True
                    break
                if CLASSIC_NORMAL.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 2
                    play_key = True
                    break
                if CLASSIC_HARD.checkForInput(BLITZ_MOUSE_POS):
                    ai_depth = 3
                    play_key = True
                    break
        if play_key:
            play_random_color()

        pygame.display.update()


# def crazyhouse():
#     while True:
#         CRAZY_MOUSE_POS = pygame.mouse.get_pos()

#         SCREEN.fill("black")

#         CRAZY_TEXT = get_font(100).render("CRAZY HOUSE", True, "#b68f40")
#         CRAZY_RECT = CRAZY_TEXT.get_rect(center=(380, 110))
#         SCREEN.blit(CRAZY_TEXT, CRAZY_RECT)

#         CRAZY_BACK = Button(image=None, pos=(600, 500),
#                             text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
#         CRAZY_GAME = Button(image=None, pos=(160, 500),
#                             text_input="START", font=get_font(50), base_color="White", hovering_color="Green")

#         CRAZY_BACK.changeColor(CRAZY_MOUSE_POS)
#         CRAZY_GAME.changeColor(CRAZY_MOUSE_POS)
#         CRAZY_BACK.update(SCREEN)
#         CRAZY_GAME.update(SCREEN)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if CRAZY_BACK.checkForInput(CRAZY_MOUSE_POS):
#                     main_menu()

#         pygame.display.update()

# Rule Book


def rule():
    pygame.display.set_caption("CHESS GAME - RULE BOOK")

    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        MENU_TEXT = get_font(75).render("CHESS RULE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # TEXT
        TEXT = get_font(30).render(
            "Capture all of your opponent's pieces ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "with a variety of pieces and tactics.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 250
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "If you catch your opponent's king, it's your win.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 280
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "Click NEXT for more explanation.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 500
        SCREEN.blit(TEXT, TEXT_RECT)

        # Button
        MAIN_MENU_BUTTON = Button(image=None, pos=(100, 700),
                                  text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON = Button(image=None, pos=(700, 700),
                             text_input="NEXT >", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(700, 100),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        for button in [MAIN_MENU_BUTTON, NEXT_BUTTON, QUIT_BUTTON]:
            button.changeColor(RULE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if MAIN_MENU_BUTTON.checkForInput(RULE_MOUSE_POS):
                    main_menu()
                if NEXT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule2()
                if QUIT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

# Rule Book 2


def rule2():
    pygame.display.set_caption("CHESS GAME - RULE BOOK")

    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        MENU_TEXT = get_font(75).render("CHESS RULE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # TEXT
        TEXT = get_font(30).render(
            "Each player starts with one king and queen, ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "two rooks and bishops, two knights, and eight pawns.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 250
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "A player using white pieces is called 'white' ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 310
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "and a player using black pieces is called 'black'.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 340
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "When it is your turn, you must move your pieces, ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 400
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(30).render(
            "and different pieces have different magic moves.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 430
        SCREEN.blit(TEXT, TEXT_RECT)

        # Button
        MAIN_MENU_BUTTON = Button(image=None, pos=(100, 700),
                                  text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON = Button(image=None, pos=(700, 700),
                             text_input="NEXT >", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        PREVIOUS_BUTTON = Button(image=None, pos=(550, 700),
                                 text_input="< PREVIOUS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(700, 100),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        for button in [MAIN_MENU_BUTTON, NEXT_BUTTON, QUIT_BUTTON, PREVIOUS_BUTTON]:
            button.changeColor(RULE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if MAIN_MENU_BUTTON.checkForInput(RULE_MOUSE_POS):
                    main_menu()
                if NEXT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule3()
                if PREVIOUS_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule()
                if QUIT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


# Rule Book 3


def rule3():
    pygame.display.set_caption("CHESS GAME - RULE BOOK")

    # Insert Image
    ImgKing = pygame.image.load("images/King_move.png")
    ImgKing = pygame.transform.scale(ImgKing, (200, 200))
    ImgKing_Rect = ImgKing.get_rect()
    ImgKing_Rect.x = 80
    ImgKing_Rect.y = 200

    ImgQueen = pygame.image.load("images/Queen_move.png")
    ImgQueen = pygame.transform.scale(ImgQueen, (200, 200))
    ImgQueen_Rect = ImgQueen.get_rect()
    ImgQueen_Rect.x = 300
    ImgQueen_Rect.y = 200

    ImgRook = pygame.image.load("images/Rook_move.png")
    ImgRook = pygame.transform.scale(ImgRook, (200, 200))
    ImgRook_Rect = ImgRook.get_rect()
    ImgRook_Rect.x = 520
    ImgRook_Rect.y = 200

    ImgBishop = pygame.image.load("images/Bishop_move.png")
    ImgBishop = pygame.transform.scale(ImgBishop, (200, 200))
    ImgBishop_Rect = ImgBishop.get_rect()
    ImgBishop_Rect.x = 80
    ImgBishop_Rect.y = 430

    ImgKnight = pygame.image.load("images/Knight_move.png")
    ImgKnight = pygame.transform.scale(ImgKnight, (200, 200))
    ImgKnight_Rect = ImgKnight.get_rect()
    ImgKnight_Rect.x = 300
    ImgKnight_Rect.y = 430

    ImgPawn = pygame.image.load("images/Pawn_move.png")
    ImgPawn = pygame.transform.scale(ImgPawn, (200, 200))
    ImgPawn_Rect = ImgPawn.get_rect()
    ImgPawn_Rect.x = 520
    ImgPawn_Rect.y = 430

    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        MENU_TEXT = get_font(75).render("CHESS RULE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # TEXT
        TEXT = get_font(30).render(
            "Below is the magic of the pieces.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 150
        SCREEN.blit(TEXT, TEXT_RECT)

        # Button
        MAIN_MENU_BUTTON = Button(image=None, pos=(100, 700),
                                  text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON = Button(image=None, pos=(700, 700),
                             text_input="NEXT >", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        PREVIOUS_BUTTON = Button(image=None, pos=(550, 700),
                                 text_input="< PREVIOUS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(700, 100),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        for button in [MAIN_MENU_BUTTON, NEXT_BUTTON, QUIT_BUTTON, PREVIOUS_BUTTON]:
            button.changeColor(RULE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if MAIN_MENU_BUTTON.checkForInput(RULE_MOUSE_POS):
                    main_menu()
                if NEXT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule4()
                if PREVIOUS_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule2()
                if QUIT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        SCREEN.blit(ImgKing, ImgKing_Rect)
        SCREEN.blit(ImgQueen, ImgQueen_Rect)
        SCREEN.blit(ImgRook, ImgRook_Rect)
        SCREEN.blit(ImgBishop, ImgBishop_Rect)
        SCREEN.blit(ImgKnight, ImgKnight_Rect)
        SCREEN.blit(ImgPawn, ImgPawn_Rect)
        pygame.display.update()

# Rule Book


def rule4():
    pygame.display.set_caption("CHESS GAME - RULE BOOK")

    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        MENU_TEXT = get_font(75).render("CHESS RULE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # TEXT
        TEXT = get_font(30).render(
            "Castling", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "Castling is a special move for the king, ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 280
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "and will tie the rook and king together.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 310
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "First, place the king two squares in front of the look king, ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 340
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "then move it to the right next to or inside the rook.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 370
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "At this time, you must move the king first, and you can ", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 400
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "move the rook after moving the king two squares.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 430
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(25).render(
            "The next chapter is an example of Castling.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.centerx = round(400)
        TEXT_RECT.y = 490
        SCREEN.blit(TEXT, TEXT_RECT)

        # Button
        MAIN_MENU_BUTTON = Button(image=None, pos=(100, 700),
                                  text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON = Button(image=None, pos=(700, 700),
                             text_input="NEXT >", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        PREVIOUS_BUTTON = Button(image=None, pos=(550, 700),
                                 text_input="< PREVIOUS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(700, 100),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        for button in [MAIN_MENU_BUTTON, NEXT_BUTTON, QUIT_BUTTON, PREVIOUS_BUTTON]:
            button.changeColor(RULE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if MAIN_MENU_BUTTON.checkForInput(RULE_MOUSE_POS):
                    main_menu()
                if NEXT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule5()
                if PREVIOUS_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule3()
                if QUIT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

# Rule Book 5


def rule5():
    pygame.display.set_caption("CHESS GAME - RULE BOOK")

    # Insert Image
    Imgcastling1 = pygame.image.load("images/castling_1.png")
    Imgcastling1 = pygame.transform.scale(Imgcastling1, (300, 300))
    Imgcastling1_Rect = Imgcastling1.get_rect()
    Imgcastling1_Rect.x = 50
    Imgcastling1_Rect.y = 200

    Imgcastling2 = pygame.image.load("images/castling_2.png")
    Imgcastling2 = pygame.transform.scale(Imgcastling2, (300, 300))
    Imgcastling2_Rect = Imgcastling2.get_rect()
    Imgcastling2_Rect.x = 400
    Imgcastling2_Rect.y = 200

    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")

        MENU_TEXT = get_font(75).render("CHESS RULE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Button
        MAIN_MENU_BUTTON = Button(image=None, pos=(100, 700),
                                  text_input="MENU", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        PREVIOUS_BUTTON = Button(image=None, pos=(550, 700),
                                 text_input="< PREVIOUS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(700, 100),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        for button in [MAIN_MENU_BUTTON, QUIT_BUTTON, PREVIOUS_BUTTON]:
            button.changeColor(RULE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if MAIN_MENU_BUTTON.checkForInput(RULE_MOUSE_POS):
                    main_menu()
                if PREVIOUS_BUTTON.checkForInput(RULE_MOUSE_POS):
                    rule4()
                if QUIT_BUTTON.checkForInput(RULE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        SCREEN.blit(Imgcastling1, Imgcastling1_Rect)
        SCREEN.blit(Imgcastling2, Imgcastling2_Rect)
        pygame.display.update()


def main_menu():
    pygame.display.set_caption("CHESS GAME")

    while True:
        SCREEN.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CHESS GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        BLITZ_BUTTON = Button(image=None, pos=(380, 450),
                              text_input="BLITZ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CLASSIC_BUTTON = Button(image=None, pos=(380, 300),
                                text_input="CLASSIC", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOW_TO_PLAY_BUTTON = Button(image=None, pos=(380, 600),
                                    text_input="HOW TO PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        EXIT_BUTTON = Button(image=None, pos=(680, 700),
                             text_input="EXIT", font=get_font(60), base_color="gray", hovering_color="White")
        for button in [BLITZ_BUTTON, CLASSIC_BUTTON, EXIT_BUTTON, HOW_TO_PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if BLITZ_BUTTON.checkForInput(MENU_MOUSE_POS):
                    blitz()
                if CLASSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    classic()
                if HOW_TO_PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rule()
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()

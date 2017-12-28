import sys
import tty
import signal
import termios
import random
import pygame
from matrix import (TetrisMatrixGame, SquareBlock, TeBlock, ZetaBlock, JayBlock)


def getch():
    """getch() -> key character

    Read a single keypress from stdin and return the resulting character. 
    Nothing is echoed to the console. This call will block if a keypress 
    is not already available, but will not wait for Enter to be pressed. 

    If the pressed key was a modifier key, nothing will be detected; if
    it were a special function key, it may return the first character of
    of an escape sequence, leaving additional characters in the buffer.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class GameTetris(object):
    def  __init__(self, *args, **kwargs):
        self.matrix_game = TetrisMatrixGame()
        self.shape = self.matrix_game.shape
        self.points = 0
        self.lines = 0
        self.level = 1
        self.time = 0
        self.started = False

        self.blocks = (
            SquareBlock,
            TeBlock,
            ZetaBlock,
            JayBlock
        )

    def restart(self):
        self.points = 0
        self.points = 0
        self.lines = 0
        self.level = 1
        self.time = 0
        self.colstart = 5
        self.col = None

    def start(self):
        self.started = True;

        print "************************** START GAME ************************"

        while self.started:
            next_block_class = random.choice(self.blocks)
            actual_block_class = random.choice(self.blocks)

            actual_block = actual_block_class()
            next_block = next_block_class()

            self.col = self.colstart
            print "Actual block: {0}".format(actual_block)

            for row in range(4, self.matrix_game.shape[0]):
                signal.alarm(1 / 1)
                keypress = ord(getch())

                # print keypress
                if keypress == 67:
                    if self.matrix_game.shape[1] - self.col > 0:
                        self.col += 1

                if keypress == 68:
                    if self.col > 0:
                        self.col -= 1
                
                if keypress == 113:
                    self.started = False
                    break

                signal.alarm(0)
                print "{0} {1}".format(row, self.col)

                if not self.matrix_game.validate_add_matrix(actual_block, rownum=row, colnum=self.col):
                    continue

                self.matrix_game.add_block(actual_block, row, self.col)


if __name__ == "__main__":
    # tetris = GameTetris()
    # tetris.restart()
    # tetris.start()
    pygame.init()

    size = width, height = 800, 700
    speed = [0, 1]
    black = 0, 0, 0
    GREEN = (  0, 255,   0)
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("ball.bmp")
    ballrect = ball.get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)
        pygame.draw.line(screen, WHITE, [200, 0], [200, 700], 10)
        pygame.draw.line(screen, WHITE, [600, 0], [600, 700], 10)

        rect = pygame.rect.Rect([400, 10, 15, 15])
        pygame.draw.rect(screen, GREEN, rect)

        # ballrect = rect.move(speed)

        rect.move_ip(0, 1)
        if rect.top < 0 or rect.bottom > height:
            speed[1] = - speed[1]
        # ballrect = ballrect.move(speed)
        # if ballrect.left < 0 or ballrect.right > width:
        #     speed[0] = -speed[0]
        # if ballrect.top < 0 or ballrect.bottom > height:
        #     speed[1] = -speed[1]

        # screen.blit(rect, ballrect)
        # pygame.display.flip()
        pygame.display.update()
    # tetris_game = TetrisMatrixGame()
    # tetris_game._print()

    # print "************************* Square ********************************"
    # square = SquareBlock()
    # square._print()
    # print "Pivote"
    # square._get_pivot()

    # print "************************* Te ********************************"
    # te = TeBlock()
    # te._print()
    # print "Pivote"
    # te._get_pivot()

    # print "************************* Zeta ********************************"
    # zeta = ZetaBlock()
    # zeta._print()
    # print "Pivote"
    # zeta._get_pivot()
    # print

    # print "************************* Add Square ********************************"
    # if tetris_game.validate_add_matrix(square, rownum=27, colnum=0):
    #     tetris_game.add_block(square, 27, 0)
    #     print "Square Added"

    # print "************************* Add Te ********************************"
    # if tetris_game.validate_add_matrix(te, rownum=26, colnum=1):
    #     tetris_game.add_block(te, 26, 1)
    #     print "Te Added"
    # else:
    #     print "Can't add TE"

    # print "************************* Add Zeta ********************************"
    # if tetris_game.validate_add_matrix(zeta, rownum=26, colnum=3):
    #     tetris_game.add_block(zeta, 26, 3)
    #     print "Zeta Added"
    # else:
    #     print "Can't add Zeta"

    # tetris_game._print()
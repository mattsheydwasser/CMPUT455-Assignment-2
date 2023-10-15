#!/usr/bin/python3
# Set the path to your python3 above

"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller

Used signal timer based off this reference:
https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/html/python3-bootcamp.html#Time
https://stackoverflow.com/questions/14920384/stop-code-after-time-period

"""
from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR, BLACK, WHITE, opponent
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
from gtp_connection import  alphabeta
import signal


class Go0(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, "Go0", 1.0)

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=False)
    
    def solve(self, board: GoBoard, timer):
       
        # tries to find best move for toPlay within the time limit
        # unknown move otherwise
        
        signal.signal(signal.SIGALRM, signalHandler)
        signal.alarm(timer)
        
        copy = board.copy()
        
        # set current and opponent players (toPlay is black, opponent is white)
        if board.current_player == WHITE:
            player = 'w'
        elif board.current_player == BLACK:
            player = 'b'
            
        if opponent(board.current_player) == WHITE:
            opp = 'w'
        elif opponent(board.current_player) == BLACK:
            opp = 'b'
            
        try:
            value, moveToPlay = alphabeta(copy, -10, 10)
            
            if value > 0:
                # if value is positive, toPlay should play it
                return player, moveToPlay
            elif value == 0:
                # if zero, this means best play for toPlay is drawing
                return 'draw', moveToPlay
            else:
                # if negative, opponent has best move
                return opp, None
            
        except TimeoutError:
            return 'unknown', None
        finally:
            signal.alarm(0)

def signalHandler(sig, frame):
    # handler for signal timer, assert an error 
    # https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
    raise TimeoutError

def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()

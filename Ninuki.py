#!/usr/bin/python3
# Set the path to your python3 above

"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller

Used signal timer based off this reference:
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
       
        # signal.signal(signal.SIGALRM, handler())
        # signal.alarm(timer)
        
        bo = board.copy()
        # try:
        value, moveToPlay = alphabeta(bo, -10, 10)
        print('-------', value, moveToPlay)        
        if value > 0:
            return 'b', moveToPlay
        elif value == 0:
            return 'draw', moveToPlay
        else:
            return 'w', None
        # except TimeoutError:
        #     return 'unknown', None
        # finally:
        #     signal.alarm(0)
        
       

def handler():
    raise TimeoutError()

def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()

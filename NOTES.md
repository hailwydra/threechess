Notes, bugs and ideas

Testing by adding the stuff at the top of the code:

# TODO: make moves available to each player, rotate board + pieces func
# Make knight_moves for unpromoted
# impose restricitions on movement of bishop and rook if other pieces in the way

# IDEA: could make rotateall120 a decorator with number of turns input and revert to original after

# DEBUG: non-pawn pieces don't respond well to piece_moves, return only original position - SOLVED
# Might be a problem with piece.plyr type (int or str) but might not be ... who knows

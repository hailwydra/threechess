## Notes, bugs and ideas

**TO DO:**
- Make moves available to each player, rotate board + pieces func - DONE
- Make knight_moves for unpromoted
- Impose restricitions on movement of bishop and rook if other pieces in the way (rook semi-complete)
- Start on graphic capacilities (online)
- Create/find graphics

**IDEAS:**
- Could make rotateall120 a decorator with number of turns input and revert to original after - USED A FUNCTIONAL

**DEBUG:** 
- Non-pawn pieces don't respond well to piece_moves, return only original position - SOLVED
- Might be a problem with piece.plyr type (int or str) but might not be ... who knows - SOLVED
- play_game function problems -> when in game.move can't seem to get index() of frmpiece

**OTHER:**
- Testing by adding the stuff at the top of the code

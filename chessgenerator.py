from matplotlib import pyplot as plt

class Piece:
    def __init__(self, position, player, typ, promoted = False):
        self.pos = position
        self.plyr = player
        self.typ = typ
        self.prom = [promoted, '']

    def __repr__(self):
        return f"[{self.pos}, {self.plyr}, {self.typ}, {self.prom}]"

class Board:
    def __init__(self):
        self.squares = []
        for i in range(-6,7):
            for j in range(-6,7):
                for k in range(-6,7):
                    if i + j + k == 0:
                        self.squares.append([i,j,k])
        self.add_colours()
        self.pieces = {
            '1': [],
            '2': [],
            '3': []
        }
        for i in range(1,4):
            plyr = str(i)
            self.rotate120(plyr, self.setup, False, plyr)

    def getcor(self, i):
        return self.squares[i][:3]

    def add_colours(self):
        colours = ['r', 'b', 'w']
        c_list = []
        index = 0
        for i in range(-6,1):
            length = 13 + i
            for j in range(length):
                c_list.append(colours[index])
                index = (index + 1) % 3
            if length % 3 == 2:
                index = (index + 2) % 3
            elif length % 3 == 0:
                index = (index + 1) % 3
        index = (index + 1)% 3
        for i in range(-1,-7,-1):
            length = 13 + i
            for j in range(length):
                c_list.append(colours[index])
                index = (index + 1) % 3
            if length % 3 == 1:
                index = (index + 1) % 3
            elif length % 3 == 0:
                index = (index + 2) % 3
        for i in range(127):
            self.squares[i].append(c_list[i])

    #general rotation - for only board tiles set all to False
    def rotate120(self, player, func, all = True, *args, **kwargs):
        if all:
            for i in range(127):
                x, y, z = self.squares[i][0], self.squares[i][1], self.squares[i][2]
                self.squares[i][0], self.squares[i][1], self.squares[i][2] = y, z ,x
            for i in range(1,4):
                for j in range(len(self.pieces[str(i)])):
                    x, y, z = self.pieces[str(i)][j].pos[0], self.pieces[str(i)][j].pos[1], self.pieces[str(i)][j].pos[2]
                    self.pieces[str(i)][j].pos[0], self.pieces[str(i)][j].pos[1], self.pieces[str(i)][j].pos[2] = y, z ,x
        elif not all:
            def rotate():
                for i in range(127):
                    x, y, z = self.squares[i][0], self.squares[i][1], self.squares[i][2]
                    self.squares[i][0], self.squares[i][1], self.squares[i][2] = y, z ,x
        for i in range(int(player) - 1):
            rotate()
        func(*args, **kwargs)
        for i in range(4 - int(player)):
            rotate()

    def setup(self, player):
        front_row = ['rook', 'knight', 'bishop', 'king', 'bishop', 'knight', 'rook']
        for i in range(7):
            cor = self.getcor(i)
            newpiece = Piece(cor, player, front_row[i])
            if i in [0,1,2]:
                newpiece.prom[1] = 'r'
            elif i in [4,5,6]:
                newpiece.prom[1] = 'l'
            self.pieces[player].append(newpiece)
        for i in range(7,15):
            cor = self.getcor(i)
            newpawn = Piece(cor, player, 'pawn')
            if i in [7,8,9,10]:
                newpawn.prom[1] = 'r'
            elif i in [11,12,13,14]:
                newpawn.prom[1] = 'l'
            self.pieces[player].append(newpawn)

    def contains(self, cor):
        pieces = [x for y in self.pieces.values() for x in y]
        for piece in pieces:
            if piece.pos == cor:
                return piece
        else:
            return None
    # Currently useless but might come in useful in future
    def exists(self, piece):
        for cor in self.square:
            if piece.pos == cor[:3]:
                return True
            else:
                return False

    #'squash' board into 2d format - for visual repr
    def to2d(self):
        for i in range(127):
            self.squares[i].pop(2)
        for i in ['1','2','3']:
            for j in range(15):
                self.pieces[i][j].pos.pop(2)

class Game:
    def __init__(self,players):
        self.board = Board()
        self.players = {'1':players[0], '2':players[1], '3':players[2]}
        self.captured = {'1':[],'2':[],'3':[]}
        self.turn = 1
        self.winner = ""
    def move(self, player, frm, new):
        allowed = True
        capture = False
        frmpiece = self.board.contains(frm)
        newpiece = self.board.contains(new)
        playerpieces = list(self.board.pieces[player])
        #new exists in board
        for sq in self.board.squares:
            if new == sq[:3]:
                break
        else:
            allowed = False
        #piece is player's or can capture
        if newpiece != None:
            if newpiece.plyr == player:
                allowed = False
            else:
                capture = True
        #move is in possible moves
        if not new in self.piece_moves(frmpiece):
            allowed = False
        if allowed:
            if capture:
                cap_piece = newpiece
                self.captured[player].append(cap_piece)
                self.board.pieces[cap_piece.plyr].remove(cap_piece)
            self.board.pieces[player][playerpieces.index(frmpiece)].pos = new

    #calculating the possible moves a piece can have
    def piece_moves(self, piece):
        def move_by(frm, by):
            temp = list(frm)
            for i in range(3):
                temp[i] = by[i] + frm[i]
            return temp

        def pawn_moves(self, piece):
            current = list(piece.pos)
            moves = []
            if False in piece.prom:
                if 'l' in piece.prom:
                    moves.append(move_by(current, [1,0,1]))
                elif 'r' in piece.prom:
                    moves.append(move_by(current, [1,-1,0]))
            return moves

        def king_moves(self, piece):
            current = list(piece.pos)
            moves = []
            for i in [-2,-1,0,1,2]:
                for j in [-2,-1,0,1,2]:
                    for k in [-2,-1,0,1,2]:
                        by = [i, j, k]
                        if i+j+k == 0:
                            if not(-2 in by and 2 in by and 0 in by):
                                moves.append(move_by(current, by))
            if current in moves:
                moves.remove(current)
            if False in piece.prom:
                for mv in moves:
                    if current[0] - mv[0] >= 0:
                        moves.remove(mv)
            return moves

        def bishop_moves(self, piece):
            current = list(piece.pos)
            moves = []
            for i in range(-6, 7):
                for j in range(-6, 7):
                    for k in range(-6, 7):
                        if i + j + k == 0 and (i == k or j == i or k == j):
                            moves.append(move_by(current, [i,j,k]))
            if current in moves:
                moves.remove(current)
            for mv in moves:
                for pos in self.board.squares:
                    if mv == pos[:3]:
                        break
                else:
                    move.remove(mv)

            if False in piece.prom:
                for mv in moves:
                    if mv[0] < current[0]:
                        moves.remove(mv)
                    if 'l' in piece.prom:
                        if mv[1] - mv[2] < current[1] - current[2]:
                            moves.remove(mv)
                    elif 'r' in piece.prom:
                        if mv[2] - mv[1] < current[2] - current[1]:
                            moves.remove(mv)
            return moves

        def rook_moves(self, piece):
            current = list(piece.pos)
            moves = []
            if piece.prom == True:
                for i in range(-12,13):
                    for j in range(-12,13):
                        moves.append([i,j,current[2]])
                        moves.append([current[2],i,j])
                        moves.append([i,current[2],j])
                for mv in moves:
                    exists = False
                    for pos in self.board.squares:
                        if mv == pos[:3]:
                            exists = True
                    if not exists:
                        moves.remove(mv)
            if False in piece.prom:
                if 'l' in piece.prom:
                    for i in range(1,7):
                        moves.append(move_by(current,[i,0,-i]))
                elif 'r' in piece.prom:
                    for i in range(1,7):
                        moves.append(move_by(list(piece.pos),[i,-i,0]))

            for mv in moves:
                if self.board.contains(mv) != None:
                    #find line (similar coordinate)
                    line = None
                    for i in range(3):
                        if mv[i] == current[i]:
                            line = i
                            break
                    diff = mv[(line + 1) % 3] - current[(line + 1) % 3]
                    diff = int(diff/abs(diff))
                    for i in range(mv[(line + 1) % 3], 7 * diff, diff):
                        forbidden = [None,None,None]
                        forbidden[line] = current[line]
                        forbidden[(line + 1) % 3] = i
                        forbidden[(line + 2) % 3] = -1 * (current[line] + 1)
                        if forbidden in moves:
                            moves.remove(forbidden)
            if current in moves:
                moves.remove(current)
            return moves

        def knight_moves(self, piece):
            current = list(piece.pos)
            moves = []
            if True in piece.prom:
                #sorry about this - M
                possibilities = [[1,2,-3],[2,1,-3],[3,-1,-2],[3,-2,-1],[2,-3,1],[1,-3,2],[-1,-2,3],[-2,-1,3],[-3,1,2],[-3,2,1],[-2,3,-1],[-1,3,-2]]
                for i in possibilities:
                    moves.append(move_by(current, i))
            if current in moves:
                moves.remove(current)
            return moves
        movesdict = {
            'pawn': pawn_moves,
            'king': king_moves,
            'bishop': bishop_moves,
            'rook': rook_moves,

        }
        return movesdict[piece.typ](self,piece)


#theoretical game // semi pseudo
def play_game(player_list):
    game = Game(player_list)
    while not game.winner:
        player = str(((game.turn - 1) % 3 + 1))
        print(f"{game.players[player]}\'s move")
        frm = input('From >>')
        new = input('To >>')
        game.board.rotate120(str(player), game.move, True, player, frm, new)
        game.turn += 1
        #show
        game.board.to2d()
        showboard(game.board.squares)
        showpieces(game.board.pieces)
        plt.xlim(-6.5,6.5)
        plt.show()

#move tests
#game.move('1', [-5,-1,6], [-4,-2,6])
#game.move('1', [-5,0,5], [-4,-1,5])
#game.move('1', [-6,3,3], [-4,2,2])

#for visual repr on pyplot
sc = 0.86603
def showboard(space):
    x = []
    y = []
    c = []
    for i in space:
        x.append(i[0] * sc)
        y.append(i[1] + (0.5 * i[0]))
        if i[2] == 'b':
            c.append('k')
        elif i[2] == 'r':
            c.append('xkcd:dark red')
        elif i[2] == 'w':
            c.append('xkcd:beige')
    plt.scatter(x,y, 1200, c = c, marker = 'H')
def showpieces(p):
    for i in range(15):
        a = p['1'][i].pos[0]
        b = p['1'][i].pos[1] + 0.5 * a
        plt.scatter(a * sc,b,c="r")
    for i in range(15):
        a = p['2'][i].pos[0]
        b = p['2'][i].pos[1] + 0.5 * a
        plt.scatter(a * sc, b,c="g")
    for i in range(15):
        a = p['3'][i].pos[0]
        b = p['3'][i].pos[1] + 0.5 * a
        plt.scatter(a * sc,b,c="y")

play_game(['Gauss','Riemann','Euler'])
